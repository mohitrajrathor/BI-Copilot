/**
 * Custom hook for analysis flow management.
 */

import { useState } from "react";
import { analyzeQuery } from "../lib/api";
import type { AnalyzeResponse } from "../lib/types";

export interface AnalysisState {
    isLoading: boolean;
    error: string | null;
    result: AnalyzeResponse | null;
    progress: string;
}

export function useAnalysis() {
    const [state, setState] = useState<AnalysisState>({
        isLoading: false,
        error: null,
        result: null,
        progress: "",
    });

    const analyze = async (query: string) => {
        setState({
            isLoading: true,
            error: null,
            result: null,
            progress: "Classifying intent...",
        });

        try {
            // Start analysis
            setState(prev => ({ ...prev, progress: "Creating analysis plan..." }));

            const result = await analyzeQuery(query);

            // Update with result
            setState({
                isLoading: false,
                error: null,
                result,
                progress: "Complete",
            });
        } catch (err: any) {
            setState({
                isLoading: false,
                error: err.response?.data?.detail || err.message || "Analysis failed",
                result: null,
                progress: "",
            });
        }
    };

    const reset = () => {
        setState({
            isLoading: false,
            error: null,
            result: null,
            progress: "",
        });
    };

    return {
        ...state,
        analyze,
        reset,
    };
}
