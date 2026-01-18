/**
 * Query input component - Chat composer style at bottom.
 */

import { useRef, useEffect, useState } from "react";
import "./QueryInput.css";

interface QueryInputProps {
    onSubmit: (query: string) => void;
    isLoading: boolean;
}

export function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
    const [query, setQuery] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // Auto-expand textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            const scrollHeight = textareaRef.current.scrollHeight;
            textareaRef.current.style.height = Math.min(scrollHeight, 120) + "px";
        }
    }, [query]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim() && !isLoading) {
            onSubmit(query.trim());
            setQuery("");
            if (textareaRef.current) {
                textareaRef.current.style.height = "auto";
            }
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
            handleSubmit(e as any);
        }
    };

    return (
        <div className="query-input-container">
            <form onSubmit={handleSubmit} className="query-form">
                <textarea
                    ref={textareaRef}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question about your data... (Ctrl+Enter to send)"
                    className="query-textarea"
                    disabled={isLoading}
                    rows={1}
                />
                <button
                    type="submit"
                    className="submit-button"
                    disabled={isLoading || !query.trim()}
                    title="Send message"
                >
                    {isLoading ? (
                        <span className="spinner-icon">⟳</span>
                    ) : (
                        <span className="send-icon">→</span>
                    )}
                </button>
            </form>
        </div>
    );
}
