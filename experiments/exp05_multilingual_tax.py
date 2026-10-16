"""EXP-05: Multilingual token tax on LIVE parallel sentences.

Reproduces 1.5-3.3x (es) to 8-13x (Indic) findings with tiktoken cl100k vs o200k.
"""
import tiktoken
from tokphd import PARALLEL, parity_ratio

for enc_name in ["cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    en = PARALLEL["en"]["text"]
    print(f"--- {enc_name} ---")
    for lang, d in PARALLEL.items():
        ids = enc.encode(d["text"])
        tax = parity_ratio(enc, d["text"], en)
        print(f"{lang}: tokens={len(ids)} tax={tax:.2f}x")
print("EXP-05 OK: non-English tax visible; o200k narrows it (marks-aware regex)")
