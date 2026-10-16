"""tokphd: from-scratch BPE tokenization research kit (Karpathy-compatible, verified)."""
from .basic_bpe import BasicTokenizer, get_stats, merge
from .regex_tokenizer import RegexTokenizer, GPT2_SPLIT_PATTERN, GPT4_SPLIT_PATTERN
from .metrics import (
    fertility,
    bytes_per_token,
    compression_ratio,
    parity_ratio,
    unmerged_byte_rate,
    tokens_per_char,
)
from .live_data import CORPORA, PARALLEL, fetch_live_corpus

__all__ = [
    "BasicTokenizer",
    "get_stats",
    "merge",
    "RegexTokenizer",
    "GPT2_SPLIT_PATTERN",
    "GPT4_SPLIT_PATTERN",
    "fertility",
    "bytes_per_token",
    "compression_ratio",
    "parity_ratio",
    "unmerged_byte_rate",
    "tokens_per_char",
    "CORPORA",
    "PARALLEL",
    "fetch_live_corpus",
]

__version__ = "0.1.0"
