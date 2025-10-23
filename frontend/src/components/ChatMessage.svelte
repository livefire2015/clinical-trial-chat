<script>
  let { message } = $props()
</script>

<div class="message {message.role}">
  <div class="message-header">
    <span class="role-badge">
      {message.role === 'user' ? 'You' : 'AI Assistant'}
    </span>
    {#if message.streaming}
      <span class="streaming-indicator">●</span>
    {/if}
  </div>
  <div class="message-content">
    {message.content}
  </div>
</div>

<style>
  .message {
    margin-bottom: 1.5rem;
    padding: 1rem;
    border-radius: 8px;
  }

  .message.user {
    background: #ebf8ff;
    margin-left: 2rem;
  }

  .message.assistant {
    background: #f7fafc;
    margin-right: 2rem;
  }

  .message-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .role-badge {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .message.user .role-badge {
    color: #2c5282;
  }

  .message.assistant .role-badge {
    color: #2d3748;
  }

  .streaming-indicator {
    color: #48bb78;
    font-size: 0.5rem;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  .message-content {
    color: #2d3748;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
</style>
