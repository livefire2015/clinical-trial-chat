/**
 * AG-UI Client Service
 * Handles communication with the backend agent via AG-UI protocol over SSE
 */
import { HttpAgent } from '@ag-ui/client'

const API_BASE_URL = 'http://localhost:8000'

/**
 * Create and configure AG-UI agent runner
 */
export function createAgentRunner() {
  return new HttpAgent({
    url: `${API_BASE_URL}/api/agent/run`,
  })
}

/**
 * Run agent with a user message
 * @param {string} message - User message
 * @param {Function} onEvent - Callback for AG-UI events
 * @param {Array} messageHistory - Previous messages
 * @returns {Promise<void>}
 */
export async function runAgent(message, onEvent, messageHistory = []) {
  const agent = createAgentRunner()

  // Build message history including the new message
  const messages = [
    ...messageHistory,
    {
      role: 'user',
      content: message,
    },
  ]

  try {
    // Run the agent using HttpAgent API
    const result = await agent.runAgent(
      {
        messages,
      },
      {
        onEvent: (event) => {
          // Forward all events to the callback
          onEvent(event)
        },
        onError: (error) => {
          console.error('AG-UI Error:', error)
          onEvent({
            type: 'error',
            error: error.message || 'An error occurred',
          })
        },
      }
    )

    // Handle completion if needed
    if (result) {
      console.log('Agent completed', result)
    }
  } catch (error) {
    console.error('AG-UI Error:', error)
    onEvent({
      type: 'error',
      error: error.message || 'An error occurred',
    })
  }
}
