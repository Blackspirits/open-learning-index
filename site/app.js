const state = {
  courses: [],
  meta: null,
};

const els = {};

const languageNames = {
  "ar": "Arabic",
  "de": "German",
  "en": "English",
  "es": "Spanish",
  "fr": "French",
  "ja": "Japanese",
  "pt-BR": "Português (Brasil)",
  "pt-PT": "Português (Portugal)",
  "zh": "Chinese",
};

function labelLanguage(code) {
  return languageNames[code] || code;
}

function labelLevel(value) {
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

function parseDateOnly(value) {
  return new Date(value + "T00:00:00Z");
}

function freshness(course) {
  const now = new Date();
  const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  const next = parseDateOnly(course.next_review).getTime();
  const days = Math.ceil((next - today) / 86400000);

  if (days > 30) return { label: "Verified", tone: "good" };
  if (days >= 0) return { label: "Review due soon", tone: "warn" };
  if (days >= -30) return { label: "Review due", tone: "warn" };
  return { label: "Priority re-review", tone: "danger" };
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(parseDateOnly(value));
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
    sort: els.sort.value,
    credential: els.credential.checked,
  };
}

function setFormState(params) {
  els.search.value = params.get("q") || "";
  els.category.value = params.get("category") || "";
  els.language.value = params.get("language") || "";
  els.level.value = params.get("level") || "";
  els.access.value = params.get("access") || "";
  els.tier.value = params.get("tier") || "";
  els.sort.value = params.get("sort") || "recommendation";
  els.credential.checked = params.get("credential") === "1";
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
  const categories = [...new Map(state.courses.map((c) => [c.category, c.category_name])).entries()]
    .sort((a, b) => a[1].localeCompare(b[1]));
  const languages = [...new Set(state.courses.flatMap((c) => [c.primary_language, ...c.other_languages]))]
    .sort((a, b) => labelLanguage(a).localeCompare(labelLanguage(b)));
  const levels = [...new Set(state.courses.map((c) => c.level))]
    .sort((a, b) => labelLevel(a).localeCompare(labelLevel(b)));

  for (const [value, label] of categories) {
    els.category.add(new Option(label, value));
  }
  for (const value of languages) {
    els.language.add(new Option(labelLanguage(value), value));
  }
  for (const value of levels) {
    els.level.add(new Option(labelLevel(value), value));
  }
}

function filteredCourses(values) {
  const query = normalize(values.q);
  const words = query.split(/\s+/).filter(Boolean);

  const list = state.courses.filter((course) => {
    if (words.length && !words.every((word) => course.search_text.includes(word))) return false;
    if (values.category && course.category !== values.category) return false;
    if (values.language && course.primary_language !== values.language && !course.other_languages.includes(values.language)) return false;
    if (values.level && course.level !== values.level) return false;
    if (values.access && course.access_short !== values.access) return false;
    if (values.tier && course.quality_tier !== values.tier) return false;
    if (values.credential && !course.has_free_credential) return false;
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
  const languages = [course.primary_language, ...course.other_languages]
    .map(labelLanguage)
    .join(" · ");

  const archive = course.status === "active_archive"
    ? '<span class="badge badge-neutral">Active archive</span>'
    : "";

  const credit = course.has_free_academic_credit
    ? '<span class="badge badge-credit">Free academic credit</span>'
    : "";

  return `
    <article class="course-card">
      <div class="card-topline">
        <span class="category">${escapeHtml(course.category_name)}</span>
        <span class="freshness freshness-${fresh.tone}">${escapeHtml(fresh.label)}</span>
      </div>

      <div>
        <h3><a href="course.html?id=${encodeURIComponent(course.id)}">${escapeHtml(course.title)}</a></h3>
        <p class="provider">${escapeHtml(course.provider)}</p>
      </div>

      <div class="badges">
        <span class="badge">${escapeHtml(labelLevel(course.level))}</span>
        <span class="badge">${escapeHtml(languages)}</span>
        <span class="badge badge-access" title="${escapeHtml(course.access_description)}">${escapeHtml(course.access_short)} · ${escapeHtml(course.access_label)}</span>
        ${archive}
        ${credit}
      </div>

      <div class="scores" aria-label="Course scores">
        ${scoreBlock("Recommendation", course.recommendation_score, course.recommendation_tier)}
        ${scoreBlock("Quality", course.quality_score, course.quality_tier)}
      </div>

      <p class="why">${escapeHtml(course.why_recommended)}</p>

      <div class="card-footer">
        <span>Verified ${escapeHtml(formatDate(course.last_verified))}</span>
        <a href="${escapeHtml(course.url)}" target="_blank" rel="noopener noreferrer">Open course <span aria-hidden="true">↗</span></a>
      </div>
    </article>
  `;
}

function render() {
  const values = getFormState();
  syncUrl(values);
  const courses = filteredCourses(values);

  els.resultCount.textContent = `${courses.length} course${courses.length === 1 ? "" : "s"}`;
  els.results.innerHTML = courses.map(renderCard).join("");
  els.empty.hidden = courses.length !== 0;
}

function clearFilters() {
  els.filters.reset();
  els.sort.value = "recommendation";
  render();
  els.search.focus();
}

function applyQuick(kind) {
  clearFilters();
  if (kind === "pt-PT") els.language.value = "pt-PT";
  if (kind === "F0") els.access.value = "F0";
  if (kind === "beginner") {
    const beginner = [...els.level.options].find((option) => option.value === "beginner");
    if (beginner) els.level.value = "beginner";
  }
  render();
}

async function boot() {
  Object.assign(els, {
    filters: document.querySelector("#filters"),
    search: document.querySelector("#search"),
    category: document.querySelector("#category"),
    language: document.querySelector("#language"),
    level: document.querySelector("#level"),
    access: document.querySelector("#access"),
    tier: document.querySelector("#tier"),
    sort: document.querySelector("#sort"),
    credential: document.querySelector("#credential"),
    clear: document.querySelector("#clear-filters"),
    results: document.querySelector("#results"),
    resultCount: document.querySelector("#result-count"),
    empty: document.querySelector("#empty-state"),
    statCourses: document.querySelector("#stat-courses"),
    statCategories: document.querySelector("#stat-categories"),
    statLanguages: document.querySelector("#stat-languages"),
  });

  try {
    const [catalogResponse, metaResponse] = await Promise.all([
      fetch("data/catalog.json"),
      fetch("data/meta.json"),
    ]);
    if (!catalogResponse.ok || !metaResponse.ok) throw new Error("Failed to load public data");

    state.courses = await catalogResponse.json();
    state.meta = await metaResponse.json();

    els.statCourses.textContent = state.meta.published_count;
    els.statCategories.textContent = state.meta.category_count;
    els.statLanguages.textContent = Object.keys(state.meta.language_counts).length;

    populateFilters();
    setFormState(new URLSearchParams(location.search));

    els.filters.addEventListener("input", render);
    els.filters.addEventListener("change", render);
    els.clear.addEventListener("click", clearFilters);

    document.querySelectorAll("[data-quick]").forEach((button) => {
      button.addEventListener("click", () => applyQuick(button.dataset.quick));
    });

    render();
  } catch (error) {
    console.error(error);
    els.resultCount.textContent = "The catalogue could not be loaded.";
    els.empty.hidden = false;
    els.empty.querySelector("h3").textContent = "Catalogue unavailable";
    els.empty.querySelector("p").textContent = "Please try again or use the canonical dataset on GitHub.";
  }
}

document.addEventListener("DOMContentLoaded", boot);
