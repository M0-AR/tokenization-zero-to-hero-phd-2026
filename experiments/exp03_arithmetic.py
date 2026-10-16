"""EXP-03: Arithmetic tokenization arbitrariness (video: 127 | 6 77 | 80 4).

Checks on tiktoken GPT-2 + cl100k that multi-digit numbers split arbitrarily,
motivating the 'arithmetic headwind' claim. Prints live evidence.
"""
import tiktoken

for enc_name in ["gpt2", "cl100k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    for s in ["127+677=804", " 127", " 677", " 804", "Hello world 1234"]:
        print(enc_name, repr(s), enc.encode(s))
print("EXP-03 OK: inspect splits above; 3-4 digit numbers fragment (esp. gpt2)")
