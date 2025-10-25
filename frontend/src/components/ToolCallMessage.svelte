<script>
  let { message } = $props()
  let expanded = $state(false)

  function toggleExpanded() {
    expanded = !expanded
  }

  function formatToolName(name) {
    // Convert tool names like 'query_database' to 'Querying database'
    return name
      .split('_')
      .map((word, i) => (i === 0 ? word.charAt(0).toUpperCase() + word.slice(1) : word))
      .join(' ') + '...'
  }

  function formatArgs(args) {
    if (!args) return ''
    try {
      // Try to parse as JSON and format nicely
      const parsed = typeof args === 'string' ? JSON.parse(args) : args
      return JSON.stringify(parsed, null, 2)
    } catch {
      // If not valid JSON, return as-is
      return args
    }
  }
</script>

<div class="tool-message">
  <div class="tool-header">
    <div class="tool-icon">🔧</div>
    <div class="tool-info">
      <div class="tool-name">
        {formatToolName(message.toolName)}
      </div>
      {#if message.status === 'loading'}
        <div class="tool-status loading">Running...</div>
      {:else if message.status === 'complete'}
        <div class="tool-status complete">Complete</div>
      {:else if message.status === 'error'}
        <div class="tool-status error">Failed</div>
      {/if}
    </div>
    {#if message.args}
      <button class="expand-button" onclick={toggleExpanded}>
        {expanded ? '▼' : '▶'}
      </button>
    {/if}
  </div>

  {#if expanded && message.args}
    <div class="tool-details">
      <div class="detail-label">Arguments:</div>
      <pre class="detail-content">{formatArgs(message.args)}</pre>
    </div>
  {/if}

  {#if message.result}
    <div class="tool-result">
      <div class="detail-label">Result:</div>
      <div class="result-preview">{String(message.result).substring(0, 200)}{String(message.result).length > 200 ? '...' : ''}</div>
    </div>
  {/if}
</div>

<style>
  .tool-message {
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    background: #edf2f7;
    border-left: 4px solid #4299e1;
  }

  .tool-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .tool-icon {
    font-size: 1.25rem;
  }

  .tool-info {
    flex: 1;
  }

  .tool-name {
    font-weight: 600;
    color: #2d3748;
    font-size: 0.875rem;
  }

  .tool-status {
    font-size: 0.75rem;
    margin-top: 0.25rem;
  }

  .tool-status.loading {
    color: #4299e1;
  }

  .tool-status.complete {
    color: #48bb78;
  }

  .tool-status.error {
    color: #f56565;
  }

  .expand-button {
    background: none;
    border: none;
    color: #718096;
    cursor: pointer;
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }

  .expand-button:hover {
    color: #2d3748;
  }

  .tool-details {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid #cbd5e0;
  }

  .detail-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #4a5568;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .detail-content {
    background: #ffffff;
    padding: 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    color: #2d3748;
    overflow-x: auto;
    margin: 0;
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  }

  .tool-result {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid #cbd5e0;
  }

  .result-preview {
    background: #f7fafc;
    padding: 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    color: #2d3748;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
</style>
