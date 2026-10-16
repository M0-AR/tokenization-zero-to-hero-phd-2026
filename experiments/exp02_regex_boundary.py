"""EXP-02: Regex pre-tokenization boundary (dog. / dog! / dog? never merge punctuation).

Verifies Karpathy/GPT-2 claim: merges never cross regex chunks, so
'dog' + punctuation stay separate by construction.
"""
from tokphd import RegexTokenizer, GPT2_SPLIT_PATTERN

tok = RegexTokenizer(GPT2_SPLIT_PATTERN)
chunks = tok._split("dog. dog! dog? hello world 123")
print("chunks:", chunks)
assert "dog" in chunks and "." in chunks, chunks
# train small and confirm '.' never merges with 'g'
tok.train("dog. dog! dog? dog dog dog hello world " * 50, 300)
ids = tok.encode("dog.")
txt = tok.decode(ids)
assert txt == "dog.", txt
# boundary proof: no vocab entry spans 'g.'
for v in tok.vocab.values():
    assert not v.endswith(b"g."), v
print("EXP-02 OK: punctuation/letter boundary enforced")
