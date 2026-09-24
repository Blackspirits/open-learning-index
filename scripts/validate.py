#!/usr/bin/env python3
import json, sys, subprocess, tempfile, re
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
COURSES=ROOT/'data/courses.json'
COURSE_SCHEMA=ROOT/'data/course.schema.json'
CATEGORIES=ROOT/'data/categories.json'
LEGACY_CANDIDATES=ROOT/'data/candidates.json'
CANDIDATE_DIR=ROOT/'data/candidates'
CANDIDATE_SCHEMA=ROOT/'data/candidate.schema.json'
SCREENING_DIR=ROOT/'data/screening'
SCREENING_SCHEMA=ROOT/'data/screening.schema.json'
DEEP_REVIEW_DIR=ROOT/'data/reviews'
DEEP_REVIEW_SCHEMA=ROOT/'data/deep-review.schema.json'
REFERENCE_REVIEWS=ROOT/'data/reference-reviews.json'
REFERENCE_REVIEW_SCHEMA=ROOT/'data/reference-review.schema.json'
ADMISSION_DIR=ROOT/'data/admissions'
ADMISSION_SCHEMA=ROOT/'data/admission.schema.json'
WEIGHTS={'pedagogy':0.25,'depth':0.20,'practice':0.20,'materials':0.10,'currency':0.10,'expertise':0.10,'accessibility':0.05}
LANGUAGE_TAG=re.compile(r'^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$')

def fail(msg):
    print(f'ERROR: {msg}', file=sys.stderr); return 1

def validate_schema(data, schema_path, label):
    try:
        import jsonschema
        validator=jsonschema.Draft202012Validator(
            json.loads(schema_path.read_text(encoding='utf-8')),
            format_checker=jsonschema.FormatChecker(),
        )
        errors=sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
        if not errors:
            return 0
        total=0
        for error in errors:
            path='.'.join(map(str,error.absolute_path)) or '<root>'
            total += fail(f'{label} schema validation failed at {path}: {error.message}')
        return total
    except ModuleNotFoundError:
        print('NOTE: jsonschema not installed; running invariant checks only.')
        return 0

def load_candidate_sources():
    paths=[]
    if LEGACY_CANDIDATES.exists():
        paths.append(LEGACY_CANDIDATES)
    if CANDIDATE_DIR.exists():
        paths.extend(sorted(CANDIDATE_DIR.glob('*.json')))
    return paths

def load_screening_sources():
    if not SCREENING_DIR.exists():
        return []
    return sorted(SCREENING_DIR.glob('*.json'))

def load_deep_review_sources():
    if not DEEP_REVIEW_DIR.exists():
        return []
    return sorted(DEEP_REVIEW_DIR.glob('*.json'))

def load_admission_sources():
    if not ADMISSION_DIR.exists():
        return []
    return sorted(ADMISSION_DIR.glob('*.json'))

def validate_readme_snapshot(courses, current_screen_decisions, current_review_candidate_ids, current_admission_candidate_ids):
    if not README.exists():
        return fail('README.md is missing')

    metrics={}
    for line in README.read_text(encoding='utf-8').splitlines():
        match=re.fullmatch(r'\\|\\s*(.*?)\\s*\\|\\s*\\*\\*(.*?)\\*\\*\\s*\\|', line)
        if match:
            metrics[match.group(1)]=match.group(2)

    advances={cid for cid,decision in current_screen_decisions.items() if decision=='advance'}
    expected={
        'Canonical published courses': str(len(courses)),
        'Primary-language pt-PT courses': str(sum(c['primary_language']=='pt-PT' for c in courses)),
        'Alternate pt-BR routes': str(sum('pt-BR' in c.get('other_languages', []) for c in courses)),
        'Portuguese alternates with unresolved regional variant': str(sum('pt' in c.get('other_languages', []) for c in courses)),
        'F0 — full course + free credential': str(sum(c['free_access']=='F0_FULL_CREDENTIAL' for c in courses)),
        'F1 — full assessed learning path': str(sum(c['free_access']=='F1_FULL_ASSESSMENTS' for c in courses)),
        'F2 — full teaching content': str(sum(c['free_access']=='F2_CONTENT_ONLY' for c in courses)),
        'Current advances Deep-Reviewed': f'{len(advances & current_review_candidate_ids)} / {len(advances)}',
        'Current advances Phase-4 decided': f'{len(advances & current_admission_candidate_ids)} / {len(advances)}',
        'Holds excluded pending evidence': str(sum(decision=='hold' for decision in current_screen_decisions.values())),
    }

    errors=0
    for label,expected_value in expected.items():
        actual=metrics.get(label)
        if actual is None:
            errors += fail(f'README current-publication metric missing: {label}')
        elif actual != expected_value:
            errors += fail(f'README current-publication metric {label!r} is {actual!r}, expected {expected_value!r}')
    return errors

