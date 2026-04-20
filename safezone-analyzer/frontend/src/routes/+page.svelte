<script lang="ts">
  import { startAnalysis, getAnalysis, getAnalysisTree } from '$lib/api';
  import TreeMap from '$lib/TreeMap.svelte';

  let repoUrl = $state('');
  let analysisId: string | null = $state(null);
  let status: 'idle' | 'analyzing' | 'completed' | 'failed' | 'error' = $state('idle');
  let errorMessage = $state('');
  let analysisData: any = $state(null);
  let fileDetails: any[] = $state([]);
  let selectedFile: any = $state(null);
  let pollingInterval: ReturnType<typeof setInterval> | null = null;

  async function handleStartAnalysis() {
    if (!repoUrl) {
      errorMessage = 'Please enter a repository URL or path.';
      return;

    }

    status = 'analyzing';
    errorMessage = '';
    analysisId = null;
    analysisData = null;
    selectedFile = null;

    try {
      const response = await startAnalysis(repoUrl);
      analysisId = response.analysis_id;
      startPolling(response.analysis_id);
    } catch (err) {
      status = 'error';
      errorMessage = 'Failed to start analysis. Make sure the backend is running.';
      console.error(err);
    }
  }

  function startPolling(id: string) {
    pollingInterval = setInterval(async () => {
      try {
        const data = await getAnalysis(id);
        if (data.status === 'completed') {
          analysisData = data.data;
          status = 'completed';
          stopPolling();
          fetchTree(id);
        } else if (data.status === 'failed') {
          status = 'failed';
          errorMessage = 'Analysis failed on the server.';
          stopPolling();
        }
      } catch (err) {
        status = 'error';
        errorMessage = 'Error polling analysis status.';
        stopPolling();
        console.error(err);
      }
    }, 3000);
  }

  async function fetchTree(id: string) {
    try {
      fileDetails = await getAnalysisTree(id);
    } catch (err) {
      console.error('Error fetching tree:', err);
    }
  }

  function stopPolling() {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
  }

  function handleFileSelect(file: any) {
    selectedFile = file;
  }
</script>

