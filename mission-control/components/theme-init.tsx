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
  return <script dangerouslySetInnerHTML={{ __html: SCRIPT }} />;
}
