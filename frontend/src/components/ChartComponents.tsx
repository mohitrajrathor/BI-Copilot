/**
 * Chart components using Recharts library.
 */

import {
    LineChart,
    Line,
    BarChart,
    Bar,
    PieChart,
    Pie,
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Cell,
} from "recharts";
import type { ChartConfig } from "../lib/types";
import "./ChartComponents.css";

const COLORS = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"];

interface ChartProps {
    config: ChartConfig;
}

export function KPICard({ config }: ChartProps) {
    if (!config.metric) return null;

    return (
        <div className="kpi-card">
            <div className="kpi-label">{config.metric.label}</div>
            <div className="kpi-value">{config.metric.value.toLocaleString()}</div>
        </div>
    );
}

export function LineChartComponent({ config }: ChartProps) {
    const yAxisKeys = Array.isArray(config.yAxis) ? config.yAxis : [config.yAxis];

    return (
        <ResponsiveContainer width="100%" height={400}>
            <LineChart data={config.data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={config.xAxis} />
                <YAxis />
                <Tooltip />
                <Legend />
                {yAxisKeys.map((key, index) => (
                    <Line
                        key={key}
                        type="monotone"
                        dataKey={key}
                        stroke={COLORS[index % COLORS.length]}
                        strokeWidth={2}
                    />
                ))}
            </LineChart>
        </ResponsiveContainer>
    );
}

export function BarChartComponent({ config }: ChartProps) {
    // Handle yAxis as string or array, use first element if array
    const yAxisKey = Array.isArray(config.yAxis) ? config.yAxis[0] : config.yAxis;
    
    return (
        <ResponsiveContainer width="100%" height={400}>
            <BarChart data={config.data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={config.xAxis} />
                <YAxis />
                <Tooltip />
                <Legend />
                {yAxisKey && <Bar dataKey={yAxisKey} fill={COLORS[0]} />}
            </BarChart>
        </ResponsiveContainer>
    );
}

export function PieChartComponent({ config }: ChartProps) {
    const valueColumn = config.valueColumn || "value";
    const labelColumn = config.labelColumn || "label";
    
    return (
        <ResponsiveContainer width="100%" height={400}>
            <PieChart>
                <Pie
                    data={config.data}
                    dataKey={valueColumn}
                    nameKey={labelColumn}
                    cx="50%"
                    cy="50%"
                    outerRadius={120}
                    label
                >
                    {config.data.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
}

export function ScatterChartComponent({ config }: ChartProps) {
    // Handle yAxis as string or array, use first element if array
    const yAxisKey = Array.isArray(config.yAxis) ? config.yAxis[0] : config.yAxis;
    const xAxisKey = config.xAxis || "x";
    const yAxisName = yAxisKey || "y";
    
    return (
        <ResponsiveContainer width="100%" height={400}>
            <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={xAxisKey} name={xAxisKey} />
                <YAxis dataKey={yAxisKey} name={yAxisName} />
                <Tooltip cursor={{ strokeDasharray: "3 3" }} />
                <Legend />
                <Scatter name="Data" data={config.data} fill={COLORS[0]} />
            </ScatterChart>
        </ResponsiveContainer>
    );
}

export function DataTable({ config }: ChartProps) {
    if (!config.data.length) {
        return <div className="no-data">No data available</div>;
    }

    return (
        <div className="data-table-container">
            <table className="data-table">
                <thead>
                    <tr>
                        {config.columns.map((col) => (
                            <th key={col}>{col}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {config.data.map((row, index) => (
                        <tr key={index}>
                            {config.columns.map((col) => (
                                <td key={col}>{row[col]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
