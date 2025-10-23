<script>
  let { stats } = $props()
</script>

{#if stats}
  <div class="stats-card">
    <h4>Statistical Summary</h4>
    <div class="stats-grid">
      {#if stats.count !== undefined}
        <div class="stat-item">
          <span class="stat-label">Count</span>
          <span class="stat-value">{stats.count}</span>
        </div>
      {/if}
      {#if stats.mean !== undefined}
        <div class="stat-item">
          <span class="stat-label">Mean</span>
          <span class="stat-value">{stats.mean.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.median !== undefined}
        <div class="stat-item">
          <span class="stat-label">Median</span>
          <span class="stat-value">{stats.median.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.std !== undefined}
        <div class="stat-item">
          <span class="stat-label">Std Dev</span>
          <span class="stat-value">{stats.std.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.min !== undefined}
        <div class="stat-item">
          <span class="stat-label">Min</span>
          <span class="stat-value">{stats.min.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.max !== undefined}
        <div class="stat-item">
          <span class="stat-label">Max</span>
          <span class="stat-value">{stats.max.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.q25 !== undefined}
        <div class="stat-item">
          <span class="stat-label">Q1 (25%)</span>
          <span class="stat-value">{stats.q25.toFixed(2)}</span>
        </div>
      {/if}
      {#if stats.q75 !== undefined}
        <div class="stat-item">
          <span class="stat-label">Q3 (75%)</span>
          <span class="stat-value">{stats.q75.toFixed(2)}</span>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .stats-card {
    margin: 1rem 0;
    padding: 1rem;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
  }

  h4 {
    margin: 0 0 1rem 0;
    font-size: 0.875rem;
    font-weight: 600;
    color: #2d3748;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-label {
    font-size: 0.75rem;
    color: #718096;
    font-weight: 500;
  }

  .stat-value {
    font-size: 1.25rem;
    color: #2d3748;
    font-weight: 600;
  }
</style>
