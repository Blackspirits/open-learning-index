const state = {
  courses: [],
  meta: null,
  visibleLimit: 18,
  viewMode: "grid",
};

const pageLocale = document.body.dataset.locale === "pt-PT" ? "pt-PT" : "en";
const pageType = document.body.dataset.page || "catalogue";
const rootPath = document.body.dataset.root || "./";
const isPt = pageLocale === "pt-PT";

const languageNames = {
  en: { "pt-BR": "Portuguese (Brazil)", "pt-PT": "Portuguese (Portugal)" },
  "pt-PT": { "pt-BR": "Português (Brasil)", "pt-PT": "Português (Portugal)" },
};

const categoryNamesPt = {
  "ai-data": "IA e Dados",
  "arts-design": "Artes e Design",
  "business-entrepreneurship": "Negócios e Empreendedorismo",
  "computer-science": "Ciência de Computadores e Software",
  "cybersecurity-it": "Cibersegurança e TI",
  "education-teaching": "Educação e Ensino",
  "engineering-electronics": "Engenharia e Eletrónica",
  "finance-economics": "Finanças e Economia",
  "health-medicine": "Saúde e Medicina",
  "history-culture": "História e Cultura",
  "humanities-philosophy": "Humanidades e Filosofia",
  languages: "Línguas",
  "law-public-policy": "Direito e Políticas Públicas",
  "marketing-sales": "Marketing e Vendas",
  "math-statistics": "Matemática e Estatística",
  "natural-sciences": "Ciências Naturais",
  "project-product-leadership": "Projeto, Produto e Liderança",
  "psychology-behavior": "Psicologia e Comportamento",
  "writing-communication": "Escrita e Comunicação",
};

const categoryIcons = {
  "computer-science": "▣",
  "business-entrepreneurship": "▥",
  "math-statistics": "∑",
  "health-medicine": "❤",
  languages: "▤",
  "ai-data": "◫",
  "cybersecurity-it": "⌾",
  "arts-design": "✦",
  "education-teaching": "◇",
};

const levelNamesPt = {
  beginner: "Principiante",
  beginner_to_intermediate: "Principiante a intermédio",
  intermediate: "Intermédio",
  intermediate_to_advanced: "Intermédio a avançado",
  advanced: "Avançado",
  graduate: "Pós-graduação",
};

const accessPt = {
  F0: "Curso completo + credencial gratuita",
  F1: "Percurso avaliado gratuito",
  F2: "Conteúdo pedagógico gratuito",
};

const displayLanguage = typeof Intl.DisplayNames === "function"
  ? new Intl.DisplayNames([pageLocale], { type: "language" })
  : null;

