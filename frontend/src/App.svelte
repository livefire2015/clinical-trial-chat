<script>
  import ChatContainer from './components/ChatContainer.svelte'
</script>

<main>
  <div class="app-header">
    <h1>Clinical Trial Analysis Chat</h1>
    <p>AI-powered pharmaceutical clinical trial analysis</p>
  </div>

  <ChatContainer />
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: #f5f7fa;
  }

  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .app-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .app-header h1 {
    color: #1a202c;
    margin: 0 0 0.5rem 0;
  }

  .app-header p {
    color: #718096;
    margin: 0;
  }
</style>
