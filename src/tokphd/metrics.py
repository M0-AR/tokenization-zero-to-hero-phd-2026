"""Tokenizer metrics (TokEval/Tokka-Bench-compatible, from 2026 literature).

Definitions (all verified against cited papers):
- fertility: tokens / whitespace-words (lower = better). Standard proxy.
- bytes_per_token: utf-8 bytes / tokens (higher = denser).
- compression_ratio: len(utf8 bytes) / len(tokens); == bytes_per_token.
- parity_ratio: tokens(lang) / tokens(english parallel) (1.0 = parity).
- unmerged_byte_rate: fraction of tokens that are single raw bytes
  (symptom of insufficient vocab coverage; correlates r~0.89 with Indic tax,
  Srivastava 2026).
- tokens_per_char: tokenizer-agnostic density for scripts without spaces.
"""
from __future__ import annotations

from typing import Protocol


class Encoder(Protocol):
    def encode(self, text: str) -> list[int]: ...


def _encode(tok: Encoder, text: str) -> list[int]:
    try:
        return tok.encode(text)  # type: ignore[call-arg]
    except TypeError:
        return tok.encode(text)


def fertility(tok: Encoder, text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return len(_encode(tok, text)) / len(words)


def bytes_per_token(tok: Encoder, text: str) -> float:
    ids = _encode(tok, text)
    if not ids:
        return 0.0
    return len(text.encode("utf-8")) / len(ids)


def compression_ratio(tok: Encoder, text: str) -> float:
    return bytes_per_token(tok, text)


def tokens_per_char(tok: Encoder, text: str) -> float:
    chars = [c for c in text if not c.isspace()]
    if not chars:
        return 0.0
    return len(_encode(tok, text)) / len(chars)


def parity_ratio(tok: Encoder, text_lang: str, text_en: str) -> float:
    den = len(_encode(tok, text_en))
    if den == 0:
        return float("nan")
    return len(_encode(tok, text_lang)) / den


def unmerged_byte_rate(tok: Encoder, text: str) -> float:
    """Fraction of emitted tokens that decode to a single byte.

    Works for any BasicTokenizer/RegexTokenizer via .vocab; falls back to
    trying tiktoken decode for external tokenizers.
    """
    ids = _encode(tok, text)
    if not ids:
        return 0.0
    vocab = getattr(tok, "vocab", None)
    if vocab is not None:
        single = sum(1 for i in ids if len(vocab[i]) == 1)
        return single / len(ids)
    # generic fallback: single-char decode heuristic
    try:
        import tiktoken  # type: ignore

        enc = getattr(tok, "_tiktoken_enc", None)
        if enc is not None:
            single = sum(1 for i in ids if len(enc.decode_single_token_bytes(i)) == 1)
            return single / len(ids)
    except Exception:
        pass
    return float("nan")
