/**
 * Main BI-Copilot application component - ChatGPT style UI.
 */

import { useState } from "react";
import { QueryInput } from "./components/QueryInput";
import { ChatMessage } from "./components/ChatMessage";
import { Sidebar } from "./components/Sidebar";
import { useAnalysis } from "./hooks/useAnalysis";
import type { AnalyzeResponse } from "./lib/types";
import "./App.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  result?: AnalyzeResponse | null;
  error?: string | null;
  isLoading?: boolean;
}

function App() {
  const { isLoading, error, result, analyze, reset } = useAnalysis();
  const [messages, setMessages] = useState<Message[]>([]);

  const handleQuery = (query: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
    };
    setMessages((prev) => [...prev, userMessage]);

    // Add loading message
    const loadingMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "",
      isLoading: true,
    };
    setMessages((prev) => [...prev, loadingMessage]);

    // Analyze
    analyze(query);
  };

  // Update messages when result arrives
  if (result && messages.length > 0) {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage.isLoading) {
      const updatedMessages = messages.map((msg) =>
        msg.id === lastMessage.id
          ? {
              ...msg,
              isLoading: false,
              content: "Analysis complete",
              result,
            }
          : msg
      );
      setMessages(updatedMessages);
    }
  }

  // Handle errors
  if (error && messages.length > 0) {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage.isLoading) {
      const updatedMessages = messages.map((msg) =>
        msg.id === lastMessage.id
          ? {
              ...msg,
              isLoading: false,
              content: "",
              error,
            }
          : msg
      );
      setMessages(updatedMessages);
    }
  }

  const handleNewChat = () => {
    setMessages([]);
    reset();
  };

  return (
    <div className="app">
      <Sidebar onNewChat={handleNewChat} />
      <div className="main-container">
        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-content">
                <h1>Welcome to BI-Copilot</h1>
                <p>Ask questions about your data and get instant insights</p>
              </div>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role}
                  content={msg.content}
                  dashboardSpec={msg.result?.dashboard_spec}
                  isLoading={msg.isLoading}
                  error={msg.error}
                />
              ))}
            </div>
          )}
        </div>
        <QueryInput onSubmit={handleQuery} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default App;
