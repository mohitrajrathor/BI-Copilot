/**
 * Chat message component for displaying conversation bubbles.
 */

import type { DashboardSpec } from "../lib/types";
import {
  KPICard,
  LineChartComponent,
  BarChartComponent,
  PieChartComponent,
  ScatterChartComponent,
  DataTable,
} from "./ChartComponents";
import "./ChatMessage.css";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  dashboardSpec?: DashboardSpec | null;
  isLoading?: boolean;
  error?: string | null;
}

export function ChatMessage({
  role,
  content,
  dashboardSpec,
  isLoading,
  error,
}: ChatMessageProps) {
  const renderChart = (chart: any, index: number) => {
    switch (chart.type) {
      case "kpi":
        return <KPICard key={index} config={chart} />;
      case "line":
        return <LineChartComponent key={index} config={chart} />;
      case "bar":
        return <BarChartComponent key={index} config={chart} />;
      case "pie":
        return <PieChartComponent key={index} config={chart} />;
      case "scatter":
        return <ScatterChartComponent key={index} config={chart} />;
      case "table":
        return <DataTable key={index} config={chart} />;
      default:
        return <DataTable key={index} config={chart} />;
    }
  };

  return (
    <div className={`chat-message chat-message-${role}`}>
      <div className="message-content">
        {error && (
          <div className="message-error">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {!error && content && (
          <div className="message-text">{content}</div>
        )}

        {isLoading && (
          <div className="message-loading">
            <div className="loading-spinner"></div>
            <span>Analyzing...</span>
          </div>
        )}

        {dashboardSpec && !isLoading && (
          <div className="dashboard-result">
            <h3 className="result-title">{dashboardSpec.title}</h3>
            <div className="charts-container">
              {dashboardSpec.charts.map((chart, index) => (
                <div key={index} className="chart-card">
                  {renderChart(chart, index)}
                </div>
              ))}
            </div>
            {dashboardSpec.insight && (
              <div className="result-insight">{dashboardSpec.insight}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
