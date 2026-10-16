"""Unit tests: every invariant verified by execution (no hand-waving)."""
import sys
sys.path.insert(0, "src")

from tokphd import BasicTokenizer, RegexTokenizer, get_stats, merge
from tokphd import fertility, bytes_per_token


def test_get_stats():
    assert get_stats([1, 2, 1, 2, 3]) == {(1, 2): 2, (2, 1): 1, (2, 3): 1}


def test_merge_nonoverlap():
    assert merge([5, 6, 6, 7, 9, 1], (6, 7), 99) == [5, 6, 99, 9, 1]
    assert merge([1, 1, 1], (1, 1), 9) == [9, 1]  # left-to-right, non-overlapping


def test_roundtrip_basic():
    tok = BasicTokenizer()
    tok.train("hello world hello world " * 20, 280)
    for s in ["hello world", "Hi there!", "안녕 egg 123"]:
        assert tok.decode(tok.encode(s)) == s


def test_invalid_utf8_replace():
    tok = BasicTokenizer()
    assert tok.decode([128]) == "�"  # lone continuation byte -> replacement char


def test_regex_boundary():
    tok = RegexTokenizer()
    chunks = tok._split("hello world 123")
    assert "hello" in chunks and " world" in chunks
    tok.train("dog. dog! dog? " * 30 + "hello world " * 30, 300)
    assert tok.decode(tok.encode("dog.")) == "dog."
    for v in tok.vocab.values():
        assert not v.endswith(b"g.")


def test_metrics_direction():
    tok = BasicTokenizer()
    tok.train("ab " * 500, 300)
    assert fertility(tok, "ab ab ab") <= fertility(tok, "xqz! @#$ qwe")
    assert bytes_per_token(tok, "ab ab ab") >= 1.0
