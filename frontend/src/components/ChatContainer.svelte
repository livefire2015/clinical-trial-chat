<script>
  import { runAgent } from '../lib/agui-client.js'
  import ChatMessage from './ChatMessage.svelte'
  import ToolCallMessage from './ToolCallMessage.svelte'
  import ErrorMessage from './ErrorMessage.svelte'

  let messages = $state([])
  let inputValue = $state('')
  let isLoading = $state(false)
  let currentResponse = $state('')

  // Track active tool calls
  let activeTools = $state(new Map()) // toolCallId -> tool message object
  let toolArgs = $state(new Map()) // toolCallId -> accumulated args

  function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  async function handleSend() {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    inputValue = ''
    isLoading = true
    currentResponse = ''

    // Add user message to UI with ID
    const userMessageObj = {
      id: generateId(),
      role: 'user',
      content: userMessage,
    }

    messages = [...messages, userMessageObj]

    // Prepare message history for AG-UI (preserve all fields including id)
    const messageHistory = messages.map((msg) => ({
      id: msg.id,
      role: msg.role,
      content: msg.content,
    }))

    try {
      await runAgent(userMessage, handleEvent, messageHistory.slice(0, -1))

      // Add final assistant response to messages with ID
      if (currentResponse) {
        messages = [
          ...messages,
          {
            id: generateId(),
            role: 'assistant',
            content: currentResponse,
          },
        ]
      }
    } catch (error) {
      console.error('Error running agent:', error)
      // Only show generic error if no error message was already added via handleEvent
      // (RUN_ERROR events add their own error messages)
      const lastMessage = messages[messages.length - 1]
      if (!lastMessage || lastMessage.type !== 'error') {
        messages = [
          ...messages,
          {
            id: generateId(),
            type: 'error',
            content: 'Sorry, an unexpected error occurred. Please try again.',
          },
        ]
      }
    } finally {
      isLoading = false
      currentResponse = ''
      // Clear tool tracking
      activeTools.clear()
      toolArgs.clear()
    }
  }

  function handleEvent(event) {
    console.log('Received event:', event.type, event)

    switch (event.type) {
      case 'TEXT_MESSAGE_START':
        // New message starting
        console.log('Message started:', event.messageId)
        break

      case 'TEXT_MESSAGE_CONTENT':
        // Streaming text content from assistant
        if (event.delta) {
          currentResponse += event.delta
        }
        break

      case 'TEXT_MESSAGE_END':
        // Message complete
        console.log('Message ended:', event.messageId)
        break

      case 'TOOL_CALL_START':
        console.log('Tool call started:', event.toolCallId, event.toolCallName)
        // Create a new tool message
        const toolMessage = {
          id: generateId(),
          type: 'tool',
          toolCallId: event.toolCallId,
          toolName: event.toolCallName,
          status: 'loading',
          args: null,
          result: null,
        }
        activeTools.set(event.toolCallId, toolMessage)
        toolArgs.set(event.toolCallId, '')
        messages = [...messages, toolMessage]
        break

      case 'TOOL_CALL_ARGS':
        // Accumulate tool arguments as they stream
        if (event.toolCallId) {
          const currentArgs = toolArgs.get(event.toolCallId) || ''
          toolArgs.set(event.toolCallId, currentArgs + event.delta)
        }
        break

      case 'TOOL_CALL_END':
        // Tool arguments complete, update the message
        if (event.toolCallId) {
          const tool = activeTools.get(event.toolCallId)
          const args = toolArgs.get(event.toolCallId)
          if (tool) {
            tool.args = args
            // Trigger reactivity
            messages = [...messages]
          }
        }
        break

      case 'TOOL_CALL_RESULT':
        console.log('Tool result:', event.toolCallId, event.result)
        // Update tool message with result
        const toolWithResult = activeTools.get(event.toolCallId)
        if (toolWithResult) {
          toolWithResult.status = 'complete'
          toolWithResult.result = event.result
          // Trigger reactivity
          messages = [...messages]
        }
        break

      case 'RUN_ERROR':
        console.error('AG-UI run error:', event)
        // Add error message to chat
        const errorMessage = {
          id: generateId(),
          type: 'error',
          content: event.message || 'An error occurred',
        }
        messages = [...messages, errorMessage]
        // Mark any active tools as error
        activeTools.forEach((tool) => {
          if (tool.status === 'loading') {
            tool.status = 'error'
          }
        })
        messages = [...messages]
        break

      case 'error':
        // Custom error from our client wrapper
        console.error('AG-UI error:', event.error)
        // Only add error message if it's not already a network error
        // (network errors are expected after RUN_ERROR)
        if (!event.error.includes('network error')) {
          const customErrorMessage = {
            id: generateId(),
            type: 'error',
            content: event.error || 'An error occurred',
          }
          messages = [...messages, customErrorMessage]
        }
        break
    }
  }

  function handleKeypress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }
</script>

<div class="chat-container">
  <div class="chat-messages">
    {#if messages.length === 0}
      <div class="empty-state">
        <p>Start a conversation about clinical trial data</p>
        <p class="subtitle">
          Ask about statistics, compliance checks, or query trial databases
        </p>
      </div>
    {:else}
      {#each messages as message}
        {#if message.type === 'tool'}
          <ToolCallMessage {message} />
        {:else if message.type === 'error'}
          <ErrorMessage {message} />
        {:else}
          <ChatMessage {message} />
        {/if}
      {/each}
      {#if isLoading && currentResponse}
        <ChatMessage
          message={{ role: 'assistant', content: currentResponse, streaming: true }}
        />
      {/if}
    {/if}
  </div>

  <div class="chat-input">
    <input
      type="text"
      bind:value={inputValue}
      onkeypress={handleKeypress}
      placeholder="Ask about clinical trial statistics, compliance, or data..."
      disabled={isLoading}
    />
    <button onclick={handleSend} disabled={isLoading || !inputValue.trim()}>
      {isLoading ? 'Sending...' : 'Send'}
    </button>
  </div>
</div>

<style>
  .chat-container {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    height: 600px;
    display: flex;
    flex-direction: column;
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #a0aec0;
  }

  .chat-input {
    border-top: 1px solid #e2e8f0;
    padding: 1rem;
    display: flex;
    gap: 0.5rem;
  }

  .chat-input input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    font-size: 0.875rem;
  }

  .chat-input input:focus {
    outline: none;
    border-color: #4299e1;
  }

  .chat-input button {
    padding: 0.75rem 1.5rem;
    background: #4299e1;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
  }

  .chat-input button:hover:not(:disabled) {
    background: #3182ce;
  }

  .chat-input button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .empty-state .subtitle {
    font-size: 0.875rem;
    color: #cbd5e0;
    margin-top: 0.5rem;
  }
</style>
