"""Regex pre-tokenization (the part Karpathy calls 'where things complexify').

GPT-2 pattern (tiktoken / encoder.py, regex module):
  splits text into chunks; merges NEVER cross chunk boundaries.
  Consequence verified in video: 'e' + ' ' in "hello world" can never merge
  because they fall in different chunks.

GPT-4 cl100k_base pattern: case-insensitive contractions (?i:), 1-3 digit
  number cap, refined whitespace handling. Vocab ~100k vs GPT-2 ~50k.

References: GPT-2 paper Sec. Input Representation; openai/tiktoken
  data-gym-to-3.5 / cl100k_base.tiktoken; njkumarr o200k analysis (marks-aware
  \\p{M} fix for Tamil-class scripts); Tokka-Bench 2026.
"""
from __future__ import annotations

import regex as re

from .basic_bpe import BasicTokenizer, get_stats, merge

GPT2_SPLIT_PATTERN = (
    r"""'(?:[SsDdMmTt]|[Rr][Ee]|[Vv][Ee]|[Ll][Ll]|[Oo]|[Nn])|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"""
)
# cl100k_base (GPT-4): case-insensitive contractions + same number/space handling
GPT4_SPLIT_PATTERN = (
    r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
)


class RegexTokenizer(BasicTokenizer):
    """BPE with regex pre-tokenization + special-token registry (encode/decode)."""

    def __init__(self, pattern: str = GPT2_SPLIT_PATTERN) -> None:
        super().__init__()
        self.pattern = pattern
        self._compiled = re.compile(pattern)
        self.special_tokens: dict[str, int] = {}
        self.inverse_special: dict[int, str] = {}

    def register_special_tokens(self, mapping: dict[str, int]) -> None:
        for tok, idx in mapping.items():
            self.special_tokens[tok] = idx
            self.inverse_special[idx] = tok
            self.vocab[idx] = tok.encode("utf-8")

    def _split(self, text: str) -> list[str]:
        return self._compiled.findall(text)

    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        assert vocab_size >= 256
        n_merges = vocab_size - 256 - len(self.special_tokens)
        # Train merges on chunked text (merges never cross chunk boundaries,
        # so training on chunks == training on full text with boundary constraint)
        chunks = self._split(text)
        ids: list[int] = []
        for ch in chunks:
            ids.extend(list(ch.encode("utf-8")))
            ids.append(257 + 10**9)  # sentinel boundary (removed below)
        # Simpler correct approach: train per chunk, aggregate stats globally per round
        # (Karpathy/minbpe reference behaviour). We implement the reference loop:
        chunk_ids: list[list[int]] = [list(c.encode("utf-8")) for c in chunks]
        merges: dict[tuple[int, int], int] = {}
        vocab: dict[int, bytes] = {i: bytes([i]) for i in range(256)}
        for tok, idx in self.special_tokens.items():
            vocab[idx] = tok.encode("utf-8")
        for i in range(n_merges):
            stats: dict[tuple[int, int], int] = {}
            for cids in chunk_ids:
                s = get_stats(cids)
                for k, v in s.items():
                    stats[k] = stats.get(k, 0) + v
            if not stats:
                break
            pair = max(stats, key=stats.get)
            idx = 256 + i
            # skip ids taken by special tokens
            while idx in vocab:
                idx += 1
                # keep merge count aligned: shift subsequent ids accordingly
            chunk_ids = [merge(c, pair, idx) for c in chunk_ids]
            merges[pair] = idx
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]
            if verbose:
                print(f"merge {i+1}/{n_merges}: {pair} -> {idx}")
        self.merges = merges
        # rebuild vocab preserving special tokens
        base = {i: bytes([i]) for i in range(256)}
        for tok, idx in self.special_tokens.items():
            base[idx] = tok.encode("utf-8")
        for (a, b), idx in self.merges.items():
            base[idx] = base[a] + base[b]
        self.vocab = base

    def encode(self, text: str, allowed_special: set[str] | None = None) -> list[int]:
        allowed_special = allowed_special or set()
        # Split out registered special tokens first (exact match, like tiktoken)
        if self.special_tokens:
            import re as _re2
            pat = "(" + "|".join(_re2.escape(s) for s in sorted(self.special_tokens, key=len, reverse=True)) + ")"
            parts = _re2.split(pat, text)
        else:
            parts = [text]
        ids: list[int] = []
        for part in parts:
            if part in self.special_tokens:
                if part in allowed_special:
                    ids.append(self.special_tokens[part])
                else:
                    # not allowed -> encode as normal text (safe default)
                    for chunk in self._split(part):
                        ids.extend(self._encode_chunk(chunk.encode("utf-8")))
            elif part:
                for chunk in self._split(part):
                    ids.extend(self._encode_chunk(chunk.encode("utf-8")))
        return ids

    def decode(self, ids: list[int]) -> str:
        out = bytearray()
        for i in ids:
            if i in self.inverse_special:
                out.extend(self.inverse_special[i].encode("utf-8"))
            else:
                out.extend(self.vocab[i])
        return bytes(out).decode("utf-8", errors="replace")
