#!/usr/bin/env python3
"""Run canonical validation while routing generated-site checks through public locale wrappers.

The canonical validator remains the source of truth for schemas, ledgers, scores and
admissions. Only its two subprocess calls for generated-site build/QA are redirected
so the same run validates every published presentation locale, including French.
"""

from __future__ import annotations

from pathlib import Path

import validate as canonical


ROOT = Path(__file__).resolve().parents[1]
_original_run = canonical.subprocess.run


def routed_run(args, *positional, **kwargs):
    routed = list(args) if isinstance(args, (list, tuple)) else args
    if isinstance(routed, list) and len(routed) >= 2:
        script = Path(str(routed[1])).name
        if script == "build_public_site.py":
            routed[1] = str(ROOT / "scripts" / "build_public_site_public.py")
        elif script == "validate_public_site.py":
            routed[1] = str(ROOT / "scripts" / "validate_public_site_public.py")
    return _original_run(routed, *positional, **kwargs)


canonical.subprocess.run = routed_run


if __name__ == "__main__":
    raise SystemExit(canonical.main())
