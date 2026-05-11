// Tiny client helper to open the ticker side-sheet from anywhere.
// The drawer component listens for the custom event AND for URL hash
// changes, so deep links like /portfolio#sheet=ACN also work.

export const TICKER_SHEET_EVENT = "open-ticker-sheet";

export function openTickerSheet(ticker: string) {
  if (typeof window === "undefined") return;
  const tk = ticker.toUpperCase().replace(/\.SA$/, "");
  // Push hash so deep-linking works (back button closes the sheet)
  const url = new URL(window.location.href);
  url.hash = `sheet=${tk}`;
  window.history.replaceState({}, "", url.toString());
  window.dispatchEvent(new CustomEvent(TICKER_SHEET_EVENT, { detail: { ticker: tk } }));
}

export function closeTickerSheet() {
  if (typeof window === "undefined") return;
  const url = new URL(window.location.href);
  if (url.hash.startsWith("#sheet=")) {
    url.hash = "";
    window.history.replaceState({}, "", url.toString());
  }
  window.dispatchEvent(new CustomEvent(TICKER_SHEET_EVENT, { detail: { ticker: null } }));
}

export function readTickerFromHash(): string | null {
  if (typeof window === "undefined") return null;
  const m = window.location.hash.match(/^#sheet=([A-Za-z0-9.\-]+)/);
  return m ? m[1].toUpperCase() : null;
}
