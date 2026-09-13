# Phase 5 QA — primary-source re-verification 01

## Scope

Re-verify ten high-volatility technical reference fixtures whose scheduled review dates fall in November/December 2026.

This is a metadata/currentness QA pass, not a re-scoring exercise.

## Result

**10 / 10 re-verified from current primary sources.**

No publication blocker and no canonical removal was found.

Canonical `last_verified` is advanced to **2026-09-13** for all ten records. Existing review intervals are preserved:

- 60-day records → next review **2026-11-12**;
- 90-day records → next review **2026-12-12**.

## CS50 family

### CS50x
Current official 2026 route remains live and free, with problem sets and a final project.

The official certificate page confirms that learners meeting the required score threshold can receive a **free CS50 Certificate**; the optional edX verified certificate remains separate.

Primary evidence:
- https://cs50.harvard.edu/x/
- https://cs50.harvard.edu/x/certificate/

### CS50P
Current free course remains live with problem sets and a final project.

The official certificate page confirms a free CS50 completion certificate for successful learners.

Primary evidence:
- https://cs50.harvard.edu/python/
- https://cs50.harvard.edu/python/certificate/

### CS50 AI
Current free route remains active, project-heavy and explicitly includes modern AI topics including large language models.

Free CS50 certificate mechanics remain documented.

Primary evidence:
- https://cs50.harvard.edu/ai/
- https://cs50.harvard.edu/ai/certificate/

### CS50 SQL
Current free route remains active across querying, schema design, optimisation/scaling and a final project.

Free CS50 certificate mechanics remain documented.

Primary evidence:
- https://cs50.harvard.edu/sql/
- https://cs50.harvard.edu/sql/certificate/

## University of Helsinki

### Full Stack Open
The official course remains continuously maintained rather than tied to a yearly edition.

Current general information confirms:
- the course is totally free;
- the certificate is free;
- University of Helsinki ECTS credits are available without tuition for the course route;
- current technical maintenance includes 2025/2026 dependency/framework updates.

Primary evidence:
- https://fullstackopen.com/en/
- https://fullstackopen.com/en/part0/general_info/

### Python Programming MOOC 2026
The current 2026 course remains open through the end of 2026 and exposes current September 2026 lecture activity.

The official FAQ confirms:
- the MOOC is free of charge and open to all;
- learners can complete it without prior university enrolment;
- passing the exercises + exam yields a completion certificate;
- learners can optionally register the completion for University of Helsinki study credits.

Primary evidence:
- https://programming-26.mooc.fi/
- https://programming-26.mooc.fi/faq/
- https://programming-26.mooc.fi/grading-and-exams/

No change is required to the existing `F0_FULL_CREDENTIAL` / `academic_completion_route` representation.

## PortSwigger Web Security Academy

The Academy remains active, continuously updated and free for learning/labs.

The separate Burp Suite Certified Practitioner credential still requires:
- purchase of an exam credit;
- an active Burp Suite Professional subscription.

This confirms that the canonical course should remain:
- `F1_FULL_ASSESSMENTS`;
- `paid_external_exam_only`.

Primary evidence:
- https://portswigger.net/web-security
- https://portswigger.net/web-security/certification
- https://portswigger.net/web-security/certification/frequently-asked-questions

## Google Machine Learning Crash Course

The official route remains active and hands-on, with current material covering production ML, large language models, fairness and browser exercises.

The Portuguese-Brazil route remains live and materially translated, so `pt-BR` remains verified as an alternate instructional language.

No completion certificate is documented on the current course route.

Primary evidence:
- https://developers.google.com/machine-learning/crash-course
- https://developers.google.com/machine-learning/crash-course?hl=pt-br

## OpenAI Academy — Agents & Workflows

OpenAI's current Help Center states that Academy courses are:
- free;
- self-paced;
- globally available to anyone with a ChatGPT account;
- assessment-bearing;
- associated with course recognition/badges and eligible completion pathways.

The current OpenAI Academy catalog still lists **Agents & Workflows** as a structured course, and public issued completion records for this course remain live.

Primary evidence:
- https://openai.com/academy/
- https://help.openai.com/en/articles/20001270-openai-academy-courses
- https://academy.openai.com/public/courses/agents-and-workflows-bieml

The existing free-access classification remains valid. Recognition terminology should continue to be monitored because the Academy now distinguishes course badges from pathway certificates in some documentation.

## Kaggle — Intro to Machine Learning

The course remains active in Kaggle Learn in 2026.

Current first-party evidence confirms:
- Kaggle Learn courses remain no-cost;
- completion certificates are still issued;
- Intro to Machine Learning certificates were issued repeatedly in 2026, including August 2026.

Primary evidence:
- https://www.kaggle.com/learn/intro-to-machine-learning

The current canonical `F0_FULL_CREDENTIAL` representation remains defensible.

## Metadata changes

For these ten records:
- `last_verified` → 2026-09-13;
- `next_review` recalculated from the existing interval;
- primary evidence arrays strengthened with current official verification URLs.

No score, quality component, access tier, provider, category or recommendation score changes are made.

## Next gate

Continue targeted primary-source re-verification with the next high-volatility canonical records, prioritising:
- current software/tooling admissions;
- cybersecurity pathways;
- marketing AI/search tooling;
- engineering vendor tooling;
- current clinical/legal courses.

Broad discovery remains paused.