def main():
    errors=0
    courses=json.loads(COURSES.read_text(encoding='utf-8'))
    categories=json.loads(CATEGORIES.read_text(encoding='utf-8'))
    category_ids=[c['id'] for c in categories]
    if len(category_ids) != len(set(category_ids)):
        errors += fail('duplicate category id in data/categories.json')
    allowed_categories=set(category_ids)

    errors += validate_schema(courses, COURSE_SCHEMA, 'courses')

    candidate_sources=load_candidate_sources()
    candidates=[]
    for source in candidate_sources:
        batch=json.loads(source.read_text(encoding='utf-8'))
        label=f'candidates:{source.relative_to(ROOT)}'
        errors += validate_schema(batch, CANDIDATE_SCHEMA, label)
        candidates.extend(batch)

    ids=set(); urls=set()
    for c in courses:
        if c['category'] not in allowed_categories:
            errors += fail(f'{c["id"]}: unknown course category {c["category"]}')
        if c['id'] in ids: errors += fail(f'duplicate course id: {c["id"]}')
        ids.add(c['id'])
        language_codes=[c['primary_language'], *c.get('other_languages', [])]
        for language_code in language_codes:
            if not LANGUAGE_TAG.fullmatch(language_code):
                errors += fail(f'{c["id"]}: invalid language tag {language_code}')
        if c['primary_language'] == 'pt':
            errors += fail(f'{c["id"]}: published primary Portuguese must resolve to pt-PT or pt-BR')
        if 'pt' in c.get('other_languages', []) and not c.get('language_notes'):
            errors += fail(f'{c["id"]}: generic pt alternate requires language_notes explaining unresolved regional variant')
        if c['primary_language'] in c.get('other_languages', []):
            errors += fail(f'{c["id"]}: primary language duplicated in other_languages')
        if c['url'] in urls: errors += fail(f'duplicate course canonical URL: {c["url"]}')
        urls.add(c['url'])
        calc=round(sum(c['quality_components'][k]*w for k,w in WEIGHTS.items()),2)
        if abs(calc-c['quality_score'])>0.01:
            errors += fail(f'{c["id"]}: quality_score={c["quality_score"]}, expected {calc}')
        if date.fromisoformat(c['next_review']) < date.fromisoformat(c['last_verified']):
            errors += fail(f'{c["id"]}: next_review precedes last_verified')

    candidate_ids=set(); candidate_urls=set()
    for c in candidates:
        if c['category'] not in allowed_categories:
            errors += fail(f'{c["id"]}: unknown candidate category {c["category"]}')
        if c['id'] in candidate_ids: errors += fail(f'duplicate candidate id across candidate pool: {c["id"]}')
        candidate_ids.add(c['id'])
        if c['url'] in candidate_urls: errors += fail(f'duplicate candidate canonical URL across candidate pool: {c["url"]}')
        candidate_urls.add(c['url'])

    screening_sources=load_screening_sources()
    screenings=[]
    for source in screening_sources:
        records=json.loads(source.read_text(encoding='utf-8'))
        label=f'screening:{source.relative_to(ROOT)}'
        errors += validate_schema(records, SCREENING_SCHEMA, label)
        screenings.extend(records)

    screen_ids=set(); current_candidate_ids=set(); current_screen_decisions={}
    all_screen_ids={s.get('screen_id') for s in screenings}
    for s in screenings:
        sid=s['screen_id']
        cid=s['candidate_id']
        if sid in screen_ids:
            errors += fail(f'duplicate screening id: {sid}')
        screen_ids.add(sid)
        if cid not in candidate_ids:
            errors += fail(f'{sid}: screening references unknown candidate {cid}')
        if s['is_current']:
            if cid in current_candidate_ids:
                errors += fail(f'multiple current screenings for candidate: {cid}')
            current_candidate_ids.add(cid)
            current_screen_decisions[cid]=s['decision']
        supersedes=s.get('supersedes_screen_id')
        if supersedes and supersedes not in all_screen_ids:
            errors += fail(f'{sid}: supersedes unknown screening {supersedes}')
        if supersedes == sid:
            errors += fail(f'{sid}: cannot supersede itself')

    review_sources=load_deep_review_sources()
    reviews=[]
    for source in review_sources:
        records=json.loads(source.read_text(encoding='utf-8'))
        label=f'deep-review:{source.relative_to(ROOT)}'
        errors += validate_schema(records, DEEP_REVIEW_SCHEMA, label)
        reviews.extend(records)

    review_ids=set(); current_review_candidate_ids=set(); current_reviews_by_candidate={}; reviews_by_id={}
    all_review_ids={r.get('review_id') for r in reviews}
    known_comparator_ids=candidate_ids | ids
    for r in reviews:
        rid=r['review_id']
        cid=r['candidate_id']
        if rid in review_ids:
            errors += fail(f'duplicate deep-review id: {rid}')
        review_ids.add(rid)
        reviews_by_id[rid]=r
        if cid not in candidate_ids:
            errors += fail(f'{rid}: deep review references unknown candidate {cid}')
        calc=round(sum(r['quality_components'][k]*w for k,w in WEIGHTS.items()),2)
        if abs(calc-r['quality_score'])>0.01:
            errors += fail(f'{rid}: quality_score={r["quality_score"]}, expected {calc}')
        for comparator in r['comparators']:
            if comparator not in known_comparator_ids:
                errors += fail(f'{rid}: unknown comparator {comparator}')
            if comparator == cid:
                errors += fail(f'{rid}: candidate cannot compare against itself')
        if r['is_current']:
            if cid in current_review_candidate_ids:
                errors += fail(f'multiple current deep reviews for candidate: {cid}')
            current_review_candidate_ids.add(cid)
            current_reviews_by_candidate[cid]=r
            if current_screen_decisions.get(cid) != 'advance':
                errors += fail(f'{rid}: current deep review requires current shallow decision=advance for {cid}')
        supersedes=r.get('supersedes_review_id')
        if supersedes and supersedes not in all_review_ids:
            errors += fail(f'{rid}: supersedes unknown deep review {supersedes}')
        if supersedes == rid:
            errors += fail(f'{rid}: cannot supersede itself')

    reference_reviews=json.loads(REFERENCE_REVIEWS.read_text(encoding='utf-8'))
    errors += validate_schema(reference_reviews, REFERENCE_REVIEW_SCHEMA, 'reference-reviews')
    reference_review_ids=set(); current_reference_course_ids=set(); reference_reviews_by_id={}
    all_reference_review_ids={r.get('review_id') for r in reference_reviews}
    course_by_id={c['id']:c for c in courses}
    for r in reference_reviews:
        rid=r['review_id']
        cid=r['course_id']
        if rid in reference_review_ids:
            errors += fail(f'duplicate reference-review id: {rid}')
        reference_review_ids.add(rid)
        reference_reviews_by_id[rid]=r
        course=course_by_id.get(cid)
        if not course:
            errors += fail(f'{rid}: reference review references unknown canonical course {cid}')
        elif course.get('review_status') != 'reference_verified':
            errors += fail(f'{rid}: reference review requires review_status=reference_verified for {cid}')
        prior_calc=round(sum(r['prior_quality_components'][k]*w for k,w in WEIGHTS.items()),2)
        if abs(prior_calc-r['prior_quality_score'])>0.01:
            errors += fail(f'{rid}: prior_quality_score={r["prior_quality_score"]}, expected {prior_calc}')
        calc=round(sum(r['quality_components'][k]*w for k,w in WEIGHTS.items()),2)
        if abs(calc-r['quality_score'])>0.01:
            errors += fail(f'{rid}: quality_score={r["quality_score"]}, expected {calc}')
        for comparator in r['comparators']:
            if comparator not in known_comparator_ids:
                errors += fail(f'{rid}: unknown comparator {comparator}')
            if comparator == cid:
                errors += fail(f'{rid}: course cannot compare against itself')
        unchanged=(
            r['prior_quality_components'] == r['quality_components']
            and abs(r['prior_quality_score']-r['quality_score'])<=0.01
            and abs(r['prior_recommendation_score']-r['recommendation_score'])<=0.01
        )
        if r['calibration_outcome']=='confirmed' and not unchanged:
            errors += fail(f'{rid}: confirmed calibration must preserve prior scores/components')
        if r['calibration_outcome']=='recalibrated' and unchanged:
            errors += fail(f'{rid}: recalibrated outcome must record a score/component change')
        if r['is_current']:
            if cid in current_reference_course_ids:
                errors += fail(f'multiple current reference reviews for course: {cid}')
            current_reference_course_ids.add(cid)
            if course:
                if course['url'] != r['canonical_url']:
                    errors += fail(f'{cid}: canonical URL must match current reference review')
                if course['free_access'] != r['observed_free_access']:
                    errors += fail(f'{cid}: free_access must match current reference review')
                if course['status'] != r['observed_status']:
                    errors += fail(f'{cid}: status must match current reference review')
                if course['self_paced'] != r['self_paced']:
                    errors += fail(f'{cid}: self_paced must match current reference review')
                if abs(course['quality_score']-r['quality_score'])>0.01:
                    errors += fail(f'{cid}: canonical quality_score must match current reference review')
                if abs(course['recommendation_score']-r['recommendation_score'])>0.01:
                    errors += fail(f'{cid}: canonical recommendation_score must match current reference review')
                if course['quality_components'] != r['quality_components']:
                    errors += fail(f'{cid}: canonical quality_components must match current reference review')
        supersedes=r.get('supersedes_review_id')
        if supersedes and supersedes not in all_reference_review_ids:
            errors += fail(f'{rid}: supersedes unknown reference review {supersedes}')
        if supersedes == rid:
            errors += fail(f'{rid}: cannot supersede itself')

    reference_course_ids={c['id'] for c in courses if c.get('review_status')=='reference_verified'}
    missing_reference_reviews=reference_course_ids-current_reference_course_ids
    extra_reference_reviews=current_reference_course_ids-reference_course_ids
    for cid in sorted(missing_reference_reviews):
        errors += fail(f'{cid}: reference_verified course requires a current reference review')
    for cid in sorted(extra_reference_reviews):
        errors += fail(f'{cid}: current reference review exists for non-reference course')

    admission_sources=load_admission_sources()
    admissions=[]
    for source in admission_sources:
        records=json.loads(source.read_text(encoding='utf-8'))
        label=f'admission:{source.relative_to(ROOT)}'
        errors += validate_schema(records, ADMISSION_SCHEMA, label)
        admissions.extend(records)

    admission_ids=set(); current_admission_candidate_ids=set(); current_admissions={}
    all_admission_ids={a.get('admission_id') for a in admissions}
    known_admission_subject_ids=candidate_ids | ids
    course_by_id={c['id']:c for c in courses}
    for a in admissions:
        aid=a['admission_id']
        cid=a['candidate_id']
        rid=a['review_id']
        if aid in admission_ids:
            errors += fail(f'duplicate admission id: {aid}')
        admission_ids.add(aid)
        if cid not in candidate_ids:
            errors += fail(f'{aid}: admission references unknown candidate {cid}')
        review=reviews_by_id.get(rid)
        if not review:
            errors += fail(f'{aid}: admission references unknown deep review {rid}')
        elif review['candidate_id'] != cid:
            errors += fail(f'{aid}: review {rid} belongs to {review["candidate_id"]}, not {cid}')
        for competitor in a['comparison_set']:
            if competitor not in known_admission_subject_ids:
                errors += fail(f'{aid}: unknown comparison subject {competitor}')
            if competitor == cid:
                errors += fail(f'{aid}: comparison_set cannot include the candidate itself')
        for incumbent in a['incumbent_ids'] + a['displaced_course_ids'] + a['complements_course_ids']:
            if incumbent not in ids:
                errors += fail(f'{aid}: unknown canonical course {incumbent}')
        for alternative in a['outcompeted_by_ids']:
            if alternative not in known_admission_subject_ids:
                errors += fail(f'{aid}: unknown outcompeting subject {alternative}')
            if alternative == cid:
                errors += fail(f'{aid}: candidate cannot outcompete itself')
        if a['decision'] == 'admit' and a['outcompeted_by_ids']:
            errors += fail(f'{aid}: admit decision cannot declare outcompeted_by_ids')
        if a['decision'] == 'do_not_admit' and (a['displaced_course_ids'] or a['complements_course_ids']):
            errors += fail(f'{aid}: do_not_admit cannot displace or complement canonical courses')
        if a['is_current']:
            if cid in current_admission_candidate_ids:
                errors += fail(f'multiple current admission decisions for candidate: {cid}')
            current_admission_candidate_ids.add(cid)
            current_admissions[cid]=a
            if current_screen_decisions.get(cid) != 'advance':
                errors += fail(f'{aid}: current admission requires current shallow decision=advance for {cid}')
            current_review=current_reviews_by_candidate.get(cid)
            if not current_review:
                errors += fail(f'{aid}: current admission requires a current deep review for {cid}')
            elif current_review['review_id'] != rid:
                errors += fail(f'{aid}: current admission must reference current deep review {current_review["review_id"]}')
        supersedes=a.get('supersedes_admission_id')
        if supersedes and supersedes not in all_admission_ids:
            errors += fail(f'{aid}: supersedes unknown admission {supersedes}')
        if supersedes == aid:
            errors += fail(f'{aid}: cannot supersede itself')

    admitted_candidate_ids={cid for cid,a in current_admissions.items() if a['decision']=='admit'}
    for c in candidates:
        cid=c['id']
        if cid in ids and cid not in admitted_candidate_ids:
            errors += fail(f'candidate id already exists in approved/reference courses without current admit decision: {cid}')
        if c['url'] in urls and cid not in admitted_candidate_ids:
            errors += fail(f'candidate URL already exists in approved/reference courses without current admit decision: {c["url"]}')

    for cid,a in current_admissions.items():
        in_courses=cid in course_by_id
        if a['decision']=='admit':
            if not in_courses:
                errors += fail(f'{a["admission_id"]}: admit decision requires {cid} in data/courses.json')
                continue
            course=course_by_id[cid]
            review=current_reviews_by_candidate.get(cid)
            if review:
                if course['url'] != review['canonical_url']:
                    errors += fail(f'{cid}: admitted course URL must match current deep-review canonical_url')
                if abs(course['quality_score']-review['quality_score'])>0.01:
                    errors += fail(f'{cid}: admitted quality_score must match current deep review')
                if abs(course['recommendation_score']-review['recommendation_score'])>0.01:
                    errors += fail(f'{cid}: admitted recommendation_score must match current deep review')
                if course['quality_components'] != review['quality_components']:
                    errors += fail(f'{cid}: admitted quality_components must match current deep review')
        elif in_courses:
            errors += fail(f'{a["admission_id"]}: do_not_admit candidate must not exist in data/courses.json')

    errors += validate_readme_snapshot(
        courses,
        current_screen_decisions,
        current_review_candidate_ids,
        current_admission_candidate_ids,
    )

    if not errors:
        with tempfile.TemporaryDirectory(prefix="open-learning-index-public-") as tmp:
            public_output=Path(tmp)/"site"
            result=subprocess.run(
                [
                    sys.executable,
                    str(ROOT/"scripts/build_public_site.py"),
                    "--output",
                    str(public_output),
                ],
                cwd=ROOT,
                check=False,
            )
            if result.returncode != 0:
                errors += fail("public catalogue build failed")
            else:
                qa_result=subprocess.run(
                    [
                        sys.executable,
                        str(ROOT/"scripts/validate_public_site.py"),
                        str(public_output),
                    ],
                    cwd=ROOT,
                    check=False,
                )
                if qa_result.returncode != 0:
                    errors += fail("generated public-site QA failed")

    if errors: return 1
    print(
        f'OK: {len(courses)} courses, {len(candidates)} candidates from {len(candidate_sources)} candidate source file(s), '
        f'{len(screenings)} screening records, {len(reviews)} deep-review records, {len(reference_reviews)} reference-review records, '
        f'{len(admissions)} admission records, and {len(allowed_categories)} categories validated.'
    )
    return 0
if __name__=='__main__': raise SystemExit(main())
