#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN_DIR = ROOT / "data" / "screening"
RESOLUTION = SCREEN_DIR / "hold-resolution-02.json"

new_records = json.loads(RESOLUTION.read_text(encoding="utf-8"))
targets = {r["supersedes_screen_id"] for r in new_records}
found = set()
changed_files = []

for path in sorted(SCREEN_DIR.glob("*.json")):
    if path == RESOLUTION:
        continue
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for record in records:
        sid = record.get("screen_id")
        if sid in targets:
            if sid in found:
                raise SystemExit(f"duplicate superseded screen id found: {sid}")
            found.add(sid)
            if record.get("is_current") is not True:
                raise SystemExit(f"expected current record before superseding: {sid}")
            record["is_current"] = False
            changed = True
    if changed:
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        changed_files.append(str(path.relative_to(ROOT)))

missing = targets - found
if missing:
    raise SystemExit("missing superseded records: " + ", ".join(sorted(missing)))

print(f"superseded {len(found)} current screening records")
for path in changed_files:
    print(path)
