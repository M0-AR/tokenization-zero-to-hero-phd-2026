"""Fetch + pin live corpora with SHA256 manifest (real-market/live-data verification)."""
import sys, json
sys.path.insert(0, "src")
from pathlib import Path
from tokphd.live_data import fetch_live_corpus, CORPORA

out = []
for name in CORPORA:
    try:
        c = fetch_live_corpus(name)
        text = c.pop("text")
        Path(f"data/live/{name}.txt").parent.mkdir(parents=True, exist_ok=True)
        Path(f"data/live/{name}.txt").write_text(text[:500000], encoding="utf-8")
        out.append(c)
        print(f"OK {name}: {c['bytes']} bytes sha={c['sha256'][:12]}")
    except Exception as e:
        print(f"FAIL {name}: {e}")
Path("data/live/manifest.json").write_text(json.dumps(out, indent=2))
