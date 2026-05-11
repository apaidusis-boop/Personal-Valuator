/**
 * Inline script injected in <head> to set data-theme BEFORE first paint.
 * This avoids the FOUC (flash of unstyled colour) that would happen if
 * we waited for hydration to apply the saved theme.
 *
 * Read order: localStorage("mc-theme") → fallback "dark".
 */
const SCRIPT = `
(function(){
  try {
    var stored = localStorage.getItem("mc-theme");
    var theme = (stored === "light" || stored === "dark") ? stored : "dark";
    document.documentElement.setAttribute("data-theme", theme);
  } catch (e) {
    document.documentElement.setAttribute("data-theme", "dark");
  }
})();
`.trim();

export default function ThemeInit() {
  // suppressHydrationWarning: browser extensions (anti-fingerprint, dark-mode forcers)
  // routinely splice elements into <head> before React hydrates. The script content
  // is static, so a mismatch here is always extension noise, not a real bug.
  return <script suppressHydrationWarning dangerouslySetInnerHTML={{ __html: SCRIPT }} />;
}
