/**
 * Progress tracker component for showing analysis status.
 */

import "./ProgressTracker.css";

interface ProgressTrackerProps {
    isLoading: boolean;
    progress: string;
    error: string | null;
}

export function ProgressTracker({ isLoading, progress, error }: ProgressTrackerProps) {
    if (!isLoading && !error && !progress) {
        return null;
    }

    return (
        <div className="progress-tracker">
            {error && (
                <div className="progress-error">
                    <span className="error-icon">⚠️</span>
                    <span>{error}</span>
                </div>
            )}

            {isLoading && (
                <div className="progress-loading">
                    <div className="progress-spinner"></div>
                    <span>{progress || "Processing..."}</span>
                </div>
            )}

            {!isLoading && !error && progress === "Complete" && (
                <div className="progress-complete">
                    <span className="complete-icon">✓</span>
                    <span>Analysis complete</span>
                </div>
            )}
        </div>
    );
}
