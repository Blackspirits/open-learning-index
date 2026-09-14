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

const componentLabels = {
  pedagogy: "Pedagogy",
  depth: "Depth",
  practice: "Practice",
  materials: "Materials",
  currency: "Currency",
  expertise: "Expertise",
  accessibility: "Accessibility",
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

function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function parseDateOnly(value) {
  return new Date(value + "T00:00:00Z");
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }).format(parseDateOnly(value));
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

function scoreBlock(label, score, tier) {
  return `
    <div class="score">
      <span>${label}</span>
      <strong>${Number(score).toFixed(1)}</strong>
      <small>${tier}</small>
    </div>
  `;
}

function fact(label, value) {
  return `<div><dt>${label}</dt><dd>${value}</dd></div>`;
}

function render(course) {
  const languages = [course.primary_language, ...course.other_languages]
    .map(labelLanguage)
    .join(" · ");
  const fresh = freshness(course);

  document.title = `${course.title} · Open Learning Index`;
  document.querySelector('meta[name="description"]').setAttribute(
    "content",
    `${course.title} — ${course.why_recommended}`
  );

  document.querySelector("#course-title").textContent = course.title;
  document.querySelector("#course-provider").textContent = course.provider;
  document.querySelector("#course-why").textContent = course.why_recommended;
  document.querySelector("#detail-scores").innerHTML =
    scoreBlock("Recommendation", course.recommendation_score, course.recommendation_tier) +
    scoreBlock("Quality", course.quality_score, course.quality_tier);

  document.querySelector("#course-facts").innerHTML = [
    fact("Category", course.category_name),
    fact("Level", labelLevel(course.level)),
    fact("Language", languages),
    fact("Format", course.self_paced ? "Self-paced" : "Scheduled / not self-paced"),
    fact("Status", humanize(course.status)),
  ].join("");

  const access = document.querySelector("#access-summary");
  access.innerHTML = `
    <div class="access-callout">
      <strong>${course.access_short} · ${course.access_label}</strong>
      <p>${course.access_description}</p>
    </div>
    <dl class="facts">
      ${fact("Certificate", humanize(course.certificate))}
      ${fact("Academic credit", humanize(course.academic_credits))}
    </dl>
  `;

  const components = document.querySelector("#quality-components");
  components.innerHTML = Object.entries(course.quality_components)
    .map(([key, value]) => `
      <div class="component-row">
        <span>${componentLabels[key] || humanize(key)}</span>
        <div class="component-meter" aria-hidden="true"><i style="width:${Number(value) * 10}%"></i></div>
        <strong>${Number(value).toFixed(1)}</strong>
      </div>
    `)
    .join("");

  document.querySelector("#verification-content").innerHTML = `
    <p><span class="freshness freshness-${fresh.tone}">${fresh.label}</span></p>
    <dl class="facts">
      ${fact("Last verified", formatDate(course.last_verified))}
      ${fact("Next review", formatDate(course.next_review))}
      ${fact("Review interval", `${course.review_interval_days} days`)}
    </dl>
  `;

  const evidence = document.querySelector("#evidence-list");
  evidence.innerHTML = course.evidence
    .map((url, index) => `<li><a href="${url}" target="_blank" rel="noopener noreferrer">Evidence source ${index + 1} ↗</a></li>`)
    .join("");

  const official = document.querySelector("#official-course");
  official.href = course.url;

  document.querySelector("#detail-loading").hidden = true;
  document.querySelector("#detail-content").hidden = false;
}

async function boot() {
  const id = new URLSearchParams(location.search).get("id");
  if (!id) {
    document.querySelector("#detail-loading").hidden = true;
    document.querySelector("#detail-error").hidden = false;
    return;
  }

  try {
    const response = await fetch("data/catalog.json");
    if (!response.ok) throw new Error("Failed to load catalogue");
    const courses = await response.json();
    const course = courses.find((item) => item.id === id);

    if (!course) {
      document.querySelector("#detail-loading").hidden = true;
      document.querySelector("#detail-error").hidden = false;
      return;
    }

    render(course);
  } catch (error) {
    console.error(error);
    document.querySelector("#detail-loading").hidden = true;
    document.querySelector("#detail-error").hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", boot);
