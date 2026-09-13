# Phase 5 QA — primary-source re-verification 04

## Scope

Re-verify the complete **Law & Public Policy** canonical set against current first-party sources:

- Saylor BUS205: Business Law;
- WIPO DL-101 General Course on Intellectual Property;
- Council of Europe HELP — Artificial Intelligence and Human Rights;
- Council of Europe HELP — Cybercrime and Electronic Evidence;
- Council of Europe HELP — Data Protection and Privacy Rights.

Legal-currentness, jurisdiction scope, current enrolment/access and exact credential mechanics receive elevated weight in this gate.

## Result

**5 / 5 records retained.**

No Quality Score, Recommendation Score, category or access-tier change is required.

Publication-metadata corrections:

- WIPO DL-101 gains four verified standard-course languages: **fr, ar, ru, es**;
- HELP Cybercrime gains fourteen currently listed alternate self-learning languages;
- all three HELP records change credential label from the generic `free_provider_certificate` to the provider-exact `free_statement_of_accomplishment`.

The canonical set remains **129**.

## Saylor — BUS205: Business Law

The current syllabus remains a 39-hour, self-paced US business-law foundation covering sources/courts, ADR, torts, contracts, property, intellectual property, employment, business crime, organisations and regulation.

Saylor currently states that:

- all course materials are free;
- the Certificate Final Exam is free;
- a free completion certificate is available at the 70% passing threshold;
- the optional ACE Recommended Credit Final Exam requires external proctoring and a $5 fee;
- the course is explicitly grounded in United States law.

This confirms the existing split between free course completion and optional paid/external college-credit mechanics.

Primary evidence:

- https://learn.saylor.org/course/bus205
- https://learn.saylor.org/mod/page/view.php?id=89920

Decision: retain `F0_FULL_CREDENTIAL`, `free_provider_certificate`, `optional_paid_or_external`, self-paced status and current scores. Advance `last_verified` to 2026-09-13.

## WIPO Academy — DL-101 General Course on Intellectual Property

The current WIPO Academy catalog confirms the 2026 English DL-101 version as:

- online;
- 55 hours;
- free of charge;
- certificate-bearing;
- final-exam based;
- repeated in scheduled sessions rather than continuously available year-round.

This validates the existing `self_paced: false` publication metadata: the course is learner-directed within a session, but access and assessment are cohort-windowed.

### Language correction

The current 2026 WIPO catalog also exposes standard 55-hour DL-101 editions in:

- French;
- Arabic;
- Russian;
- Spanish.

These are sufficiently equivalent to the canonical general DL-101 learning role to record as alternate instructional versions.

WIPO also exposes customised regional editions, including a 75-hour Portuguese-Brazilian course and other jurisdiction-adapted variants. Those are **not** merged into `other_languages` here because equivalence to the standard 55-hour course is not established merely by the shared DL-101 family name.

Primary evidence:

- https://welc.wipo.int/acc/index.jsf?lang=en&page=wipoDLCatalog.xhtml
- https://welc.wipo.int/acc/index.jsf?lang=fr&page=wipoDLCatalog.xhtml
- https://welc.wipo.int/acc/index.jsf?lang=es&page=wipoDLCatalog.xhtml
- https://www.wipo.int/edocs/pubdocs/en/training/468/wipo_pub_468.pdf

Decision: retain F0, free WIPO certificate, scheduled-session caveat and scores; add `fr, ar, ru, es`; advance verification to 2026-09-13.

## Council of Europe HELP — Artificial Intelligence and Human Rights

The official current course remains a six-hour self-learning route. It was developed in 2024 and comprehensively updated in 2025 around the Council of Europe Framework Convention on AI, HUDERIA and related European/international standards.

The course still uses presentations, interactive screens, knowledge tests and reflective exercises. Completion generates an electronic **Statement of Accomplishment**.

The Council of Europe reported in 2026 that the course remains current and is actively used in HELP programmes. Current public material says the self-learning version is in English and that translations have been initiated; this does not yet justify adding unverified translated versions to canonical language metadata.

