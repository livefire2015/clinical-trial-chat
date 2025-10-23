<script>
  // Will implement AG-UI client integration here
  let messages = []
</script>

<div class="chat-container">
  <div class="chat-messages">
    {#if messages.length === 0}
      <div class="empty-state">
        <p>Start a conversation about clinical trial data</p>
      </div>
    {/if}
  </div>

  <div class="chat-input">
    <input
      type="text"
      placeholder="Ask about clinical trial statistics, compliance, or data..."
    />
    <button>Send</button>
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

  .chat-input button:hover {
    background: #3182ce;
  }
</style>