function route(path) {
  return `${rootPath}${path}`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function labelLanguage(code) {
  if (languageNames[pageLocale]?.[code]) return languageNames[pageLocale][code];
  try {
    return displayLanguage?.of(code) || code;
  } catch {
    return code;
  }
}

function labelCategory(course) {
  return isPt ? (categoryNamesPt[course.category] || course.category_name) : course.category_name;
}

function labelLevel(value) {
  if (isPt && levelNamesPt[value]) return levelNamesPt[value];
  return String(value || "")
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
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

function initials(provider) {
  const stopwords = new Set(["of", "the", "and", "de", "da", "do", "dos", "das", "e", "et", "la", "le"]);
  const cleaned = String(provider || "")
    .replace(/\([^)]*\)/g, " ")
    .replace(/[^A-Za-zÀ-ÿ0-9 ]/g, " ");
  const allWords = cleaned.split(/\s+/).filter(Boolean);
  const words = allWords.filter((word) => !stopwords.has(normalize(word)));
  const source = words.length ? words : allWords;
  if (!source.length) return "OLI";
  if (source.length === 1) return source[0].slice(0, 3).toUpperCase();
  return source.slice(0, 2).map((word) => word[0]).join("").toUpperCase();
}

function scorePill(course) {
  return `<span class="score-pill">${Number(course.recommendation_score).toFixed(1)}</span>`;
}

function renderMiniCourseCard(course) {
  const archived = course.status === "active_archive"
    ? `<span class="mini-tag tag-archive">${isPt ? "Arquivado" : "Archived"}</span>`
    : "";
  return `
    <article class="mini-course-card">
      <div class="mini-card-top">
        ${scorePill(course)}
        <span class="bookmark" aria-hidden="true">♡</span>
      </div>
      <div class="provider-mark" aria-hidden="true">${escapeHtml(initials(course.provider))}</div>
      <h3><a href="${route(`courses/${encodeURIComponent(course.id)}/`)}">${escapeHtml(course.title)}</a></h3>
      <p class="provider">${escapeHtml(course.provider)}</p>
      <div class="mini-tags">
        <span class="mini-tag tag-category">${escapeHtml(labelCategory(course))}</span>
        <span class="mini-tag">${escapeHtml(labelLanguage(course.primary_language))}</span>
        <span class="mini-tag">${escapeHtml(labelLevel(course.level))}</span>
        ${archived}
      </div>
    </article>
  `;
}

function renderHomeCategory(id, name, count) {
  const icon = categoryIcons[id] || "◇";
  const cataloguePath = isPt ? `pt/courses/?category=${encodeURIComponent(id)}` : `courses/?category=${encodeURIComponent(id)}`;
  return `
    <a class="category-tile" href="${route(cataloguePath)}">
      <span class="category-icon icon-${escapeHtml(id)}" aria-hidden="true">${escapeHtml(icon)}</span>
      <strong>${escapeHtml(name)}</strong>
      <small>${count} ${isPt ? "cursos" : "courses"}</small>
    </a>
  `;
}

function renderHome() {
  const statCourses = document.querySelector("#stat-courses");
  const statCategories = document.querySelector("#stat-categories");
  const statLanguages = document.querySelector("#stat-languages");
  if (statCourses) statCourses.textContent = state.meta.published_count;
  if (statCategories) statCategories.textContent = state.meta.category_count;
  if (statLanguages) statLanguages.textContent = Object.keys(state.meta.language_counts).length;

  const categoryOrder = [
    "computer-science",
    "business-entrepreneurship",
    "math-statistics",
    "health-medicine",
    "languages",
  ];
  const counts = new Map();
  state.courses.forEach((course) => counts.set(course.category, (counts.get(course.category) || 0) + 1));
  const byCategory = new Map(state.courses.map((course) => [course.category, course]));
  const categories = categoryOrder
    .filter((id) => byCategory.has(id))
    .map((id) => {
      const course = byCategory.get(id);
      return renderHomeCategory(id, labelCategory(course), counts.get(id) || 0);
    });
  document.querySelector("#home-categories").innerHTML = categories.join("");

  const featured = [...state.courses]
    .filter((course) => course.status === "active")
    .sort((a, b) =>
      b.recommendation_score - a.recommendation_score ||
      b.quality_score - a.quality_score ||
      a.title.localeCompare(b.title)
    )
    .slice(0, 4);
  document.querySelector("#featured-courses").innerHTML = featured.map(renderMiniCourseCard).join("");
}

function getCatalogueEls() {
  return {
    filters: document.querySelector("#filters"),
    search: document.querySelector("#search"),
    category: document.querySelector("#category"),
    language: document.querySelector("#language"),
    level: document.querySelector("#level"),
    access: document.querySelector("#access"),
    tier: document.querySelector("#tier"),
    status: document.querySelector("#status"),
    sort: document.querySelector("#sort"),
    credential: document.querySelector("#credential"),
    credit: document.querySelector("#credit"),
    clear: document.querySelector("#clear-filters"),
    results: document.querySelector("#results"),
    resultCount: document.querySelector("#result-count"),
    empty: document.querySelector("#empty-state"),
    showMore: document.querySelector("#show-more"),
    pageCourseCount: document.querySelector("#page-course-count"),
    viewButtons: [...document.querySelectorAll("[data-view]")],
  };
}

function getFormState(els) {
  return {
    q: els.search.value.trim(),
    category: els.category.value,
    language: els.language.value,
    level: els.level.value,
    access: els.access.value,
    tier: els.tier.value,
    status: els.status.value,
    sort: els.sort.value,
    credential: els.credential.checked,
    credit: els.credit.checked,
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
  const categories = [...new Map(state.courses.map((c) => [c.category, labelCategory(c)])).entries()]
    .sort((a, b) => a[1].localeCompare(b[1], pageLocale));
  const languages = [...new Set(state.courses.flatMap((c) => [c.primary_language, ...c.other_languages]))]
    .sort((a, b) => labelLanguage(a).localeCompare(labelLanguage(b), pageLocale));
  const levels = [...new Set(state.courses.map((c) => c.level))]
    .sort((a, b) => labelLevel(a).localeCompare(labelLevel(b), pageLocale));

  categories.forEach(([value, label]) => els.category.add(new Option(label, value)));
  languages.forEach((value) => els.language.add(new Option(labelLanguage(value), value)));
  levels.forEach((value) => els.level.add(new Option(labelLevel(value), value)));
}

function filteredCourses(values) {
  const queryTokens = tokenize(values.q);
  const list = state.courses.filter((course) => {
    const courseTokens = tokenize(course.search_text);
    if (queryTokens.length && !queryTokens.every((word) => courseTokens.includes(word))) return false;
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
    recommendation: (a, b) => b.recommendation_score - a.recommendation_score || b.quality_score - a.quality_score || a.title.localeCompare(b.title),
    quality: (a, b) => b.quality_score - a.quality_score || b.recommendation_score - a.recommendation_score || a.title.localeCompare(b.title),
    verified: (a, b) => b.last_verified.localeCompare(a.last_verified) || b.recommendation_score - a.recommendation_score,
    title: (a, b) => a.title.localeCompare(b.title),
  }[values.sort] || (() => 0);

  return list.sort(compare);
}

function renderCatalogueCard(course) {
  const archived = course.status === "active_archive"
    ? `<span class="mini-tag tag-archive">${isPt ? "Arquivado" : "Archived"}</span>`
    : "";
  const accessText = isPt ? (accessPt[course.access_short] || course.access_label) : course.access_label;
  return `
    <article class="catalogue-card">
      <div class="catalogue-card-head">
        ${scorePill(course)}
        <span class="bookmark" aria-hidden="true">♡</span>
      </div>
      <div class="provider-mark large" aria-hidden="true">${escapeHtml(initials(course.provider))}</div>
      <h3><a href="${route(`courses/${encodeURIComponent(course.id)}/`)}">${escapeHtml(course.title)}</a></h3>
      <p class="provider">${escapeHtml(course.provider)}</p>
      <div class="card-spacer"></div>
      <div class="mini-tags">
        <span class="mini-tag tag-category">${escapeHtml(labelCategory(course))}</span>
        <span class="mini-tag">${escapeHtml(labelLanguage(course.primary_language))}</span>
        <span class="mini-tag">${escapeHtml(labelLevel(course.level))}</span>
        ${archived}
      </div>
      <div class="access-line" title="${escapeHtml(course.access_description)}">
        <strong>${escapeHtml(course.access_short)}</strong>
        <span>${escapeHtml(accessText)}</span>
      </div>
    </article>
  `;
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

  els.resultCount.textContent = isPt
    ? `${courses.length} curso${courses.length === 1 ? "" : "s"}`
    : `${courses.length} course${courses.length === 1 ? "" : "s"}`;
  els.results.innerHTML = visible.map(renderCatalogueCard).join("");
  els.empty.hidden = courses.length !== 0;
  els.showMore.hidden = visible.length >= courses.length;

  if (!els.showMore.hidden) {
    const remaining = courses.length - visible.length;
    els.showMore.textContent = isPt ? `Mostrar mais · ${remaining}` : `Show more · ${remaining}`;
  }
}

function bootCatalogue() {
  const els = getCatalogueEls();
  els.pageCourseCount.textContent = state.meta.published_count;
  populateFilters(els);
  setFormState(els, new URLSearchParams(location.search));
  try {
    const savedView = localStorage.getItem("oli-catalogue-view");
    if (savedView === "grid" || savedView === "list") state.viewMode = savedView;
  } catch {
    state.viewMode = "grid";
  }

  const rerender = () => {
    state.visibleLimit = 18;
    renderCatalogue(els);
  };
  els.filters.addEventListener("input", rerender);
  els.filters.addEventListener("change", rerender);
  els.clear.addEventListener("click", () => {
    els.filters.reset();
    els.sort.value = "recommendation";
    state.visibleLimit = 18;
    renderCatalogue(els);
    els.search.focus();
  });
  els.showMore.addEventListener("click", () => {
    state.visibleLimit += 18;
    renderCatalogue(els);
  });
  els.viewButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.viewMode = button.dataset.view === "list" ? "list" : "grid";
      try {
        localStorage.setItem("oli-catalogue-view", state.viewMode);
      } catch {
        // View preference persistence is optional.
      }
      renderCatalogue(els);
    });
  });

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
    if (resultCount) resultCount.textContent = isPt ? "Não foi possível carregar o catálogo." : "The catalogue could not be loaded.";
    if (empty) empty.hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", boot);
