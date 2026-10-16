"""EXP-04: Python whitespace efficiency (video: GPT-2 wastes 220 220 220 220).

Live code from CPython stdlib; compares gpt2 vs cl100k vs o200k bytes/token.
"""
import tiktoken
from tokphd import fetch_live_corpus, bytes_per_token

code = fetch_live_corpus("code_stdlib_argparse")["text"][:20000]
for enc_name in ["gpt2", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    ids = enc.encode(code)
    bpt = len(code.encode()) / len(ids)
    print(f"{enc_name}: tokens={len(ids)} bytes/token={bpt:.3f}")
# GPT-2 single-space token id check
g = tiktoken.get_encoding("gpt2")
assert g.encode("    ") == [220, 220, 220, 220], g.encode("    ")
c = tiktoken.get_encoding("cl100k_base")
assert len(c.encode("    ")) == 1, c.encode("    ")
print("EXP-04 OK: GPT-2 4-spaces=4 toks; cl100k 4-spaces=1 tok")
