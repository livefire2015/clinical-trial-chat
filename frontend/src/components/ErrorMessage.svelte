<script>
  let { message } = $props()

  function formatErrorMessage(error) {
    // Make error messages more user-friendly
    if (error.includes('No such file or directory')) {
      return 'Database file not found. Please ensure the database is properly configured.'
    }
    return error
  }
</script>

<div class="error-message">
  <div class="error-header">
    <div class="error-icon">⚠️</div>
    <div class="error-title">Error</div>
  </div>
  <div class="error-content">
    {formatErrorMessage(message.content)}
  </div>
</div>

<style>
  .error-message {
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 8px;
    background: #fff5f5;
    border-left: 4px solid #f56565;
  }

  .error-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .error-icon {
    font-size: 1.25rem;
  }

  .error-title {
    font-weight: 600;
    color: #c53030;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .error-content {
    color: #742a2a;
    font-size: 0.875rem;
    line-height: 1.6;
  }
</style>
