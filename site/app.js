const state = {
  courses: [],
  meta: null,
  visibleLimit: 24,
};

const els = {};
const pageLocale = document.body.dataset.locale === "pt-PT" ? "pt-PT" : "en";
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

const levelNamesPt = {
  beginner: "Principiante",
  beginner_to_intermediate: "Principiante a intermédio",
  intermediate: "Intermédio",
  intermediate_to_advanced: "Intermédio a avançado",
  advanced: "Avançado",
  graduate: "Pós-graduação",
};

const accessPt = {
  F0: { label: "Curso completo + credencial gratuita" },
  F1: { label: "Percurso avaliado gratuito" },
  F2: { label: "Conteúdo pedagógico gratuito" },
};

const displayLanguage = typeof Intl.DisplayNames === "function"
  ? new Intl.DisplayNames([pageLocale], { type: "language" })
  : null;

function route(path) {
  return `${rootPath}${path}`;
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
  return value
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

function parseDateOnly(value) {
  return new Date(value + "T00:00:00Z");
}

function formatDate(value) {
  return new Intl.DateTimeFormat(pageLocale, {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(parseDateOnly(value));
}

function freshness(course) {
  const now = new Date();
  const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  const next = parseDateOnly(course.next_review).getTime();
  const days = Math.ceil((next - today) / 86400000);
  const checked = formatDate(course.last_verified);

  if (isPt) {
    if (days > 30) return { label: `Verificado ${checked}`, tone: "good" };
    if (days >= 0) return { label: `Revisão em breve · ${checked}`, tone: "warn" };
    if (days >= -30) return { label: `Revisão necessária · ${checked}`, tone: "warn" };
    return { label: `Prioridade de revisão · ${checked}`, tone: "danger" };
  }

  if (days > 30) return { label: `Checked ${checked}`, tone: "good" };
  if (days >= 0) return { label: `Check due soon · ${checked}`, tone: "warn" };
  if (days >= -30) return { label: `Check due · ${checked}`, tone: "warn" };
  return { label: `Re-check priority · ${checked}`, tone: "danger" };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getFormState() {
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

function setFormState(params) {
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

function populateFilters() {
  const categories = [...new Map(state.courses.map((c) => [c.category, labelCategory(c)])).entries()]
    .sort((a, b) => a[1].localeCompare(b[1], pageLocale));
  const languages = [...new Set(state.courses.flatMap((c) => [c.primary_language, ...c.other_languages]))]
    .sort((a, b) => labelLanguage(a).localeCompare(labelLanguage(b), pageLocale));
  const levels = [...new Set(state.courses.map((c) => c.level))]
    .sort((a, b) => labelLevel(a).localeCompare(labelLevel(b), pageLocale));

  for (const [value, label] of categories) els.category.add(new Option(label, value));
  for (const value of languages) els.language.add(new Option(labelLanguage(value), value));
  for (const value of levels) els.level.add(new Option(labelLevel(value), value));
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

function scoreBlock(label, score, tier) {
  return `
    <div class="score">
      <span>${escapeHtml(label)}</span>
      <strong>${Number(score).toFixed(1)}</strong>
      <small>${escapeHtml(tier)}</small>
    </div>
  `;
}

function renderCard(course) {
  const fresh = freshness(course);
  const languages = [course.primary_language, ...course.other_languages].map(labelLanguage).join(" · ");
  const archive = course.status === "active_archive"
    ? `<span class="badge badge-neutral">${isPt ? "Arquivado mas disponível" : "Archived but still available"}</span>`
    : "";
  const credit = course.has_free_academic_credit
    ? `<span class="badge badge-credit">${isPt ? "Créditos académicos gratuitos" : "Free academic credit"}</span>`
    : "";
  const accessLabel = isPt ? (accessPt[course.access_short]?.label || course.access_label) : course.access_label;
  const recommendationLabel = isPt ? "Recomendação" : "Recommendation";
  const qualityLabel = isPt ? "Qualidade" : "Quality";
  const detailsLabel = isPt ? "Detalhes (EN)" : "Details";
  const openLabel = isPt ? "Abrir curso" : "Open course";
  const editorialNote = isPt ? '<span class="badge">Nota editorial em inglês</span>' : "";

  return `
    <article class="course-card">
      <div class="card-topline">
        <a class="category" href="${route(`categories/${encodeURIComponent(course.category)}/`)}">${escapeHtml(labelCategory(course))}</a>
        <span class="freshness freshness-${fresh.tone}">${escapeHtml(fresh.label)}</span>
      </div>
      <div>
        <h3><a href="${route(`courses/${encodeURIComponent(course.id)}/`)}">${escapeHtml(course.title)}</a></h3>
        <p class="provider">${escapeHtml(course.provider)}</p>
      </div>
      <div class="badges">
        <span class="badge">${escapeHtml(labelLevel(course.level))}</span>
        <span class="badge">${escapeHtml(languages)}</span>
        <span class="badge badge-access" title="${escapeHtml(course.access_description)}">${escapeHtml(course.access_short)} · ${escapeHtml(accessLabel)}</span>
        ${archive}
        ${credit}
        ${editorialNote}
      </div>
      <div class="scores" aria-label="${isPt ? "Avaliações do curso" : "Course scores"}">
        ${scoreBlock(recommendationLabel, course.recommendation_score, course.recommendation_tier)}
        ${scoreBlock(qualityLabel, course.quality_score, course.quality_tier)}
      </div>
      <p class="why">${escapeHtml(course.why_recommended)}</p>
      <div class="card-footer">
        <span class="card-links">
          <a href="${route(`courses/${encodeURIComponent(course.id)}/`)}" aria-label="${escapeHtml(detailsLabel)}: ${escapeHtml(course.title)}">${detailsLabel}</a>
          <a href="${escapeHtml(course.url)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(openLabel)}: ${escapeHtml(course.title)}">${openLabel} <span aria-hidden="true">↗</span></a>
        </span>
      </div>
    </article>
  `;
}

function activeFilterCount(values) {
  return [values.q, values.category, values.language, values.level, values.access, values.tier, values.status, values.credential, values.credit].filter(Boolean).length;
}

function updateQuickState(values) {
  const states = {
    all: activeFilterCount(values) === 0,
    "pt-PT": values.language === "pt-PT",
    F0: values.access === "F0",
    beginner: values.level === "beginner-friendly",
    languages: values.category === "languages",
  };
  document.querySelectorAll("[data-quick]").forEach((button) => {
    button.setAttribute("aria-pressed", states[button.dataset.quick] ? "true" : "false");
  });
}

function render() {
  const values = getFormState();
  syncUrl(values);
  const courses = filteredCourses(values);
  const visible = courses.slice(0, state.visibleLimit);
  const count = activeFilterCount(values);

  els.resultCount.textContent = isPt
    ? `${courses.length} curso${courses.length === 1 ? "" : "s"}`
    : `${courses.length} course${courses.length === 1 ? "" : "s"}`;
  els.activeFilterCount.textContent = count ? (isPt ? ` · ${count} ativo${count === 1 ? "" : "s"}` : ` · ${count} active`) : "";
  els.results.innerHTML = visible.map(renderCard).join("");
  els.empty.hidden = courses.length !== 0;
  els.showMore.hidden = visible.length >= courses.length;
  if (!els.showMore.hidden) {
    const remaining = courses.length - visible.length;
    els.showMore.textContent = isPt ? `Mostrar mais · ${remaining} restantes` : `Show more · ${remaining} remaining`;
  }
  updateQuickState(values);
}

function clearFilters(options = {}) {
  const { focusSearch = true } = options;
  els.filters.reset();
  els.sort.value = "recommendation";
  state.visibleLimit = 24;
  render();
  if (focusSearch) els.search.focus();
}

function togglePreset(control, value) {
  control.value = control.value === value ? "" : value;
}

function applyQuick(kind) {
  state.visibleLimit = 24;
  if (kind === "all") {
    clearFilters({ focusSearch: false });
    return;
  }
  if (kind === "pt-PT") togglePreset(els.language, "pt-PT");
  if (kind === "F0") togglePreset(els.access, "F0");
  if (kind === "beginner") togglePreset(els.level, "beginner-friendly");
  if (kind === "languages") togglePreset(els.category, "languages");
  render();
}

async function boot() {
  Object.assign(els, {
    filterDisclosure: document.querySelector("#filter-disclosure"),
    filters: document.querySelector("#filters"),
    activeFilterCount: document.querySelector("#active-filter-count"),
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
    statCourses: document.querySelector("#stat-courses"),
    statCategories: document.querySelector("#stat-categories"),
    statLanguages: document.querySelector("#stat-languages"),
  });

  try {
    const [catalogResponse, metaResponse] = await Promise.all([
      fetch(route("data/catalog.json")),
      fetch(route("data/meta.json")),
    ]);
    if (!catalogResponse.ok || !metaResponse.ok) throw new Error("Failed to load public data");

    state.courses = await catalogResponse.json();
    state.meta = await metaResponse.json();

    els.statCourses.textContent = state.meta.published_count;
    els.statCategories.textContent = state.meta.category_count;
    els.statLanguages.textContent = Object.keys(state.meta.language_counts).length;

    populateFilters();
    setFormState(new URLSearchParams(location.search));

    const resetAndRender = () => {
      state.visibleLimit = 24;
      render();
    };
    els.filters.addEventListener("input", resetAndRender);
    els.filters.addEventListener("change", resetAndRender);
    els.clear.addEventListener("click", () => clearFilters());
    els.showMore.addEventListener("click", () => {
      state.visibleLimit += 24;
      render();
    });

    document.querySelectorAll("[data-quick]").forEach((button) => {
      button.addEventListener("click", () => applyQuick(button.dataset.quick));
    });

    const mobile = window.matchMedia("(max-width: 700px)");
    const syncDisclosure = () => {
      if (mobile.matches) els.filterDisclosure.removeAttribute("open");
      else els.filterDisclosure.setAttribute("open", "");
    };
    syncDisclosure();
    mobile.addEventListener?.("change", syncDisclosure);

    render();
  } catch (error) {
    console.error(error);
    els.resultCount.textContent = isPt ? "Não foi possível carregar o catálogo." : "The catalogue could not be loaded.";
    els.empty.hidden = false;
    els.empty.querySelector("h3").textContent = isPt ? "Catálogo indisponível" : "Catalogue unavailable";
    els.empty.querySelector("p").textContent = isPt
      ? "Tenta novamente ou consulta o conjunto de dados canónico no GitHub."
      : "Please try again or use the canonical dataset on GitHub.";
  }
}

document.addEventListener("DOMContentLoaded", boot);
