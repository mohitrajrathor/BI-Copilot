/**
 * Query input component for natural language queries.
 */

import { useState } from "react";
import "./QueryInput.css";

interface QueryInputProps {
    onSubmit: (query: string) => void;
    isLoading: boolean;
}

const EXAMPLE_QUERIES = [
    "Show me total sales by region",
    "What are the top 10 customers by revenue?",
    "Plot monthly revenue trends",
    "Compare product categories by sales",
];

export function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
    const [query, setQuery] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim() && !isLoading) {
            onSubmit(query.trim());
        }
    };

    const handleExampleClick = (exampleQuery: string) => {
        setQuery(exampleQuery);
    };

    return (
        <div className="query-input-container">
            <h2>Ask a Question About Your Data</h2>

            <form onSubmit={handleSubmit} className="query-form">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g., Show me sales trends over time..."
                    className="query-input"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    className="submit-button"
                    disabled={isLoading || !query.trim()}
                >
                    {isLoading ? "Analyzing..." : "Analyze"}
                </button>
            </form>

            <div className="example-queries">
                <p className="example-label">Example queries:</p>
                <div className="example-buttons">
                    {EXAMPLE_QUERIES.map((example, index) => (
                        <button
                            key={index}
                            onClick={() => handleExampleClick(example)}
                            className="example-button"
                            disabled={isLoading}
                        >
                            {example}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
