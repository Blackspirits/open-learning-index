(() => {
  const paths = {
    brand: '<path d="M12 4v16M8 8l4-4 4 4"/><path d="M7 20h10"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/>',
    moon: '<path d="M20 15.2A8.5 8.5 0 0 1 8.8 4a8.5 8.5 0 1 0 11.2 11.2Z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    curated: '<path d="m12 3 2.4 4.8L20 9l-4 3.9.9 5.6L12 16l-4.9 2.5.9-5.6L4 9l5.6-1.2Z"/>',
    evidence: '<rect x="5" y="4" width="14" height="16" rx="2"/><path d="M8 9h8M8 13h6M8 17h4"/>',
    clock: '<circle cx="12" cy="12" r="8"/><path d="M12 8v5l3 2"/>',
    globe: '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.2 2.3 3.2 5 3.2 8s-1 5.7-3.2 8M12 4c-2.2 2.3-3.2 5-3.2 8s1 5.7 3.2 8"/>',
    code: '<path d="m9 8-4 4 4 4M15 8l4 4-4 4M13 5l-2 14"/>',
    business: '<rect x="4" y="7" width="16" height="12" rx="2"/><path d="M9 7V5h6v2M4 12h16M10 12v2h4v-2"/>',
    math: '<path d="M17 5H7l5 7-5 7h10"/>',
    health: '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>',
    languages: '<path d="M5 5h8v10H8l-3 3Z"/><path d="M11 9h8v9h-3l-3 2v-5"/>',
    ai: '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6M9 13h6M9 17h3M12 2v3M12 19v3M2 12h3M19 12h3"/>',
    shield: '<path d="M12 3 19 6v5c0 4.7-3 7.6-7 10-4-2.4-7-5.3-7-10V6Z"/><path d="m9 12 2 2 4-4"/>',
    palette: '<path d="M12 4a8 8 0 1 0 0 16h1.2a1.8 1.8 0 0 0 1.1-3.2c-.5-.4-.2-1.3.5-1.3H17A3 3 0 0 0 20 12a8 8 0 0 0-8-8Z"/><circle cx="8" cy="10" r="1"/><circle cx="11" cy="7" r="1"/><circle cx="15" cy="8" r="1"/>',
    education: '<path d="m3 9 9-5 9 5-9 5Z"/><path d="M7 12v4c3 2 7 2 10 0v-4"/>',
    engineering: '<path d="M9 4h6l1 3 3 1v6l-3 1-1 3H9l-1-3-3-1V8l3-1Z"/><circle cx="12" cy="11" r="2.5"/>',
    finance: '<path d="M4 9h16M6 9v8M10 9v8M14 9v8M18 9v8M4 18h16M12 4 4 8h16Z"/>',
    history: '<path d="M5 5h14v14H5Z"/><path d="M8 9h8M8 12h8M8 15h5"/>',
    humanities: '<path d="M6 4h12v16H6Z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    law: '<path d="M12 4v16M7 7h10M6 7l-3 6h6Zm12 0-3 6h6Z"/>',
    marketing: '<path d="M4 13h4l8 4V7l-8 4H4Z"/><path d="M8 13v5"/>',
    science: '<path d="M9 3h6M10 3v6l-5 9h14l-5-9V3"/><path d="M8 14h8"/>',
    leadership: '<circle cx="8" cy="8" r="3"/><circle cx="17" cy="9" r="2"/><path d="M3 19c.7-4 3-6 5-6s4.3 2 5 6M14 18c.4-2.7 1.9-4.5 4-4.5 1.6 0 2.8 1.1 3.5 3"/>',
    brain: '<path d="M9 5a3 3 0 0 0-5 2.2A3 3 0 0 0 5 13a3 3 0 0 0 4 4V5Zm6 0a3 3 0 0 1 5 2.2A3 3 0 0 1 19 13a3 3 0 0 1-4 4V5Z"/><path d="M9 9H7M9 13H6M15 9h2M15 13h3"/>',
    writing: '<path d="m5 19 4-.8L19 8.2 15.8 5 5.8 15Z"/><path d="m14.5 6.3 3.2 3.2M4 20h16"/>',
    status: '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/>',
    provider: '<path d="M4 20h16M6 20V8l6-4 6 4v12M9 11h2M13 11h2M9 15h2M13 15h2"/>',
    level: '<path d="M5 18V9M12 18V5M19 18v-6"/>',
    access: '<path d="M7 11V8a5 5 0 0 1 10 0v3M6 11h12v9H6Z"/>',
    arrow: '<path d="M5 12h14M14 7l5 5-5 5"/>'
  };

  const aliases = {
    "computer-science": "code",
    "business-entrepreneurship": "business",
    "math-statistics": "math",
    "health-medicine": "health",
    "languages": "languages",
    "ai-data": "ai",
    "cybersecurity-it": "shield",
    "arts-design": "palette",
    "education-teaching": "education",
    "engineering-electronics": "engineering",
    "finance-economics": "finance",
    "history-culture": "history",
    "humanities-philosophy": "humanities",
    "law-public-policy": "law",
    "marketing-sales": "marketing",
    "natural-sciences": "science",
    "project-product-leadership": "leadership",
    "psychology-behavior": "brain",
    "writing-communication": "writing"
  };

  function markup(name, className = "") {
    const key = aliases[name] || name;
    const body = paths[key] || paths.curated;
    const cls = ["ui-icon", className].filter(Boolean).join(" ");
    return '<svg class="' + cls + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + body + '</svg>';
  }

  function hydrate(root = document) {
    root.querySelectorAll("[data-icon]").forEach((node) => {
      const name = node.dataset.icon;
      if (!name) return;
      node.innerHTML = markup(name, node.dataset.iconClass || "");
    });
  }

  window.oliIcon = markup;
  window.oliHydrateIcons = hydrate;
  document.addEventListener("DOMContentLoaded", () => hydrate(document));
})();
