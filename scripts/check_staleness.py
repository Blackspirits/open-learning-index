#!/usr/bin/env python3
import json
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
today=date.today()
courses=json.loads((ROOT/'data/courses.json').read_text(encoding='utf-8'))
stale=[]
for c in courses:
    next_review=date.fromisoformat(c['next_review'])
    if today>next_review:
        stale.append((today-next_review,c))
if not stale:
    print('No overdue course reviews.')
else:
    print(f'{len(stale)} overdue review(s):')
    for overdue,c in sorted(stale, reverse=True, key=lambda x:x[0]):
        print(f'- {c["id"]}: {overdue.days} day(s) overdue; last verified {c["last_verified"]}')
