#!/usr/bin/env python3
import json, sys
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/courses.json'
SCHEMA=ROOT/'data/course.schema.json'
WEIGHTS={'pedagogy':0.25,'depth':0.20,'practice':0.20,'materials':0.10,'currency':0.10,'expertise':0.10,'accessibility':0.05}

def fail(msg):
    print(f'ERROR: {msg}', file=sys.stderr); return 1

def main():
    errors=0
    courses=json.loads(DATA.read_text(encoding='utf-8'))
    try:
        import jsonschema
        jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(courses)
    except ModuleNotFoundError:
        print('NOTE: jsonschema not installed; running invariant checks only.')
    except Exception as e:
        errors += fail(f'schema validation failed: {e}')

    ids=set(); urls=set()
    for c in courses:
        if c['id'] in ids: errors += fail(f'duplicate id: {c["id"]}')
        ids.add(c['id'])
        if c['url'] in urls: errors += fail(f'duplicate canonical URL: {c["url"]}')
        urls.add(c['url'])
        calc=round(sum(c['quality_components'][k]*w for k,w in WEIGHTS.items()),2)
        if abs(calc-c['quality_score'])>0.01:
            errors += fail(f'{c["id"]}: quality_score={c["quality_score"]}, expected {calc}')
        if date.fromisoformat(c['next_review']) < date.fromisoformat(c['last_verified']):
            errors += fail(f'{c["id"]}: next_review precedes last_verified')
    if errors: return 1
    print(f'OK: {len(courses)} courses validated.')
    return 0
if __name__=='__main__': raise SystemExit(main())
