/**
 * Main BI-Copilot application component.
 */

import { QueryInput } from "./components/QueryInput";
import { ProgressTracker } from "./components/ProgressTracker";
import { DashboardRenderer } from "./components/DashboardRenderer";
import { useAnalysis } from "./hooks/useAnalysis";
import "./App.css";

function App() {
  const { isLoading, error, result, progress, analyze } = useAnalysis();

  const handleQuery = (query: string) => {
    analyze(query);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 BI-Copilot</h1>
        <p className="app-subtitle">GenAI-Powered Data Analysis</p>
      </header>

      <main className="app-main">
        <QueryInput onSubmit={handleQuery} isLoading={isLoading} />

        <ProgressTracker
          isLoading={isLoading}
          progress={progress}
          error={error}
        />

        {result && <DashboardRenderer dashboardSpec={result.dashboard_spec} />}
      </main>

      <footer className="app-footer">
        <p>
          Powered by multi-agent pipeline: Orchestrator → Analysis Planner → SQL Generator → Dashboard Generator
        </p>
      </footer>
    </div>
  );
}

export default App;
