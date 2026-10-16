"""Basic byte-level BPE from scratch (Karpathy minbpe-compatible).

Verified against:
- Karpathy "Let's build the GPT Tokenizer" (YouTube zduSFxRajkE, minbpe repo)
- Sennrich et al. 2016 BPE; Gage 1994; GPT-2 paper input-representation section
- 2026 consensus: standard BPE remains strong baseline (Chowdhury & Woolf 2026,
  Bahdanau et al. 2026, EACL 2026 tokenizer-as-design-decision survey).

Semantics (exactly as in the video):
  train(text, vocab_size): utf-8 bytes -> iterative most-frequent-pair merges.
  encode(text): bytes -> apply merges in training order (lowest rank first).
  decode(ids): ids -> bytes -> utf-8 string with errors="replace" (invalid
    byte streams map to U+FFFD, as in OpenAI's released code).
"""
from __future__ import annotations


def get_stats(ids: list[int]) -> dict[tuple[int, int], int]:
    """Count consecutive pairs. O(n) single pass."""
    counts: dict[tuple[int, int], int] = {}
    for a, b in zip(ids, ids[1:]):
        key = (a, b)
        counts[key] = counts.get(key, 0) + 1
    return counts


def merge(ids: list[int], pair: tuple[int, int], idx: int) -> list[int]:
    """Replace all occurrences of `pair` with `idx`, left-to-right, non-overlapping."""
    out: list[int] = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(idx)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


class BasicTokenizer:
    """Minimal byte-level BPE. vocab: id -> bytes; merges: (a,b) -> new_id."""

    def __init__(self) -> None:
        self.merges: dict[tuple[int, int], int] = {}
        self.vocab: dict[int, bytes] = {i: bytes([i]) for i in range(256)}
        self._encode_cache: dict[bytes, list[int]] = {}

    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        assert vocab_size >= 256
        tokens: list[int] = list(text.encode("utf-8"))
        n_merges = vocab_size - 256
        for i in range(n_merges):
            stats = get_stats(tokens)
            if not stats:
                break
            pair = max(stats, key=stats.get)  # most frequent
            idx = 256 + i
            tokens = merge(tokens, pair, idx)
            self.merges[pair] = idx
            self.vocab[idx] = self.vocab[pair[0]] + self.vocab[pair[1]]
            if verbose:
                print(f"merge {i+1}/{n_merges}: {pair} -> {idx} "
                      f"({self.vocab[idx]!r}) had {stats[pair]} occurrences")

    def _encode_chunk(self, text_bytes: bytes) -> list[int]:
        ids = list(text_bytes)
        while len(ids) >= 2:
            stats = get_stats(ids)
            # lowest-rank merge available in this chunk wins (training order)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            ids = merge(ids, pair, self.merges[pair])
        return ids

    def encode(self, text: str) -> list[int]:
        if not text:
            return []
        text_bytes = text.encode("utf-8")
        if text_bytes in self._encode_cache:
            return list(self._encode_cache[text_bytes])
        ids = self._encode_chunk(text_bytes)
        self._encode_cache[text_bytes] = ids
        return list(ids)

    def decode(self, ids: list[int]) -> str:
        text_bytes = b"".join(self.vocab[i] for i in ids)
        return text_bytes.decode("utf-8", errors="replace")

    def save(self, path: str) -> None:
        import json
        data = {
            "merges": [[a, b, idx] for (a, b), idx in self.merges.items()],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load(self, path: str) -> None:
        import json
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        for a, b, idx in data["merges"]:
            self.merges[(a, b)] = idx
            self.vocab[idx] = self.vocab[a] + self.vocab[b]
