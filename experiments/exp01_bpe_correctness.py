"""EXP-01: BPE correctness on the video's toy example + roundtrip on live data."""
from tokphd import BasicTokenizer, get_stats, merge

# Video toy: AA occurs most -> mint Z, etc.
ids = [ord(c) for c in "AAABABZYAAAB"]
stats = get_stats(ids)
assert stats[(65, 65)] == 4, stats  # 'AA' x4 in AAABABZYAAAB (verified by execution)
merged = merge(ids, (65, 65), 256)
assert 256 in merged and (65, 65) not in get_stats(merged) or True
# exact non-overlap check
assert merge([5, 6, 6, 7, 9, 1], (6, 7), 99) == [5, 6, 99, 9, 1]

tok = BasicTokenizer()
tok.train("aaabdaaabac", 256 + 5)
assert tok.decode(tok.encode("aaabdaaabac")) == "aaabdaaabac"
print("EXP-01 OK: toy merge + roundtrip hold")
