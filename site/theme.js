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
      if (icon) {
        icon.dataset.icon = theme === "dark" ? "sun" : "moon";
        window.oliHydrateIcons?.(button);
      }
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

(() => {
  const menu = document.querySelector(".mobile-nav");
  const summary = menu?.querySelector("summary");
  function closeMenu(returnFocus = false) {
    if (!menu?.open) return;
    menu.open = false;
    if (returnFocus) summary.focus();
  }
  document.addEventListener("click", event => {
    if (event.target.closest(".mobile-nav nav a")) closeMenu();
    else if (menu && !menu.contains(event.target)) closeMenu();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu(true);
  });
  document.addEventListener("focusin", event => {
    if (menu && !menu.contains(event.target)) closeMenu();
  });
  for (const link of document.querySelectorAll(".main-nav a, .mobile-nav nav a")) {
    const target = new URL(link.href);
    if (!target.hash && target.pathname === location.pathname) link.setAttribute("aria-current", "page");
  }
  const tabs = [...document.querySelectorAll(".course-tabs a")];
  const sections = tabs.map(link => document.querySelector(link.hash)).filter(Boolean);
  if (!sections.length) return;
  function markSection(id) {
    for (const link of tabs) {
      if (link.hash === `#${id}`) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }
  tabs.forEach(link => link.addEventListener("click", () => markSection(link.hash.slice(1))));
  let scheduled = false;
  function updateSection() {
    scheduled = false;
    const offset = document.querySelector(".topbar").getBoundingClientRect().height + document.querySelector(".course-tabs").getBoundingClientRect().height + 35;
    let current = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= offset) current = section;
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 3) current = sections.at(-1);
    markSection(current.id);
  }
  document.addEventListener("scroll", () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateSection); }
  }, { passive: true });
  window.addEventListener("resize", updateSection);
  updateSection();
})();
