const state = {
  courses: [],
  meta: null,
  visibleLimit: 18,
  viewMode: "grid",
};

const rootPath = document.body.dataset.root || "./";
const pageType = document.body.dataset.page || "catalogue";
const pageLocale = "fr";

const categoryNames = {
  "ai-data": "IA et données",
  "arts-design": "Arts et design",
  "business-entrepreneurship": "Entreprise et entrepreneuriat",
  "computer-science": "Informatique et logiciels",
  "cybersecurity-it": "Cybersécurité et IT",
  "education-teaching": "Éducation et enseignement",
  "engineering-electronics": "Ingénierie et électronique",
  "finance-economics": "Finance et économie",
  "health-medicine": "Santé et médecine",
  "history-culture": "Histoire et culture",
  "humanities-philosophy": "Sciences humaines et philosophie",
  languages: "Langues",
  "law-public-policy": "Droit et politiques publiques",
  "marketing-sales": "Marketing et vente",
  "math-statistics": "Mathématiques et statistiques",
  "natural-sciences": "Sciences naturelles",
  "project-product-leadership": "Projet, produit et leadership",
  "psychology-behavior": "Psychologie et comportement",
  "writing-communication": "Écriture et communication",
};

const categoryIcons = {
  "computer-science": "code",
  "business-entrepreneurship": "business",
  "math-statistics": "math",
  "health-medicine": "health",
  languages: "languages",
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
  "writing-communication": "writing",
};

const levelNames = {
  beginner: "Débutant",
  beginner_to_intermediate: "Débutant à intermédiaire",
  beginner_to_advanced: "Débutant à avancé",
  intermediate: "Intermédiaire",
  intermediate_to_advanced: "Intermédiaire à avancé",
  advanced: "Avancé",
  undergraduate: "Licence",
  graduate: "Études supérieures",
};

const levelOrder = [
  "beginner",
  "beginner_to_intermediate",
  "intermediate",
  "intermediate_to_advanced",
  "advanced",
  "undergraduate",
  "graduate",
  "beginner_to_advanced",
];

const languageNames = {
  ar: "arabe", az: "azéri", bg: "bulgare", cs: "tchèque", de: "allemand",
  en: "anglais", es: "espagnol", fr: "français", hu: "hongrois",
  hy: "arménien", it: "italien", ja: "japonais", ka: "géorgien",
  ko: "coréen", nl: "néerlandais", pl: "polonais",
  pt: "portugais (variante non précisée)",
  "pt-BR": "portugais (Brésil)", "pt-PT": "portugais (Portugal)",
  ro: "roumain", ru: "russe", sk: "slovaque", tr: "turc",
  uk: "ukrainien", vi: "vietnamien", zh: "chinois",
};

const accessNames = {
  F0: "Cours et attestation gratuits",
  F1: "Parcours complet avec évaluation",
  F2: "Contenu pédagogique complet gratuit",
};

const copy = {
  recommendation: "Recommandation",
  quality: "Qualité",
  verified: "Vérifié",
  archived: "Archivé",
  remove: "Supprimer",
  level: "Niveau",
  progression: "Progression",
  broad: "Parcours étendu",
  shortcut: "Raccourci",
  beginnerFriendly: "Adapté aux débutants",
  course: "cours",
  courses: "cours",
  showMore: "Afficher plus",
  loadError: "Impossible de charger le catalogue.",
};

function route(path) {
  return `${rootPath}${path}`;
}

