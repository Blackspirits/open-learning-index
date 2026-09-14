(() => {
  const storageKey = "oli-theme";
  const root = document.documentElement;
  const darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

  function storedTheme() {
    try {
      const value = localStorage.getItem(storageKey);
      return value === "dark" || value === "light" ? value : null;
    } catch {
      return null;
    }
  }

  function effectiveTheme() {
    return storedTheme() || (darkQuery.matches ? "dark" : "light");
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;

    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#07131a" : "#ffffff");

    const isPt = document.documentElement.lang === "pt-PT";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      const next = theme === "dark" ? "light" : "dark";
      button.setAttribute(
        "aria-label",
        isPt
          ? (next === "dark" ? "Usar tema escuro" : "Usar tema claro")
          : (next === "dark" ? "Use dark theme" : "Use light theme")
      );
      button.setAttribute("title", button.getAttribute("aria-label"));
      const icon = button.querySelector("[data-theme-icon]");
      if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
    });
  }

  function setTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch {
      // Theme persistence is optional.
    }
    applyTheme(theme);
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-theme-toggle]");
    if (!button) return;
    setTheme(effectiveTheme() === "dark" ? "light" : "dark");
  });

  darkQuery.addEventListener?.("change", () => {
    if (!storedTheme()) applyTheme(effectiveTheme());
  });

  document.addEventListener("DOMContentLoaded", () => applyTheme(effectiveTheme()));
  applyTheme(effectiveTheme());
})();
