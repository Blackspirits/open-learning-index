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

    if errors: return 1
    print(f'OK: {len(courses)} courses, {len(candidates)} candidates from {len(candidate_sources)} candidate source file(s), and {len(allowed_categories)} categories validated.')
    return 0
if __name__=='__main__': raise SystemExit(main())
