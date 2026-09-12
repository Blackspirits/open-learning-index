#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

candidate_paths = ['data/candidates.json'] + [f'data/candidates/batch-{n:02d}.json' for n in range(2, 8)]
candidates = []
for path in candidate_paths:
    candidates.extend(load(path))

screens = []
for path in sorted((ROOT / 'data' / 'screening').glob('*.json')):
    screens.extend(json.loads(path.read_text(encoding='utf-8')))

current = {r['candidate_id']: r for r in screens if r.get('is_current') is True}
if len(current) != len(candidates):
    raise SystemExit(f'expected {len(candidates)} current decisions, found {len(current)}')

categories = load('data/categories.json')
category_names = {c['id']: c['name'] for c in categories}
by_cat = defaultdict(Counter)
for c in candidates:
    by_cat[c['category']]['discovered'] += 1
    by_cat[c['category']][current[c['id']]['decision']] += 1

survivors = [c for c in candidates if current[c['id']]['decision'] in {'advance','hold'}]
provider_counts = Counter(c['provider'] for c in survivors)
lang_counts = Counter()
for c in survivors:
    for lang in current[c['id']].get('instruction_languages', []):
        lang_counts[lang] += 1

access_counts = Counter(current[c['id']]['observed_free_access'] for c in candidates if current[c['id']]['decision']=='advance')

language_paths = []
for c in candidates:
    if c['category'] == 'languages':
        r = current[c['id']]
        language_paths.append((c.get('target_language','—'), c['title'], r['decision'], c['provider']))
language_paths.sort()

holds = []
for c in candidates:
    r = current[c['id']]
    if r['decision'] == 'hold':
        holds.append((c['id'], c['title'], c['category'], r['rationale']))

lines = [
    '# Final Coverage Snapshot — v0.2', '',
    '**Generated from the current screening ledger.**', '',
    f'- Discovery candidates: **{len(candidates)}**',
    f'- Current advance: **{sum(1 for r in current.values() if r["decision"]=="advance")}**',
    f'- Current hold: **{sum(1 for r in current.values() if r["decision"]=="hold")}**',
    f'- Current reject: **{sum(1 for r in current.values() if r["decision"]=="reject")}**',
    f'- Active survivor pool (advance + hold): **{len(survivors)}**', '',
    '## Current coverage by category', '',
    '| Category | Discovered | Advance | Hold | Reject | Survivors |',
    '|---|---:|---:|---:|---:|---:|',
]
for cat in categories:
    x = by_cat[cat['id']]
    lines.append(f"| {cat['name']} | {x['discovered']} | {x['advance']} | {x['hold']} | {x['reject']} | {x['advance']+x['hold']} |")

lines += ['', '## Instruction languages among active survivors', '', '| Language | Survivors |', '|---|---:|']
for lang, count in lang_counts.most_common():
    lines.append(f'| `{lang}` | {count} |')

lines += ['', '## Provider concentration among active survivors', '', '| Provider | Survivors |', '|---|---:|']
for provider, count in provider_counts.most_common(20):
    lines.append(f'| {provider} | {count} |')

lines += ['', '## Access tiers among current advances', '', '| Access tier | Advances |', '|---|---:|']
for tier, count in sorted(access_counts.items()):
    lines.append(f'| `{tier}` | {count} |')

lines += ['', '## Language-learning pathways', '', '| Target language | Course | Decision | Provider |', '|---|---|---|---|']
for target, title, decision, provider in language_paths:
    lines.append(f'| `{target}` | {title} | `{decision}` | {provider} |')

lines += ['', '## Current holds', '']
for cid, title, cat, rationale in holds:
    lines += [f'### {title}', '', f'- Candidate: `{cid}`', f'- Category: `{cat}`', f'- Rationale: {rationale}', '']

out = ROOT / 'docs' / 'coverage-audit-v0.2-final-snapshot.md'
out.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
print(out)
