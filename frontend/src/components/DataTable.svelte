<script>
  let { columns = [], rows = [] } = $props()
</script>

{#if columns.length > 0 && rows.length > 0}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          {#each columns as column}
            <th>{column}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each rows as row}
          <tr>
            {#each row as cell}
              <td>{cell}</td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
    <div class="table-footer">
      <span class="row-count">{rows.length} rows</span>
    </div>
  </div>
{/if}

<style>
  .table-container {
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  thead {
    background: #f7fafc;
  }

  th {
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 600;
    color: #2d3748;
    border-bottom: 2px solid #e2e8f0;
  }

  td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e2e8f0;
    color: #4a5568;
  }

  tbody tr:hover {
    background: #f7fafc;
  }

  tbody tr:last-child td {
    border-bottom: none;
  }

  .table-footer {
    padding: 0.5rem 1rem;
    background: #f7fafc;
    border-top: 1px solid #e2e8f0;
  }

  .row-count {
    font-size: 0.75rem;
    color: #718096;
  }
</style>
