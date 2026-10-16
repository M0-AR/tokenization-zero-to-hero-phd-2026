"""EXP-06: Special tokens + trailing-whitespace distribution shift.

- <|endoftext|> swaps in only when allowed_special includes it (tiktoken parity).
- trailing space appends token 220 in GPT-2, splitting the next token's
  leading-space merge -> out-of-distribution continuation (API warns).
"""
import tiktoken
from tokphd import RegexTokenizer, GPT2_SPLIT_PATTERN

tok = RegexTokenizer(GPT2_SPLIT_PATTERN)
tok.register_special_tokens({"<|endoftext|>": 50256})
tok.train("hello world " * 200, 300)
assert tok.encode("hi <|endoftext|> bye") != tok.encode("hi <|endoftext|> bye", allowed_special={"<|endoftext|>"})
print("special-token gating OK")

g = tiktoken.get_encoding("gpt2")
a = g.encode("Here is a tagline for an ice cream shop")
b = g.encode("Here is a tagline for an ice cream shop ")
print("no-trailing:", a[-3:], "with-trailing:", b[-3:])
assert b[-1] == 220  # lone space token; next token loses its leading-space merge
print("EXP-06 OK: trailing space = extra 220, next-token merge broken")
