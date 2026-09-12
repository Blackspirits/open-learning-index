#!/usr/bin/env python3
import json, sys
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
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
WEIGHTS={'pedagogy':0.25,'depth':0.20,'practice':0.20,'materials':0.10,'currency':0.10,'expertise':0.10,'accessibility':0.05}

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
        if c['id'] in ids: errors += fail(f'candidate id already exists in approved/reference courses: {c["id"]}')
        if c['url'] in urls: errors += fail(f'candidate URL already exists in approved/reference courses: {c["url"]}')

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

    review_ids=set(); current_review_candidate_ids=set()
    all_review_ids={r.get('review_id') for r in reviews}
    known_comparator_ids=candidate_ids | ids
    for r in reviews:
        rid=r['review_id']
        cid=r['candidate_id']
        if rid in review_ids:
            errors += fail(f'duplicate deep-review id: {rid}')
        review_ids.add(rid)
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
            if current_screen_decisions.get(cid) != 'advance':
                errors += fail(f'{rid}: current deep review requires current shallow decision=advance for {cid}')
        supersedes=r.get('supersedes_review_id')
        if supersedes and supersedes not in all_review_ids:
            errors += fail(f'{rid}: supersedes unknown deep review {supersedes}')
        if supersedes == rid:
            errors += fail(f'{rid}: cannot supersede itself')

    if errors: return 1
    print(
        f'OK: {len(courses)} courses, {len(candidates)} candidates from {len(candidate_sources)} candidate source file(s), '
        f'{len(screenings)} screening records, {len(reviews)} deep-review records, and {len(allowed_categories)} categories validated.'
    )
    return 0
if __name__=='__main__': raise SystemExit(main())