<div class="dashboard">
  <nav class="sidebar">
    <div class="logo">
      <span class="logo-icon">&#9678;</span>
      <span class="logo-text">SafeZone</span>
    </div>
    <div class="nav-section">
      <span class="nav-label">Analysis</span>
      <button class="nav-item active" onclick={() => {}}>
        <span class="nav-icon">&#9635;</span> Treemap
      </button>
    </div>
    {#if analysisData}
      <div class="nav-section">
        <span class="nav-label">Summary</span>
        <div class="summary-stats">
          <div class="stat safe">
            <span class="stat-dot"></span>
            <span>Safe</span>
            <span class="stat-count">{fileDetails.filter(f => f.zone === 'safe').length}</span>
          </div>
          <div class="stat caution">
            <span class="stat-dot"></span>
            <span>Caution</span>
            <span class="stat-count">{fileDetails.filter(f => f.zone === 'caution').length}</span>
          </div>
          <div class="stat restricted">
            <span class="stat-dot"></span>
            <span>Restricted</span>
            <span class="stat-count">{fileDetails.filter(f => f.zone === 'restricted').length}</span>
          </div>
        </div>
      </div>
    {/if}
  </nav>

  <div class="main-area">
    <header>
      <div class="header-top">
        <div>
          <h1>Safe Zone Analyzer</h1>
          <p class="subtitle">Classify repository files into permission zones for AI-assisted editing</p>
        </div>
        {#if status !== 'idle'}
          <div class="status-pill status-{status}">
            {#if status === 'analyzing'}
              <span class="pulse"></span>
            {/if}
            {status.toUpperCase()}
          </div>
        {/if}
      </div>
      <div class="input-group">
        <div class="input-wrapper">
          <span class="input-icon">&#128193;</span>
          <input
            type="text"
            bind:value={repoUrl}
            placeholder="GitHub URL (https://github.com/...) or local path on the server"
            disabled={status === 'analyzing'}
            onkeydown={(e) => e.key === 'Enter' && handleStartAnalysis()}
          />
        </div>
        <button class="analyze-btn" onclick={handleStartAnalysis} disabled={status === 'analyzing'}>
          {#if status === 'analyzing'}
            <span class="spinner"></span> Analyzing...
          {:else}
            Analyze
          {/if}
        </button>
      </div>
      {#if errorMessage}
        <div class="error-banner">{errorMessage}</div>
      {/if}
    </header>

    <main>
      {#if status === 'analyzing' || status === 'completed' || status === 'failed'}
        <div class="content-layout">
          <div class="treemap-section">
            <div class="section-header">
              <h2>File Treemap</h2>
              <span class="file-count">{fileDetails.length} files</span>
            </div>
            <div class="treemap-body">
              {#if analysisData && fileDetails.length > 0}
                <TreeMap data={fileDetails} onFileSelect={handleFileSelect} />
              {:else if status === 'analyzing'}
                <div class="loading-state">
                  <div class="loading-bars">
                    <span></span><span></span><span></span><span></span>
                  </div>
                  <p>Scanning and classifying files...</p>
                </div>
              {/if}
            </div>
          </div>

          <aside class="details-panel" class:has-file={selectedFile}>
            {#if selectedFile}
              <div class="section-header">
                <h2>File Details</h2>
              </div>
              <div class="file-path-display">
                <span class="path-icon">&#128196;</span>
                <code>{selectedFile.path}</code>
              </div>
              <div class="detail-grid">
                <div class="detail-item">
                  <span class="detail-label">Zone</span>
                  <span class="zone-badge zone-{selectedFile.zone}">
                    {selectedFile.zone.toUpperCase()}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Confidence</span>
                  <div class="confidence-bar-wrapper">
                    <div class="confidence-bar">
                      <div
                        class="confidence-fill zone-fill-{selectedFile.zone}"
                        style="width: {selectedFile.confidence * 100}%"
                      ></div>
                    </div>
                    <span class="confidence-value">{(selectedFile.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
              <div class="detail-section">
                <span class="detail-label">Reason</span>
                <p class="reason-text">{selectedFile.reason}</p>
              </div>
              {#if selectedFile.details && selectedFile.details.length > 0}
                <div class="detail-section">
                  <span class="detail-label">Detected Patterns</span>
                  <ul class="pattern-list">
                    {#each selectedFile.details as detail}
                      <li><code>{detail}</code></li>
                    {/each}
                  </ul>
                </div>
              {/if}
            {:else if status === 'completed'}
              <div class="empty-detail">
                <span class="empty-icon">&#128065;</span>
                <p>Click a file in the treemap to inspect it</p>
              </div>
            {/if}
          </aside>
        </div>
      {:else}
        <div class="hero-state">
          <div class="hero-icon">&#128737;</div>
          <h2>Analyze a Repository</h2>
          <p>Enter a repository path above to classify files into safe, caution, and restricted zones.</p>
        </div>
      {/if}
    </main>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: #0f1117;
    color: #e1e4e8;
  }

  .dashboard {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  /* --- Sidebar --- */
  .sidebar {
    width: 220px;
    background: #161b22;
    border-right: 1px solid #21262d;
    display: flex;
    flex-direction: column;
    padding: 1.25rem 0.75rem;
    gap: 1.5rem;
    flex-shrink: 0;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0 0.5rem;
  }
  .logo-icon { font-size: 1.5rem; color: #58a6ff; }
  .logo-text { font-size: 1.1rem; font-weight: 700; letter-spacing: -0.02em; }

  .nav-section { display: flex; flex-direction: column; gap: 0.35rem; }
  .nav-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8b949e;
    padding: 0 0.5rem;
    margin-bottom: 0.25rem;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    background: transparent;
    border: none;
    color: #c9d1d9;
    font-size: 0.85rem;
    cursor: pointer;
    text-align: left;
    width: 100%;
  }
  .nav-item.active { background: rgba(88, 166, 255, 0.1); color: #58a6ff; }
  .nav-icon { font-size: 1rem; }

  .summary-stats { display: flex; flex-direction: column; gap: 0.4rem; padding: 0 0.25rem; }
  .stat {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    padding: 0.35rem 0.5rem;
    border-radius: 0.375rem;
    color: #c9d1d9;
  }
  .stat-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .stat.safe .stat-dot { background: #3fb950; }
  .stat.caution .stat-dot { background: #d29922; }
  .stat.restricted .stat-dot { background: #f85149; }
  .stat-count {
    margin-left: auto;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }

  /* --- Main area --- */
  .main-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  header {
    padding: 1.25rem 1.5rem;
    background: #161b22;
    border-bottom: 1px solid #21262d;
  }
  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  h1 {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f0f3f6;
    letter-spacing: -0.02em;
  }
  .subtitle {
    margin: 0.25rem 0 0;
    font-size: 0.8rem;
    color: #8b949e;
  }

  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    flex-shrink: 0;
  }
  .status-analyzing { background: rgba(88, 166, 255, 0.15); color: #58a6ff; }
  .status-completed { background: rgba(63, 185, 80, 0.15); color: #3fb950; }
  .status-failed, .status-error { background: rgba(248, 81, 73, 0.15); color: #f85149; }

  .pulse {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #58a6ff;
    animation: pulse-anim 1.5s ease-in-out infinite;
  }
  @keyframes pulse-anim {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.5); }
  }

  .input-group { display: flex; gap: 0.5rem; }
  .input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 0.5rem;
    padding: 0 0.75rem;
    transition: border-color 0.2s;
  }
  .input-wrapper:focus-within { border-color: #58a6ff; }
  .input-icon { font-size: 1rem; color: #484f58; margin-right: 0.5rem; }
  input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: #e1e4e8;
    font-size: 0.9rem;
    padding: 0.6rem 0;
    font-family: inherit;
  }
  input::placeholder { color: #484f58; }
  input:disabled { opacity: 0.5; }

  .analyze-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1.25rem;
    background: linear-gradient(135deg, #238636, #2ea043);
    color: #fff;
    border: none;
    border-radius: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
  }
  .analyze-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #2ea043, #3fb950);
    box-shadow: 0 0 12px rgba(46, 160, 67, 0.3);
  }
  .analyze-btn:disabled { opacity: 0.6; cursor: not-allowed; }

  .spinner {
    width: 14px; height: 14px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .error-banner {
    margin-top: 0.75rem;
    padding: 0.5rem 0.75rem;
    background: rgba(248, 81, 73, 0.1);
    border: 1px solid rgba(248, 81, 73, 0.3);
    border-radius: 0.5rem;
    color: #f85149;
    font-size: 0.8rem;
  }

  main {
    flex: 1;
    overflow: hidden;
    padding: 1rem 1.5rem;
  }

  .content-layout {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 1rem;
    height: 100%;
  }

  .treemap-section {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 0.75rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #21262d;
  }
  .section-header h2 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: #f0f3f6;
  }
  .file-count {
    font-size: 0.75rem;
    color: #8b949e;
    background: #21262d;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
  }
  .treemap-body { flex: 1; overflow: hidden; }

  .details-panel {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 0.75rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  .file-path-display {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: #0d1117;
    border-bottom: 1px solid #21262d;
    font-size: 0.8rem;
  }
  .path-icon { font-size: 1rem; }
  .file-path-display code {
    color: #58a6ff;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.78rem;
    word-break: break-all;
  }

  .detail-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  .detail-item { display: flex; flex-direction: column; gap: 0.35rem; }
  .detail-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8b949e;
    font-weight: 500;
  }

  .zone-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    width: fit-content;
  }
  .zone-safe { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.3); }
  .zone-caution { background: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid rgba(210, 153, 34, 0.3); }
  .zone-restricted { background: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid rgba(248, 81, 73, 0.3); }

  .confidence-bar-wrapper {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  .confidence-bar {
    flex: 1;
    height: 6px;
    background: #21262d;
    border-radius: 3px;
    overflow: hidden;
  }
  .confidence-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.4s ease;
  }
  .zone-fill-safe { background: #3fb950; }
  .zone-fill-caution { background: #d29922; }
  .zone-fill-restricted { background: #f85149; }
  .confidence-value {
    font-size: 0.85rem;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    color: #e1e4e8;
    min-width: 2.5rem;
    text-align: right;
  }

  .detail-section {
    padding: 0 1rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .reason-text {
    margin: 0;
    font-size: 0.85rem;
    color: #c9d1d9;
    line-height: 1.5;
  }
  .pattern-list {
    list-style: none;
    padding: 0;
    margin: 0.25rem 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .pattern-list li {
    font-size: 0.8rem;
  }
  .pattern-list code {
    background: #0d1117;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #f0883e;
    border: 1px solid #21262d;
  }

  .empty-detail {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #484f58;
    gap: 0.5rem;
  }
  .empty-icon { font-size: 2rem; opacity: 0.5; }
  .empty-detail p { margin: 0; font-size: 0.85rem; }

  .hero-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: #484f58;
  }
  .hero-icon { font-size: 3.5rem; margin-bottom: 1rem; opacity: 0.4; }
  .hero-state h2 {
    margin: 0 0 0.5rem;
    font-size: 1.25rem;
    color: #8b949e;
    font-weight: 600;
  }
  .hero-state p {
    margin: 0;
    font-size: 0.9rem;
    max-width: 400px;
    line-height: 1.5;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 1rem;
    color: #8b949e;
  }
  .loading-bars {
    display: flex;
    gap: 4px;
    align-items: flex-end;
    height: 30px;
  }
  .loading-bars span {
    width: 4px;
    background: #58a6ff;
    border-radius: 2px;
    animation: loading-bar 1s ease-in-out infinite;
  }
  .loading-bars span:nth-child(1) { height: 10px; animation-delay: 0s; }
  .loading-bars span:nth-child(2) { height: 20px; animation-delay: 0.15s; }
  .loading-bars span:nth-child(3) { height: 15px; animation-delay: 0.3s; }
  .loading-bars span:nth-child(4) { height: 25px; animation-delay: 0.45s; }
  @keyframes loading-bar {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(2); }
  }
  .loading-state p { margin: 0; font-size: 0.85rem; }
</style>