Primary evidence:

- https://www.coe.int/en/web/artificial-intelligence/-/updated-help-online-course-on-artificial-intelligence-and-human-rights-is-now-available-and-opened-for-enrolment-to-interested-participants
- https://www.coe.int/web/help/-/justice-professionals-tackle-challenges-related-to-ai
- https://help.elearning.ext.coe.int/enrol/index.php?id=7331

Decision: retain F0 and scores; correct credential taxonomy to `free_statement_of_accomplishment`.

## Council of Europe HELP — Cybercrime and Electronic Evidence

Council of Europe sources continue to expose the course as an open, self-paced HELP route with completion recognition. The current 2026 HELP network documentation identifies Cybercrime as an updated course.

The current Council of Europe cybercrime training page lists the HELP course in:

- English;
- Arabic;
- Azerbaijani;
- Bulgarian;
- Czech;
- French;
- Hungarian;
- Armenian;
- Georgian;
- Portuguese;
- Romanian;
- Slovak;
- Spanish;
- Ukrainian;
- Turkish.

Canonical English remains the primary language. The fourteen non-English versions are added to `other_languages`.

Completion terminology is an electronic **Statement of Accomplishment**, not a generic certificate in the public self-learning route.

Primary evidence:

- https://www.coe.int/en/web/cybercrime/-/council-of-europe-help-online-course-on-cybercrime-and-electronic-evidence
- https://www.coe.int/en/web/octopus/training
- https://www.coe.int/en/web/help/-/2026-help-annual-network-conference-in-strasbourg-conference-report

Decision: retain F0 and current scores; add verified languages and correct credential taxonomy.

## Council of Europe HELP — Data Protection and Privacy Rights

The Council of Europe explicitly presented Data Protection and Privacy Rights as an updated HELP course at the 2026 Network Conference, preserving the key legal-currentness signal used in Phase 3/4.

Current public detailed materials continue to support:

- free self-learning access;
- European data-protection/privacy framework coverage;
- interactive professional learning;
- electronic Statement of Accomplishment after completion.

Older HELP pages document many translated versions, but the 2026 revision is not publicly mapped language-by-language. To avoid conflating older translations with the newest revision, canonical `other_languages` remains empty until current equivalence is directly verified.

Primary evidence:

- https://www.coe.int/en/web/help/help-courses
- https://www.coe.int/en/web/help/-/2026-help-annual-network-conference-in-strasbourg-conference-report
- https://www.coe.int/en/web/help/-/data-protection-and-privacy-rights-council-of-europe-help-course-for-latvian-and-portuguese-legal-professionals

Decision: retain F0, English primary route and scores; correct credential taxonomy to `free_statement_of_accomplishment`.

## Structural reconciliation

The new verified alternate-language records raise courses with alternate instruction languages from **4 to 6**.

Key all-route language counts become:

- English — 120;
- French — 9;
- Spanish — 4;
- Arabic — 3;
- generic Portuguese — 3;
- Russian — 2;
- plus newly represented Azerbaijani, Bulgarian, Czech, Hungarian, Armenian, Georgian, Romanian, Slovak, Turkish and Ukrainian.

The primary-instruction concentration does **not** change: 120 / 129 courses remain primarily English.

Credential distribution is also corrected without changing F0/F1/F2 access counts:

- no formal free credential — 55;
- free provider certificate — 41;
- free badge — 12;
- free badge + statement — 8;
- free statement of participation — 6;
- free Statement of Accomplishment — 3;
- other explicit credential models — 4.

## Next gate

Continue Phase 5 Gate 3 with **session/cohort-dependent and version-fragile records**.

WIPO DL-101 has already been checked in this batch, so the next pass should avoid duplicating it and focus on the remaining canonical records whose availability or completion route depends on a live cohort/session, annual version, closing window, hardware/software version or provider platform state.

After that pass: final publication-readiness gate.

Broad discovery remains paused.
