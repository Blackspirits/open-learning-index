#!/usr/bin/env python3
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
courses=json.loads((ROOT/'data/courses.json').read_text(encoding='utf-8'))
fields=['id','title','provider','category','level','primary_language','other_languages','url','free_access','certificate','academic_credits','self_paced','status','quality_score','recommendation_score','last_verified','review_interval_days','next_review','why_recommended']
with (ROOT/'data/courses.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for c in courses:
        row={k:c.get(k,'') for k in fields}; row['other_languages']=';'.join(c.get('other_languages',[])); w.writerow(row)
print(f'Generated {len(courses)} rows.')
