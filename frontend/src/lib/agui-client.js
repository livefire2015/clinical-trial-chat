/**
 * AG-UI Client Service
 * Handles communication with the backend agent via AG-UI protocol over SSE
 */
import { HttpAgent } from '@ag-ui/client'

const API_BASE_URL = 'http://localhost:8000'

/**
 * Create and configure AG-UI agent runner
 * @param {Array} initialMessages - Initial message history
 */
export function createAgentRunner(initialMessages = []) {
  return new HttpAgent({
    url: `${API_BASE_URL}/api/agent/run`,
    initialMessages: initialMessages,
  })
}

/**
 * Generate a unique ID for messages
 */
function generateId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Run agent with a user message
 * @param {string} message - User message
 * @param {Function} onEvent - Callback for AG-UI events
 * @param {Array} messageHistory - Previous messages
 * @returns {Promise<void>}
 */
export async function runAgent(message, onEvent, messageHistory = []) {
  // Build message history including the new message
  // AG-UI requires messages to have an 'id' field
  const messages = [
    ...messageHistory.map((msg) => ({
      ...msg,
      id: msg.id || generateId(),
    })),
    {
      id: generateId(),
      role: 'user',
      content: message,
    },
  ]

  console.log('Sending messages to agent:', messages)

  // Create agent with initial messages
  const agent = createAgentRunner(messages)

  try {
    // Run the agent using HttpAgent API with proper subscriber pattern
    const result = await agent.runAgent(
      {}, // Pass empty object since messages are already in the agent
      {
        onEvent: (params) => {
          // Forward the event from params to the callback
          console.log('AG-UI Event:', params.event)
          onEvent(params.event)
        },
        onRunFailed: (params) => {
          console.error('AG-UI Run Failed:', params.error)
          onEvent({
            type: 'error',
            error: params.error.message || 'An error occurred',
          })
        },
      }
    )

    // Handle completion
    console.log('Agent run completed', result)
  } catch (error) {
    console.error('AG-UI Error:', error)
    onEvent({
      type: 'error',
      error: error.message || 'An error occurred',
    })
  }
}
