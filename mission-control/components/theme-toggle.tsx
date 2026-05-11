"use client";

import { useEffect, useState } from "react";

type Theme = "light" | "dark";

const STORAGE_KEY = "mc-theme";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme | null>(null);

  // Sync from DOM after hydration
  useEffect(() => {
    const current =
      (document.documentElement.getAttribute("data-theme") as Theme | null) ||
      "dark";
    setTheme(current);
  }, []);

  const toggle = () => {
    const next: Theme = theme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* ignore */
    }
    setTheme(next);
  };

  // Avoid hydration mismatch — render placeholder until client mount
  if (theme === null) {
    return (
      <button
        type="button"
        aria-label="Toggle theme"
        className="text-[var(--text-tertiary)] type-mono-sm"
        style={{ width: 56 }}
      >
        &nbsp;
      </button>
    );
  }

  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      title={isDark ? "Switch to light" : "Switch to dark"}
      className="type-mono-sm flex items-center gap-1.5 px-2 py-1 border border-[var(--border-subtle)] hover:border-[var(--border-strong)] hover:text-[var(--text-primary)] text-[var(--text-tertiary)] transition-colors"
    >
      <span aria-hidden>{isDark ? "○" : "●"}</span>
      <span>{isDark ? "light" : "dark"}</span>
    </button>
  );
}
