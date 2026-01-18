/**
 * Dashboard renderer that displays analysis results.
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
import "./DashboardRenderer.css";

interface DashboardRendererProps {
    dashboardSpec: DashboardSpec | null;
}

export function DashboardRenderer({ dashboardSpec }: DashboardRendererProps) {
    if (!dashboardSpec) {
        return null;
    }

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
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2>{dashboardSpec.title}</h2>
                {dashboardSpec.metadata && (
                    <p className="dashboard-metadata">
                        {dashboardSpec.metadata.row_count} rows · {dashboardSpec.metadata.chart_type} chart
                    </p>
                )}
            </div>

            <div className="charts-grid">
                {dashboardSpec.charts.map((chart, index) => (
                    <div key={index} className="chart-wrapper">
                        {renderChart(chart, index)}
                    </div>
                ))}
            </div>

            {dashboardSpec.insight && (
                <div className="dashboard-insight">
                    <div className="insight-icon">💡</div>
                    <div className="insight-content">
                        <h3>Insight</h3>
                        <p>{dashboardSpec.insight}</p>
                    </div>
                </div>
            )}
        </div>
    );
}
