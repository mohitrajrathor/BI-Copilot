/**
 * Sidebar component for navigation and app controls.
 */

import { useState } from "react";
import "./Sidebar.css";

interface SidebarProps {
  onNewChat: () => void;
}

export function Sidebar({ onNewChat }: SidebarProps) {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.setAttribute(
      "data-theme",
      !isDarkMode ? "dark" : "light"
    );
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">BI-Copilot</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button className="nav-button nav-button-primary" onClick={onNewChat}>
          <span className="nav-icon">+</span>
          New Chat
        </button>
      </nav>

      <div className="sidebar-footer">
        <button
          className="sidebar-control"
          onClick={toggleDarkMode}
          title="Toggle dark mode"
        >
          <span className="control-icon">{isDarkMode ? "☀️" : "🌙"}</span>
        </button>
      </div>
    </aside>
  );
}
