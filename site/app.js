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

const levelNamesPt = {
  beginner: "Principiante",
  beginner_to_intermediate: "Principiante a intermédio",
  beginner_to_advanced: "Principiante a avançado",
  intermediate: "Intermédio",
  intermediate_to_advanced: "Intermédio a avançado",
  advanced: "Avançado",
  graduate: "Pós-graduação",
  undergraduate: "Licenciatura",
};

const accessPt = {
  F0: "Curso e credencial gratuitos",
  F1: "Percurso completo com avaliação",
  F2: "Conteúdos completos gratuitos",
};

const displayLanguage = typeof Intl.DisplayNames === "function"
  ? new Intl.DisplayNames([pageLocale], { type: "language" })
  : null;

function route(path) {
  return `${rootPath}${path}`;
}

function coursePath(courseId) {
  return isPt
    ? `pt/courses/${encodeURIComponent(courseId)}/`
    : `courses/${encodeURIComponent(courseId)}/`;
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

function labelCourseLanguage(course) {
  const label = labelLanguage(course.primary_language);
  return isPt ? `Em ${label.charAt(0).toLocaleLowerCase(pageLocale)}${label.slice(1)}` : `In ${label}`;
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
  const score = new Intl.NumberFormat(pageLocale, { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(course.recommendation_score);
  const label = isPt ? `Recomendação ${score} em 10` : `Recommendation ${score} out of 10`;
  return `<span class="score-pill" aria-label="${label}">${score}</span>`;
}

function courseTitle(course) {
  return isPt ? course.presentation_pt.title : course.title;
}

function courseMedia(course) {
  const media = course.media || {};
  if (media.src) return `<div class="course-media media-${escapeHtml(media.kind)}" aria-hidden="true"><img src="${route(media.src)}" alt="" width="800" height="450" loading="lazy" decoding="async"></div>`;
  const icon = media.icon || categoryIcons[course.category] || "education";
  return `<div class="course-media media-editorial media-${escapeHtml(course.category)}" aria-hidden="true"><span class="media-symbol" data-icon="${escapeHtml(icon)}"></span><span class="media-provider-name">${escapeHtml(course.provider)}</span></div>`;
}

function renderMiniCourseCard(course) {
  return renderCatalogueCard(course, "mini-course-card");
}

function renderHomeCategory(id, name, count) {
  const icon = categoryIcons[id] || "curated";
  const categoryPath = isPt ? `pt/categories/${encodeURIComponent(id)}/` : `categories/${encodeURIComponent(id)}/`;
  return `
    <a class="category-tile" href="${route(categoryPath)}">
      <span class="category-icon icon-${escapeHtml(id)}" data-icon="${escapeHtml(icon)}" aria-hidden="true"></span>
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
  if (statLanguages) statLanguages.textContent = state.meta.language_count ?? Object.keys(state.meta.language_counts).length;

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
  const categoryContainer = document.querySelector("#home-categories");
  categoryContainer.innerHTML = categories.join("");
  window.oliHydrateIcons?.(categoryContainer);

  const featured = [...state.courses]
    .filter((course) => course.status === "active")
    .sort((a, b) =>
      b.recommendation_score - a.recommendation_score ||
      b.quality_score - a.quality_score ||
      a.title.localeCompare(b.title)
    )
    .slice(0, 4);
  const container = document.querySelector("#featured-courses");
  container.innerHTML = featured.map(renderMiniCourseCard).join("");
  window.oliHydrateIcons?.(container);
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
    filterDisclosure: document.querySelector("#primary-filters"),
    mobileFilterCount: document.querySelector("#mobile-filter-count"),
    emptyClear: document.querySelector("#empty-clear-filters"),
    activeFilters: document.querySelector("#active-filters"),
    searchShortcut: document.querySelector("[data-focus-search]"),
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
    const courseTokens = tokenize(`${course.search_text} ${labelCategory(course)} ${labelLanguage(course.primary_language)}`);
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
    title: (a, b) => courseTitle(a).localeCompare(courseTitle(b), pageLocale),
  }[values.sort] || (() => 0);

  return list.sort(compare);
}

function renderCatalogueCard(course, className = "catalogue-card") {
  const archived = course.status === "active_archive"
    ? `<span class="mini-tag tag-archive">${isPt ? "Arquivado" : "Archived"}</span>`
    : "";
  const accessText = isPt ? (accessPt[course.access_short] || course.access_label) : course.access_label;
  return `
    <article class="${className}">
      ${courseMedia(course)}
      <div class="card-body">
      <div class="card-heading">
        <p class="provider">${escapeHtml(course.provider)}</p>
        <h3><a href="${route(coursePath(course.id))}">${escapeHtml(courseTitle(course))}</a></h3>
      </div>
      <div class="catalogue-card-head">
        ${scorePill(course)}
        <span class="score-context">${isPt ? "Recomendação" : "Recommendation"}</span>
      </div>
      <div class="mini-tags">
        <span class="mini-tag tag-category">${escapeHtml(labelCategory(course))}</span>
        <span class="mini-tag">${escapeHtml(labelCourseLanguage(course))}</span>
        <span class="mini-tag">${escapeHtml(labelLevel(course.level))}</span>
        ${archived}
      </div>
      <div class="access-line">
        <span data-icon="access" aria-hidden="true"></span>
        <span>${escapeHtml(accessText)}</span>
      </div>
      </div>
    </article>
  `;
}

function activeFilterCount(values) {
  return [
    values.category,
    values.language,
    values.level,
    values.access,
    values.tier,
    values.status,
    values.credential,
    values.credit,
  ].filter(Boolean).length;
}

function renderActiveFilters(els, values) {
  const items = [];
  for (const key of ["q", "category", "language", "level", "access", "tier", "status", "credential", "credit"]) {
    if (!values[key]) continue;
    const control = key === "q" ? els.search : els[key];
    const fieldLabel = control.labels?.[0]?.textContent.trim() || key;
    const valueLabel = control.tagName === "SELECT" ? control.selectedOptions[0].textContent : (typeof values[key] === "string" ? values[key] : "");
    const text = valueLabel ? `${fieldLabel}: ${valueLabel}` : fieldLabel;
    const label = `${isPt ? "Remover" : "Remove"} ${text}`;
    items.push(`<button type="button" class="filter-chip" data-remove-filter="${key}" aria-label="${escapeHtml(label)}"><span>${escapeHtml(text)}</span><b aria-hidden="true">×</b></button>`);
  }
  els.activeFilters.innerHTML = items.join("");
  els.clear.hidden = items.length === 0;
  const languageSwitch = document.querySelector(".language-switch");
  if (languageSwitch) {
    const target = new URL(languageSwitch.href);
    target.search = location.search;
    languageSwitch.href = target.href;
  }
}

function resetCatalogue(els, focusSearch = true) {
  els.filters.reset();
  els.sort.value = "recommendation";
  state.visibleLimit = 18;
  renderCatalogue(els);
  if (focusSearch) els.search.focus();
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
  if (els.mobileFilterCount) {
    const count = activeFilterCount(values);
    els.mobileFilterCount.textContent = count ? ` · ${count}` : "";
  }
  els.results.innerHTML = visible.map(course => renderCatalogueCard(course)).join("");
  window.oliHydrateIcons?.(els.results);
  renderActiveFilters(els, values);
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
  els.filters.addEventListener("submit", event => event.preventDefault());
  els.filters.addEventListener("input", rerender);
  els.sort.addEventListener("change", rerender);
  els.activeFilters.addEventListener("click", event => {
    const button = event.target.closest("[data-remove-filter]");
    if (!button) return;
    const key = button.dataset.removeFilter;
    const control = key === "q" ? els.search : els[key];
    if (control.type === "checkbox") control.checked = false;
    else control.value = "";
    rerender();
    (els.activeFilters.querySelector("button") || els.search).focus();
  });
  els.filters.addEventListener("change", rerender);
  els.clear.addEventListener("click", () => resetCatalogue(els));
  els.emptyClear?.addEventListener("click", () => resetCatalogue(els));
  els.searchShortcut?.addEventListener("click", () => els.search.focus());
  els.showMore.addEventListener("click", () => {
    const previousLimit = state.visibleLimit;
    state.visibleLimit += 18;
    renderCatalogue(els);
    els.results.children[previousLimit]?.querySelector("h3 a")?.focus();
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

  const mobile = window.matchMedia("(max-width: 760px)");
  const syncMobileLayout = () => {
    if (els.filterDisclosure) {
      if (mobile.matches) els.filterDisclosure.removeAttribute("open");
      else els.filterDisclosure.setAttribute("open", "");
    }
    if (mobile.matches && state.viewMode !== "grid") {
      state.viewMode = "grid";
    }
  };
  syncMobileLayout();
  mobile.addEventListener?.("change", () => {
    syncMobileLayout();
    renderCatalogue(els);
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