function coursePath(courseId) {
  return `fr/courses/${encodeURIComponent(courseId)}/`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function normalize(value) {
  return (value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function tokenize(value) {
  return normalize(value).match(/[a-z0-9+#.]+/g) || [];
}

function labelLanguage(code) {
  return languageNames[code] || code;
}

function labelCategory(course) {
  return categoryNames[course.category] || course.category_name;
}

function labelLevel(value) {
  return levelNames[value] || String(value || "").split("_").join(" ");
}

function presentationFor(course) {
  return course.presentations?.fr || null;
}

function courseTitle(course) {
  return presentationFor(course)?.title || course.title;
}

function courseRationale(course) {
  return presentationFor(course)?.description || course.why_recommended;
}

function formatReviewMonth(value) {
  const date = new Date(`${value}T00:00:00Z`);
  return new Intl.DateTimeFormat("fr", {
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

function renderCatalogueCard(course, className = "catalogue-card") {
  const archived = course.status === "active_archive"
    ? `<span class="mini-tag tag-archive">${copy.archived}</span>`
    : "";
  const recScore = new Intl.NumberFormat("fr", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(course.recommendation_score);
  const qualityScore = new Intl.NumberFormat("fr", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(course.quality_score);
  const access = accessNames[course.access_short] || course.access_label;
  return `
    <article class="${className}">
      <div class="card-body">
        <div class="card-heading">
          <p class="provider">${escapeHtml(course.provider)}</p>
          <h3><a href="${route(coursePath(course.id))}">${escapeHtml(courseTitle(course))}</a></h3>
        </div>
        <div class="card-score-row">
          <span class="card-score card-score-primary" aria-label="${copy.recommendation} ${recScore} / 10"><strong>${recScore}</strong><small>${copy.recommendation}</small></span>
          <span class="card-score" aria-label="${copy.quality} ${qualityScore} / 10"><strong>${qualityScore}</strong><small>${copy.quality}</small></span>
          <span class="mini-tag tag-tier">${escapeHtml(course.quality_tier)}</span>
        </div>
        <p class="card-rationale">${escapeHtml(courseRationale(course))}</p>
        <div class="mini-tags">
          <span class="mini-tag tag-category">${escapeHtml(labelCategory(course))}</span>
          <span class="mini-tag">En ${escapeHtml(labelLanguage(course.primary_language))}</span>
          <span class="mini-tag">${escapeHtml(labelLevel(course.level))}</span>
          ${archived}
        </div>
        <div class="card-footer">
          <div class="access-line"><span data-icon="access" aria-hidden="true"></span><span>${escapeHtml(access)}</span></div>
          <span class="verified-line">${copy.verified} ${escapeHtml(formatReviewMonth(course.last_verified))}</span>
        </div>
      </div>
    </article>
  `;
}

function renderHomeCategory(id, name, count) {
  const icon = categoryIcons[id] || "curated";
  return `
    <a class="category-tile" href="${route(`fr/categories/${encodeURIComponent(id)}/`)}">
      <span class="category-icon icon-${escapeHtml(id)}" data-icon="${escapeHtml(icon)}" aria-hidden="true"></span>
      <strong>${escapeHtml(name)}</strong>
      <small>${count} ${copy.courses}</small>
    </a>`;
}

function renderHome() {
  document.querySelector("#stat-courses").textContent = state.meta.published_count;
  document.querySelector("#stat-categories").textContent = state.meta.category_count;
  document.querySelector("#stat-languages").textContent = state.meta.language_count ?? Object.keys(state.meta.language_counts).length;
  document.querySelector("#stat-verified").textContent = formatReviewMonth(state.meta.latest_verification);

  const order = ["computer-science", "business-entrepreneurship", "math-statistics", "health-medicine", "languages"];
  const counts = new Map();
  state.courses.forEach((course) => counts.set(course.category, (counts.get(course.category) || 0) + 1));
  const sample = new Map(state.courses.map((course) => [course.category, course]));
  const categoryContainer = document.querySelector("#home-categories");
  categoryContainer.innerHTML = order
    .filter((id) => sample.has(id))
    .map((id) => renderHomeCategory(id, labelCategory(sample.get(id)), counts.get(id) || 0))
    .join("");
  window.oliHydrateIcons?.(categoryContainer);

  const featured = [...state.courses]
    .filter((course) => course.status === "active")
    .sort((a, b) => b.recommendation_score - a.recommendation_score || b.quality_score - a.quality_score || courseTitle(a).localeCompare(courseTitle(b), "fr"))
    .slice(0, 4);
  const container = document.querySelector("#featured-courses");
  container.innerHTML = featured.map((course) => renderCatalogueCard(course, "mini-course-card")).join("");
  window.oliHydrateIcons?.(container);
}

function getCatalogueEls() {
  return {
    filters: document.querySelector("#filters"), search: document.querySelector("#search"),
    category: document.querySelector("#category"), language: document.querySelector("#language"),
    level: document.querySelector("#level"), access: document.querySelector("#access"),
    tier: document.querySelector("#tier"), status: document.querySelector("#status"),
    sort: document.querySelector("#sort"), credential: document.querySelector("#credential"),
    credit: document.querySelector("#credit"), clear: document.querySelector("#clear-filters"),
    results: document.querySelector("#results"), resultCount: document.querySelector("#result-count"),
    empty: document.querySelector("#empty-state"), showMore: document.querySelector("#show-more"),
    pageCourseCount: document.querySelector("#page-course-count"),
    viewButtons: [...document.querySelectorAll("[data-view]")],
    filterDisclosure: document.querySelector("#primary-filters"),
    mobileFilterCount: document.querySelector("#mobile-filter-count"),
    emptyClear: document.querySelector("#empty-clear-filters"),
    activeFilters: document.querySelector("#active-filters"),
    searchShortcut: document.querySelector("[data-focus-search]"),
  };
}

function getFormState(els) {
  return {
    q: els.search.value.trim(), category: els.category.value, language: els.language.value,
    level: els.level.value, access: els.access.value, tier: els.tier.value,
    status: els.status.value, sort: els.sort.value,
    credential: els.credential.checked, credit: els.credit.checked,
  };
}

function setFormState(els, params) {
  els.search.value = params.get("q") || "";
  els.category.value = params.get("category") || "";
  els.language.value = params.get("language") || "";
  els.level.value = params.get("level") || "";
  els.access.value = params.get("access") || "";
  els.tier.value = params.get("tier") || "";
  els.status.value = params.get("status") || "";
  els.sort.value = params.get("sort") || "recommendation";
  els.credential.checked = params.get("credential") === "1";
  els.credit.checked = params.get("credit") === "1";
}

function syncUrl(values) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
    if (value === true) params.set(key, "1");
    else if (value && !(key === "sort" && value === "recommendation")) params.set(key, value);
  }
  const query = params.toString();
  history.replaceState(null, "", query ? `?${query}` : location.pathname);
}

function populateFilters(els) {
  const categories = [...new Map(state.courses.map((course) => [course.category, labelCategory(course)])).entries()]
    .sort((a, b) => a[1].localeCompare(b[1], "fr"));
  const languages = [...new Set(state.courses.flatMap((course) => [course.primary_language, ...course.other_languages]))]
    .sort((a, b) => labelLanguage(a).localeCompare(labelLanguage(b), "fr"));
  const rank = new Map(levelOrder.map((value, index) => [value, index]));
  const levels = [...new Set(state.courses.map((course) => course.level))]
    .sort((a, b) => (rank.get(a) ?? 99) - (rank.get(b) ?? 99));

  categories.forEach(([value, label]) => els.category.add(new Option(label, value)));
  languages.forEach((value) => els.language.add(new Option(labelLanguage(value), value)));

  const placeholder = new Option(copy.level, "");
  const progression = document.createElement("optgroup");
  progression.label = copy.progression;
  levels.filter((value) => value !== "beginner_to_advanced")
    .forEach((value) => progression.append(new Option(labelLevel(value), value)));
  const broad = document.createElement("optgroup");
  broad.label = copy.broad;
  if (levels.includes("beginner_to_advanced")) broad.append(new Option(labelLevel("beginner_to_advanced"), "beginner_to_advanced"));
  const shortcut = document.createElement("optgroup");
  shortcut.label = copy.shortcut;
  shortcut.append(new Option(copy.beginnerFriendly, "beginner-friendly"));
  els.level.replaceChildren(placeholder, progression, broad, shortcut);
}

function filteredCourses(values) {
  const queryTokens = tokenize(values.q);
  const list = state.courses.filter((course) => {
    const tokens = tokenize(`${course.search_text} ${labelCategory(course)} ${labelLanguage(course.primary_language)}`);
    if (queryTokens.length && !queryTokens.every((word) => tokens.some((token) => token === word || (word.length >= 2 && token.startsWith(word))))) return false;
    if (values.category && course.category !== values.category) return false;
    if (values.language && course.primary_language !== values.language && !course.other_languages.includes(values.language)) return false;
    if (values.level === "beginner-friendly" && !["beginner", "beginner_to_intermediate"].includes(course.level)) return false;
    if (values.level && values.level !== "beginner-friendly" && course.level !== values.level) return false;
    if (values.access && course.access_short !== values.access) return false;
    if (values.tier && course.quality_tier !== values.tier) return false;
    if (values.status && course.status !== values.status) return false;
    if (values.credential && !course.has_free_credential) return false;
    if (values.credit && !course.has_free_academic_credit) return false;
    return true;
  });
  const compare = {
    recommendation: (a, b) => b.recommendation_score - a.recommendation_score || b.quality_score - a.quality_score || courseTitle(a).localeCompare(courseTitle(b), "fr"),
    quality: (a, b) => b.quality_score - a.quality_score || b.recommendation_score - a.recommendation_score || courseTitle(a).localeCompare(courseTitle(b), "fr"),
    verified: (a, b) => b.last_verified.localeCompare(a.last_verified) || b.recommendation_score - a.recommendation_score,
    title: (a, b) => courseTitle(a).localeCompare(courseTitle(b), "fr"),
  }[values.sort] || (() => 0);
  return list.sort(compare);
}

function activeFilterCount(values) {
  return ["q", "category", "language", "level", "access", "tier", "status", "credential", "credit"]
    .filter((key) => Boolean(values[key])).length;
}

function renderActiveFilters(els, values) {
  const items = [];
  for (const key of ["q", "category", "language", "level", "access", "tier", "status", "credential", "credit"]) {
    if (!values[key]) continue;
    const control = key === "q" ? els.search : els[key];
    const fieldLabel = control.labels?.[0]?.textContent.trim() || key;
    const valueLabel = control.tagName === "SELECT" ? control.selectedOptions[0].textContent : (typeof values[key] === "string" ? values[key] : "");
    const text = valueLabel ? `${fieldLabel} : ${valueLabel}` : fieldLabel;
    items.push(`<button type="button" class="filter-chip" data-remove-filter="${key}" aria-label="${copy.remove} ${escapeHtml(text)}"><span>${escapeHtml(text)}</span><b aria-hidden="true">×</b></button>`);
  }
  els.activeFilters.innerHTML = items.join("");
  els.clear.hidden = items.length === 0;
  document.querySelectorAll(".language-menu a").forEach((link) => {
    const target = new URL(link.href);
    target.search = location.search;
    link.href = target.href;
  });
}

function renderCatalogue(els) {
  const values = getFormState(els);
  syncUrl(values);
  const courses = filteredCourses(values);
  const visible = courses.slice(0, state.visibleLimit);

  els.results.classList.toggle("catalogue-list", state.viewMode === "list");
  els.viewButtons.forEach((button) => {
    const active = button.dataset.view === state.viewMode;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", active ? "true" : "false");
  });
  els.resultCount.textContent = `${courses.length} ${copy.courses}`;
  if (els.mobileFilterCount) {
    const count = activeFilterCount(values);
    els.mobileFilterCount.textContent = count ? ` · ${count}` : "";
  }
  els.results.innerHTML = visible.map((course) => renderCatalogueCard(course)).join("");
  window.oliHydrateIcons?.(els.results);
  renderActiveFilters(els, values);
  els.empty.hidden = courses.length !== 0;
  els.showMore.hidden = visible.length >= courses.length;
  if (!els.showMore.hidden) els.showMore.textContent = `${copy.showMore} · ${courses.length - visible.length}`;
}

function resetCatalogue(els, focusSearch = true) {
  els.filters.reset();
  els.sort.value = "recommendation";
  state.visibleLimit = 18;
  renderCatalogue(els);
  if (focusSearch) els.search.focus();
}

function bootCatalogue() {
  const els = getCatalogueEls();
  els.pageCourseCount.textContent = state.meta.published_count;
  populateFilters(els);
  setFormState(els, new URLSearchParams(location.search));
  try {
    const savedView = localStorage.getItem("oli-catalogue-view");
    if (savedView === "grid" || savedView === "list") state.viewMode = savedView;
  } catch {}

  const rerender = () => { state.visibleLimit = 18; renderCatalogue(els); };
  els.filters.addEventListener("submit", (event) => event.preventDefault());
  els.filters.addEventListener("input", rerender);
  els.filters.addEventListener("change", rerender);
  els.sort.addEventListener("change", rerender);
  els.clear.addEventListener("click", () => resetCatalogue(els));
  els.emptyClear?.addEventListener("click", () => resetCatalogue(els));
  els.searchShortcut?.addEventListener("click", () => els.search.focus());
  els.activeFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-remove-filter]");
    if (!button) return;
    const key = button.dataset.removeFilter;
    const control = key === "q" ? els.search : els[key];
    if (control.type === "checkbox") control.checked = false;
    else control.value = "";
    rerender();
  });
  els.showMore.addEventListener("click", () => {
    const previous = state.visibleLimit;
    state.visibleLimit += 18;
    renderCatalogue(els);
    els.results.children[previous]?.querySelector("h3 a")?.focus();
  });
  els.viewButtons.forEach((button) => button.addEventListener("click", () => {
    state.viewMode = button.dataset.view === "list" ? "list" : "grid";
    try { localStorage.setItem("oli-catalogue-view", state.viewMode); } catch {}
    renderCatalogue(els);
  }));

  const mobile = window.matchMedia("(max-width: 760px)");
  const syncMobile = () => {
    if (els.filterDisclosure) {
      if (mobile.matches) els.filterDisclosure.removeAttribute("open");
      else els.filterDisclosure.setAttribute("open", "");
    }
    if (mobile.matches) state.viewMode = "grid";
  };
  syncMobile();
  mobile.addEventListener?.("change", () => { syncMobile(); renderCatalogue(els); });
  renderCatalogue(els);
}

async function boot() {
  try {
    const [catalogResponse, metaResponse] = await Promise.all([
      fetch(route("data/catalog.json")),
      fetch(route("data/meta.json")),
    ]);
    if (!catalogResponse.ok || !metaResponse.ok) throw new Error("Failed to load public data");
    state.courses = await catalogResponse.json();
    state.meta = await metaResponse.json();
    if (pageType === "home") renderHome();
    else bootCatalogue();
  } catch (error) {
    console.error(error);
    const resultCount = document.querySelector("#result-count");
    const empty = document.querySelector("#empty-state");
    if (resultCount) resultCount.textContent = copy.loadError;
    if (empty) empty.hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", boot);
