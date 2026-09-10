# Shallow Screening 01 — 2026-09-10

## Purpose

This is the first real elimination gate after discovery. Shallow screening does **not** assign 0–10 quality scores. It asks whether a candidate is sufficiently current, complete, genuinely free and well evidenced to justify an expensive deep review.

Decision meanings:

- `advance` — survives the shallow gate and becomes eligible for deep review;
- `hold` — potentially strong, but an unresolved access/evidence issue prevents advancement;
- `reject` — fails an exclusion criterion and should not consume deep-review effort unless new evidence appears.

Screening evidence is stored separately from discovery data in `data/screening/` so the historical fact that a course was considered is never erased.

## Tranche

This calibration tranche screens **15 candidates** from two already competitive areas: Cybersecurity & IT and AI & Data.

| Provider/group | Screened | Advance | Hold | Reject |
|---|---:|---:|---:|---:|
| Cisco Networking Academy | 8 | 8 | 0 | 0 |
| Fortinet Training Institute | 2 | 1 | 1 | 0 |
| Kaggle Learn | 5 | 5 | 0 | 0 |
| **Total** | **15** | **14** | **1** | **0** |

## Advances

### Cisco Networking Academy

The following eight candidates advance because current Cisco curriculum evidence documents complete self-paced learning paths with meaningful labs/activities, assessment and digital-badge recognition:

- Networking Basics
- Networking Devices and Initial Configuration
- Operating Systems Basics
- Introduction to Cybersecurity
- Endpoint Security
- Network Defense
- Cyber Threat Management
- Ethical Hacker

The deeper review must still decide whether several sequential Cisco courses belong individually in a final global index or whether only the strongest course/pathway representation survives head-to-head redundancy testing.

### Kaggle Learn

Five compact applied courses advance:

- Pandas
- Data Visualization
- Intro to SQL
- Advanced SQL
- Intermediate Machine Learning

Their short duration is not an automatic weakness. Deep review must compare practice density and learning outcomes against longer courses and decide whether individual micro-courses or a broader pathway representation is more useful to the final index.

### Fortinet Networking Fundamentals

This candidate advances as a concise, complete free networking foundation with course-completion recognition. It has no certification exam, which is explicitly separated from the free learning credential.

## Hold

### FortiGate Operator

The current course remains pedagogically plausible and includes interactive simulations and assessment. However, the 2026 Fortinet NSE structure ties badge/certification progression to an associated online exam. The research found strong indications but not sufficiently explicit primary evidence that this exam is currently zero-cost for the general public.

Result: **hold at F1**, with `credential-cost-unconfirmed` flagged. It can advance immediately if explicit current evidence confirms the complete credential path is free; alternatively it can still compete as F1 if the final methodology determines the free course path itself is sufficiently exceptional.

## What this tranche teaches us

1. **Screening needs its own immutable evidence ledger.** Overwriting discovery rows would lose decision history.
2. **Pathway redundancy is a first-class problem.** A provider can offer eight individually good sequential courses without all eight deserving final-list slots.
3. **Credential claims need stronger evidence than course-access claims.** A free course does not imply a free exam or certification.
4. **Compact courses must be judged by learning density, not duration alone.** Kaggle is the calibration case for this rule.
5. **No rejects in a calibration tranche is acceptable.** These 15 were intentionally selected from high-confidence candidates to validate the screening model; later screens should include ambiguous and weak records and are expected to reject more aggressively.

## Next screening tranche

Screen saturated categories in larger mixed-provider blocks and deliberately include weaker/ambiguous candidates. Priority should be:

1. AI & Data beyond Kaggle;
2. Cybersecurity & IT beyond Cisco/Fortinet;
3. Marketing & Sales;
4. Business & Entrepreneurship;
5. Psychology & Behaviour, with aggressive currency checks.

The objective is not to maximise advancement. It is to reduce the 286-candidate research pool to the smallest set that can plausibly produce a world-class final Top 100–150.
