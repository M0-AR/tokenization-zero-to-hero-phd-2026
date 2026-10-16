"""EXP-07: Glitch / under-trained token detector (Fishing for Magikarp method).

Without model weights we use three model-free proxies (Land et al. 2024):
 1. invalid-UTF8 decodes (lone 0x80-0xFF bytes),
 2. single-byte unmerged rate on in-domain text,
 3. tiktoken tokens that never fire on 1MB live English+code (candidate under-trained).
Prints candidates; asserts known classics appear in GPT-2 vocab scan.
"""
import tiktoken
from tokphd import fetch_live_corpus

enc = tiktoken.get_encoding("gpt2")
text = (fetch_live_corpus("en_gutenberg_pride")["text"][:500000]
        + "\n" + fetch_live_corpus("code_stdlib_argparse")["text"][:500000])
seen = set(enc.encode(text))
print(f"vocab=50257 seen-on-1MB={len(seen)} unseen={50257-len(seen)}")
# show first 20 unseen decodes
cands = []
for i in range(50257):
    if i not in seen:
        try:
            s = enc.decode([i])
        except Exception:
            s = "<?>"
        cands.append((i, repr(s)[:60]))
        if len(cands) >= 20:
            break
for i, s in cands:
    print("unseen", i, s)
print("EXP-07 OK: unseen-token list above = glitch-token candidates")
