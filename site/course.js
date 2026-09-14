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

const credentialLabels = {
  free_provider_certificate: "Free provider completion certificate",
  free_statement_of_participation: "Free statement of participation",
  academic_completion_route: "Academic completion route",
  paid_verified_certificate: "Paid verified certificate",
  none: "No free completion credential",
};

const creditLabels = {
  none: "No academic credit",
  none_by_default: "No academic credit by default",
  optional_paid_or_external: "Optional paid or external credit route",
  free_ects_available: "Free ECTS available",
  free_ects_available_subject_to_rules: "Free ECTS available subject to eligibility rules",
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

function courseHost(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "official provider";
  }
}

function displayCredential(course, review) {
  return review?.credential || credentialLabels[course.certificate] || humanize(course.certificate);
}

function displayCredit(course, review) {
  return review?.academic_credits || creditLabels[course.academic_credits] || humanize(course.academic_credits);
}

function readableId(value) {
  return String(value || "")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
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

  if (days > 30) return { label: "Current", tone: "good" };
  if (days >= 0) return { label: "Check due soon", tone: "warn" };
  if (days >= -30) return { label: "Check due", tone: "warn" };
  return { label: "Re-check priority", tone: "danger" };
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

function fact(label, value) {
  return `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`;
}

function render(course, allCourses) {
  const languages = [course.primary_language, ...course.other_languages]
    .map(labelLanguage)
    .join(" · ");
  const fresh = freshness(course);
  const editorial = course.editorial || {};
  const review = editorial.review || null;
  const admission = editorial.admission || null;
  const courseMap = new Map(allCourses.map((item) => [item.id, item]));

  document.title = `${course.title} · Open Learning Index`;
  document.querySelector('meta[name="description"]').setAttribute(
    "content",
    `${course.title} — ${course.why_recommended}`
  );

  document.querySelector("#course-title").textContent = course.title;
  document.querySelector("#course-provider").textContent = course.provider;
  document.querySelector("#course-why").textContent = course.why_recommended;

  const officialHero = document.querySelector("#official-course-hero");
  officialHero.href = course.url;
  officialHero.textContent = `Open on ${courseHost(course.url)} ↗`;
  document.querySelector("#detail-scores").innerHTML =
    scoreBlock("Recommendation", course.recommendation_score, course.recommendation_tier) +
    scoreBlock("Quality", course.quality_score, course.quality_tier);

  document.querySelector("#course-facts").innerHTML = [
    fact("Category", course.category_name),
    fact("Level", labelLevel(course.level)),
    fact("Language", languages),
    fact("Format", course.self_paced ? "Self-paced" : "Scheduled / not self-paced"),
    fact("Status", course.status === "active_archive" ? "Archived but still available" : "Active"),
  ].join("");

  const referencePanel = document.querySelector("#reference-note-panel");
  if (editorial.reference_note) {
    document.querySelector("#reference-note").textContent = editorial.reference_note;
    referencePanel.hidden = false;
  }

  const beforePanel = document.querySelector("#before-start-panel");
  const beforeFacts = [];
  if (review?.prerequisites) beforeFacts.push(fact("Prerequisites", review.prerequisites));
  if (review?.required_resources) beforeFacts.push(fact("Required resources", review.required_resources));
  if (beforeFacts.length || review?.scope_notes) {
    document.querySelector("#before-start").innerHTML = beforeFacts.join("");
    document.querySelector("#scope-notes").textContent = review?.scope_notes || "";
    beforePanel.hidden = false;
  }

  const access = document.querySelector("#access-summary");
  access.innerHTML = `
    <div class="access-callout">
      <strong>${escapeHtml(course.access_short)} · ${escapeHtml(course.access_label)}</strong>
      <p>${escapeHtml(course.access_description)}</p>
    </div>
    <dl class="facts">
      ${fact("Certificate", displayCredential(course, review))}
      ${fact("Academic credit", displayCredit(course, review))}
    </dl>
  `;

  const components = document.querySelector("#quality-components");
  components.innerHTML = Object.entries(course.quality_components)
    .map(([key, value]) => {
      const evidence = review?.component_evidence?.[key];
      return `
        <div class="component-item">
          <div class="component-row">
            <span>${escapeHtml(componentLabels[key] || humanize(key))}</span>
            <div class="component-meter" aria-hidden="true"><i style="width:${Number(value) * 10}%"></i></div>
            <strong>${Number(value).toFixed(1)}</strong>
          </div>
          ${evidence ? `<p class="component-evidence">${escapeHtml(evidence)}</p>` : ""}
        </div>
      `;
    })
    .join("");

  const scoreContextPanel = document.querySelector("#score-context-panel");
  const scoreParts = [];
  if (review?.recommendation_rationale) {
    scoreParts.push(`<h3>Recommendation rationale</h3><p>${escapeHtml(review.recommendation_rationale)}</p>`);
  }
  if (admission?.learning_need) {
    scoreParts.push(`<h3>Learning need</h3><p>${escapeHtml(admission.learning_need)}</p>`);
  }
  if (admission?.marginal_value) {
    scoreParts.push(`<h3>Why it adds value</h3><p>${escapeHtml(admission.marginal_value)}</p>`);
  }

  const comparisonIds = [...new Set([
    ...(admission?.comparison_set || []),
    ...(review?.comparators || []),
  ])].filter((id) => id && id !== course.id);

  if (comparisonIds.length) {
    const items = comparisonIds.map((id) => {
      const compared = courseMap.get(id);
      if (compared) {
        return `<li><a href="course.html?id=${encodeURIComponent(id)}">${escapeHtml(compared.title)}</a></li>`;
      }
      return `<li>${escapeHtml(readableId(id))}</li>`;
    }).join("");
    scoreParts.push(`<h3>Compared against</h3><ul class="comparison-list">${items}</ul>`);
  }

  if (admission?.decision_rationale) {
    scoreParts.push(`<details class="editorial-details"><summary>Admission decision rationale</summary><p>${escapeHtml(admission.decision_rationale)}</p></details>`);
  }

  if (scoreParts.length) {
    document.querySelector("#score-context").innerHTML = scoreParts.join("");
    scoreContextPanel.hidden = false;
  }

  document.querySelector("#verification-content").innerHTML = `
    <p><span class="freshness freshness-${fresh.tone}">${fresh.label}</span></p>
    <dl class="facts">
      ${fact("Last verified", formatDate(course.last_verified))}
      ${fact("Next review", formatDate(course.next_review))}
      ${fact("Review interval", `${course.review_interval_days} days`)}
    </dl>
  `;

  const evidence = document.querySelector("#evidence-list");
  const evidenceUrls = [...new Set([...(review?.evidence || []), ...(course.evidence || [])])];
  evidence.innerHTML = evidenceUrls
    .map((url, index) => {
      const host = courseHost(url);
      return `<li><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(host)} · source ${index + 1} ↗</a></li>`;
    })
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

    render(course, courses);
  } catch (error) {
    console.error(error);
    document.querySelector("#detail-loading").hidden = true;
    document.querySelector("#detail-error").hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", boot);
