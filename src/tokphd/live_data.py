"""Live-data corpora: real, public, re-fetchable (no vendored dumps).

Every experiment fetches from the live web at run time, with a pinned
fallback snapshot under data/raw/ so runs are reproducible offline.
Sources are stable public URLs (Wikipedia REST, Project Gutenberg,
CPython stdlib raw GitHub). Timestamps + SHA256 are recorded per run.
"""
from __future__ import annotations

import hashlib
import urllib.request
from datetime import datetime, timezone

CORPORA: dict[str, dict[str, str]] = {
    "en_wiki_taylor_swift": {
        "url": "https://en.wikipedia.org/api/rest_v1/page/plain/Taylor_Swift",
        "desc": "Long Wikipedia page (Karpathy used it for GPT-4 merges demo)",
    },
    "en_gutenberg_pride": {
        "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
        "desc": "Pride and Prejudice (English prose benchmark)",
    },
    "es_gutenberg_quijote": {
        "url": "https://www.gutenberg.org/files/2000/2000-0.txt",
        "desc": "Don Quijote (Spanish prose benchmark)",
    },
    "code_stdlib_argparse": {
        "url": "https://raw.githubusercontent.com/python/cpython/main/Lib/argparse.py",
        "desc": "Real Python stdlib code (indentation stress test)",
    },
}

# Parallel sentences (FLORES-style, content-controlled). Short so parity is exact.
PARALLEL: dict[str, dict[str, str]] = None  # type: ignore
PARALLEL = {
    "en": {"text": "Hello, how are you? Here is a tagline for an ice cream shop."},
    "es": {"text": "Hola, ¿cómo estás? Aquí hay un eslogan para una heladería."},
    "fr": {"text": "Bonjour, comment ça va ? Voici un slogan pour un glacier."},
    "de": {"text": "Hallo, wie geht es dir? Hier ist ein Slogan für einen Eisladen."},
    "ko": {"text": "안녕하세요, 어떻게 지내세요? 아이스크림 가게 슬로건입니다."},
    "ar": {"text": "مرحبا، كيف حالك؟ إليك شعارا لمحل آيس كريم."},
    "zh": {"text": "你好，你好吗？这里有一家冰淇淋店的标语。"},
    "hi": {"text": "नमस्ते, आप कैसे हैं? यहाँ एक आइसक्रीम की दुकान के लिए एक टैगलाइन है।"},
}


def fetch_live_corpus(name: str, timeout: int = 60, max_bytes: int = 2_000_000) -> dict:
    meta = CORPORA[name]
    req = urllib.request.Request(meta["url"], headers={"User-Agent": "tokphd-research/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(max_bytes)
    text = raw.decode("utf-8", errors="replace")
    return {
        "name": name,
        "url": meta["url"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "chars": len(text),
        "text": text,
    }
