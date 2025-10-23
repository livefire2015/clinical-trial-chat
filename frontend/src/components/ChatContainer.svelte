<script>
  import { runAgent } from '../lib/agui-client.js'
  import ChatMessage from './ChatMessage.svelte'

  let messages = $state([])
  let inputValue = $state('')
  let isLoading = $state(false)
  let currentResponse = $state('')

  async function handleSend() {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    inputValue = ''
    isLoading = true
    currentResponse = ''

    // Add user message to UI
    messages = [
      ...messages,
      {
        role: 'user',
        content: userMessage,
      },
    ]

    // Prepare message history for AG-UI
    const messageHistory = messages.map((msg) => ({
      role: msg.role,
      content: msg.content,
    }))

    try {
      await runAgent(userMessage, handleEvent, messageHistory.slice(0, -1))

      // Add final assistant response to messages
      if (currentResponse) {
        messages = [
          ...messages,
          {
            role: 'assistant',
            content: currentResponse,
          },
        ]
      }
    } catch (error) {
      console.error('Error running agent:', error)
      messages = [
        ...messages,
        {
          role: 'assistant',
          content: 'Sorry, an error occurred. Please try again.',
        },
      ]
    } finally {
      isLoading = false
      currentResponse = ''
    }
  }

  function handleEvent(event) {
    switch (event.type) {
      case 'message_delta':
        // Streaming text from assistant
        if (event.delta?.content) {
          currentResponse += event.delta.content
        }
        break

      case 'message_done':
        // Message complete
        break

      case 'tool_call_start':
        console.log('Tool call:', event.tool_name)
        break

      case 'tool_call_result':
        console.log('Tool result:', event.result)
        break

      case 'error':
        console.error('AG-UI error:', event.error)
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
        <ChatMessage {message} />
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
