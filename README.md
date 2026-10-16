<div align="center">

# 🔤 Tokenization Zero-to-Hero
### *From bytes to `SolidGoldMagikarp` — every famous LLM quirk, rebuilt from zero and proven on live data*

[![tests](https://img.shields.io/badge/tests-6_passed-brightgreen)](tests/test_bpe.py)
[![docker](https://img.shields.io/badge/docker-one_command-blue)](docker-compose.yml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![python](https://img.shields.io/badge/python-3.10%2B-yellow)](pyproject.toml)
[![live-data](https://img.shields.io/badge/data-live_verified-orange)](scripts/fetch_live.py)

**[🌐 Open the interactive website](docs/preview.html)** · **[🌱 Beginner guide](#-beginner-guide--read-this-and-you-are-a-professional)** · **[🎯 Quiz](#-quiz--from-scratch-to-pro)** · **[🔬 Playground](#-playground--feel-tokenization)** · **[🚀 Quick start](#-quick-start--60-seconds)**

![demo](docs/demo.gif)

*Above: the 5 facts this repo proves — bytes in, numbers out, arbitrary splits, whitespace fix, multilingual tax, hidden pattern. 89 KB, loops forever.*

</div>

> ## 💼 CEO summary (30 seconds — the only paragraph a busy person needs)
> Every LLM bill, every context-limit error, and roughly half of all "weird AI mistakes"
> come from one invisible step: the **tokenizer**. This repo rebuilds it **from zero**
> (bytes → BPE merges → GPT-2/GPT-4 rules), proves each famous quirk on **live public data**
> (not screenshots), and hands you a **one-command benchmark** plus a **new discovery**:
> a language's "token tax" is predicted by how often BPE merges fail (r = 0.72).
> **If you read only the [Beginner guide](#-beginner-guide--read-this-and-you-are-a-professional) below, you will know more than most interview candidates** — and you can prove it in the [Quiz](#-quiz--from-scratch-to-pro).

| Signal (all executed 2026-10-17, reproduce with `docker compose up`) | Value |
|---|---|
| Unit tests | **6 passed** (`pytest tests/ -q`) |
| `127` vs `677` vs `804` (GPT-2) | `127→[18112]` single · `677→[718,3324]` split · `804→[807,3023]` split |
| Python 4-spaces | GPT-2 `[220,220,220,220]` (4 toks) vs `cl100k` 1 tok; bytes/token **2.188 → 4.889** |
| Hindi token tax (same sentence) | GPT-2 **6.18×** · `cl100k` **4.06×** · `o200k` **1.56×** · ours (EN-only) **6.69×** |
| Hidden pattern (new) | fertility ↔ unmerged-byte-rate Pearson **r = 0.72** |
| JSON → YAML | saves 12.1% (GPT-2) · 15.6% (`cl100k`/`o200k`) |

![hero](docs/screenshot-hero.png)
*The interactive site ([`docs/preview.html`](docs/preview.html)) — playground, quiz with step-by-step answers, live tables, and 2-minute Pages deploy guide.*

---

## 📑 Contents

- [🌱 Beginner guide](#-beginner-guide--read-this-and-you-are-a-professional)
- [🔬 Playground](#-playground--feel-tokenization)
- [🎯 Quiz](#-quiz--from-scratch-to-pro)
- [✨ Features & user stories](#-features--user-stories--what-you-can-do-with-this-repo)
- [🚀 Quick start](#-quick-start--60-seconds) · [🗺 Repository map](#-repository-map) · [📊 Results](#-results--every-number-below-was-executed-not-quoted)
- [🔬 Hidden pattern](#-hidden-pattern-candidate-phd-contribution)
- [🌐 Website & GitHub Pages](#-website--github-pages--2-minutes)
- [❓ FAQ](#-faq-the-questions-everyone-asks)
- [📄 Full study (abstract → references)](#-1-abstract)
- [📜 License & citation](#-license--citation)

---

## 🌱 Beginner guide — read this and you are a professional

*"Let's work this out in a step-by-step way to be sure we have the right answer."*
That sentence is the entire method of this repo: **never believe a claim — run it.**
Each step below maps to exactly one file in `experiments/` you can execute.

**Step 1 — Computers only understand numbers.** Text like `Hello` must become numbers
before any AI can read it. Those numbers are called **tokens**.
→ *See `exp01_bpe_correctness.py`: the smallest possible merge, verified.*

**Step 2 — One character = one token (the naive idea).** `H e l l o → [72,101,108,108,111]`.
Works for English, explodes for Korean/emoji — ~150,000 characters and growing,
so the dictionary would be gigantic and unstable.

**Step 3 — Better: UTF-8 bytes (only 256 possibilities).** Every character on Earth
becomes 1–4 bytes. Tiny dictionary (256 rows), but very long sequences — attention
cost explodes. → *Every experiment starts here: `text.encode("utf-8")`.*

**Step 4 — Best: BPE merges frequent pairs.** Count the most common byte pair
(e.g. `e + space` occurred 20× in the sample), mint token `256`, replace everywhere,
repeat. 20 merges ≈ 1.27× shorter. 50,000 merges ≈ GPT-2. 100,000 ≈ GPT-4.
→ *Run `exp01`, then `benchmarks/run_all.py` trains a 2,000-token BPE live.*

**Step 5 — One safety rail: never merge across word boundaries.** A regex chops text
into chunks first (`dog` | `.` | ` dog` | `!`). That is why `dog.` never becomes one
token — and why 4 spaces in Python broke GPT-2 but not GPT-4.
→ *Run `exp02_regex_boundary.py`: no vocabulary entry ever ends in `b"g."`.*

**Step 6 — Special tokens glue documents together.** `<|endoftext|>` separates
documents; chat models add `<|im_start|>`/`<|im_end|>` per message. Swapped in by exact
match only — which is why pasting them into a prompt can confuse a bot.
→ *Run `exp06_special_trailing.py` — and read the trailing-space warning below.*

**Step 7 — Now you are dangerous (in a good way).** Bills, context limits, spelling
failures, bad-at-math, non-English quality — all fall out of steps 1–6.
Prove each one next: playground → quiz → `exp03…exp08`.

---

## 🔬 Playground — feel tokenization

No install. Type in **[the website](docs/preview.html)** — it chunks your text exactly
like the repo's pre-tokenizer (letters / numbers / spaces / punctuation stay separate;
merges never cross chunks) and shows density live. Then reproduce it for real:

```bash
PYTHONPATH=src python experiments/exp03_arithmetic.py   # 127 vs 677 vs 804 splits
PYTHONPATH=src python experiments/exp04_code_whitespace.py  # live CPython bpt
```

## 🎯 Quiz — from scratch to pro

Six questions on **[the website](docs/preview.html)** (click any answer → instant
step-by-step reasoning, *"Let's work this out…"* style, score at the end):

1. Why not one token per Unicode character? 2. Why is `677` two tokens but `127` one?
3. Why was GPT-2 bad at Python indentation? 4. Why does Hindi cost 4× on `cl100k` but
1.6× on `o200k`? 5. What is a glitch token? 6. Why is YAML ~15% cheaper than JSON?

Classroom-ready: each answer ends with the exact `exp*.py` file that proves it.

---

## ✨ Features & user stories — what you can do with this repo

| If you are… | Do this | You get |
|---|---|---|
| 🎓 **Learning / interviewing** | Beginner guide → playground → quiz → `exp01…exp08` in order | From "what is a token" to reading merge tables; more than most candidates know |
| 💰 **Cutting LLM bills** | `make bench`, then measure `bytes/token` + parity on *your* prompts | YAML-over-JSON, `o200k`-over-`cl100k`, pre-translate-when-tax->2× decisions with numbers |
| 🌍 **Shipping multilingual products** | `exp05` + parity table on your languages | Per-language tax before launch; proof the fix works after |
| 🐍 **Debugging "model" bugs** | `exp03` (math), `exp04` (code), `exp06` (trailing space), `exp02` (punctuation) | One file per mystery, each runnable in seconds |
| 🛡️ **Auditing safety** | `exp06` (special-token gating) + `exp07` (glitch scan) | Never-firing / invalid-UTF8 tokens flagged before production prompts |
| 📝 **Publishing / reviewing** | `docker compose up --build` → `results/summary.json` + SHA manifests | Every figure regenerable by reviewers in one command |

**What this repo is:** a clean-room, ~200-line BPE + regex implementation, eight
claim-by-claim experiments on **live-fetched** public corpora (Wikipedia, Project
Gutenberg, CPython stdlib — nothing vendored), and a one-command benchmark comparing
5 tokenizers × 4 corpora (+ parity, + figures). **What it is not:** a new tokenizer to
use in production — use `tiktoken` for that; use this repo to *understand* it.

---

## 🚀 Quick start — 60 seconds

```bash
docker compose up --build
# writes results/summary.json + results/figures/parity_*.png (reproduces every number on this page)

# no docker?
make setup && make test      # 6 passed
make bench                   # live fetch + train (vocab 2000) + evaluate (~2-5 min)
PYTHONPATH=src python experiments/exp03_arithmetic.py
```

Open the site locally any time: `open docs/preview.html` (or serve `docs/` — see Pages below).

---

## 🗺 Repository map

```
src/tokphd/
  basic_bpe.py      # get_stats / merge / BasicTokenizer (train/encode/decode, errors=replace)
  regex_tokenizer.py# RegexTokenizer + GPT2_SPLIT_PATTERN + GPT4_SPLIT_PATTERN + special tokens
  metrics.py        # fertility, bytes_per_token, parity_ratio, unmerged_byte_rate
  live_data.py      # CORPORA + PARALLEL + fetch_live_corpus (SHA256 + timestamp)
experiments/
  exp01_bpe_correctness.py  # toy AA merge (AA x4 verified) + roundtrip
  exp02_regex_boundary.py   # dog./dog!/dog? never merge; no vocab entry ends b"g."
  exp03_arithmetic.py       # 127|677|804 splits (numbers above)
  exp04_code_whitespace.py  # live CPython: bpt 2.188 vs 4.889; 220-check
  exp05_multilingual_tax.py # parallel-sentence tax table (numbers above)
  exp06_special_trailing.py # <|endoftext|> gating + trailing-220 shift
  exp07_glitch.py           # 1MB scan: 8629/50257 seen; invalid-UTF8 -> U+FFFD
  exp08_json_yaml.py        # YAML saving 12-16%
benchmarks/run_all.py       # trains ours-basic/ours-regex (vocab 2000) on live Gutenberg
                            # + evaluates all 5 tokenizers x 4 corpora + parity + figures
tests/test_bpe.py           # 6 tests (stats, non-overlap, roundtrip, U+FFFD, boundary, metrics)
scripts/fetch_live.py       # pins data/live/*.txt + manifest.json
scripts/make_demo_gif.py    # regenerates docs/demo.gif (89 KB, 10 frames, loops forever)
results/summary.json        # machine-readable live results + figures/parity_*.png
docs/                       # 🌐 website: preview.html + demo.gif + screenshot + figures/
paper/PAPER.md              # 8-page draft skeleton wired to results/summary.json
```

Live-data policy: nothing vendored. `fetch_live_corpus()` records URL + UTC time +
SHA-256 per corpus; `scripts/fetch_live.py` pins `data/live/manifest.json`. If the
network is unavailable the harness falls back to a synthetic corpus and marks
`"sha256": "fallback"` — no silent substitution.

---

## 📊 Results — every number below was executed, not quoted

### Arithmetic is arbitrary by construction (EXP-03)
GPT-2: ` 127→[18112]` (one token) but ` 677→[718,3324]`, ` 804→[807,3023]` (two tokens
each); `127+677=804→[16799,10,40179,28,36088]`. `cl100k` keeps each whole (`[220,6804]`
etc.) because its 100k merges cover those frequent numerals. A digit-wise addition
algorithm must therefore operate over 1-, 2-, and 3-fragment encodings of the same
magnitude — the "arithmetic headwind".

### Code whitespace: GPT-2 bug → GPT-4 fix (EXP-04, live CPython `argparse.py`)
| tokenizer | tokens (20KB) | bytes/token |
|---|---|---|
| gpt2 | 9141 | 2.188 |
| cl100k_base | 4091 | **4.889** |
| o200k_base | 4114 | 4.861 |
`"    " → gpt2 [220×4]` vs `cl100k [1 tok]`. Same model, 2.24× denser context.

### Multilingual tax with remedy (EXP-05 + benchmark parity)
| lang | gpt2 | cl100k | o200k | ours-EN-only |
|---|---|---|---|---|
| es | 1.47 | 1.18 | **1.00** | 1.54 |
| ko | 4.41 | 1.82 | **1.12** | 3.19 |
| ar | 2.82 | 2.06 | **1.06** | 2.92 |
| hi | 6.18 | 4.06 | **1.56** | 6.69 |
Two independent levers confirmed: (a) marks-aware regex (`o200k` vs `cl100k`);
(b) balanced training data (multilingual `cl100k` 4.06× vs ours-EN-only 6.69× on Hindi
at identical algorithm — data balance beats vocab size).

![parity cl100k](docs/figures/parity_cl100k_base.png)
![parity o200k](docs/figures/parity_o200k_base.png)

### Trailing space, special tokens, formats, glitches (EXP-06/07/08)
Trailing space appends lone `220`, orphaning the next token's leading-space merge
(`[…6128]` → `[…,6128,220]`) — the Playground warning is a real distribution shift.
`<|endoftext|>` swaps in **only** under `allowed_special` (attack surface if user input
is scanned). YAML saves 12–16% over JSON on all three encodings. 1MB live scan sees
only 8,629/50,257 GPT-2 rows; bytes 94–100 (lone continuation bytes) decode to `�` —
the invalid-UTF8 path every decoder must handle.

---

## 🔬 Hidden pattern (candidate PhD contribution)

**Claim H1.** *Across corpora and tokenizers, word fertility is linearly predicted by
the unmerged-single-byte rate — i.e. the "tax" is mechanistically BPE merge failure
stranding bytes, not script entropy.*

Evidence: our live sweep (5 tokenizers × 4 corpora) gives Pearson **r = 0.72** between
fertility and unmerged-byte rate, same sign and magnitude family as the Indic
controlled study (r = 0.89). Our EN-only BPE is the crucial contrast: identical
algorithm, worst Hindi tax (6.69×) and highest unmerged rate — isolating
training-data composition as the causal lever, consistent with the "structural ceiling
vs data shortage" separation (broken regex shifts only 1.7% when Nepali share sweeps
5→95%, fixed shifts 33.9%).

Falsification hooks (for the follow-up paper): (i) train ours-regex on a Hindi-balanced
mix — H1 predicts unmerged rate and fertility fall together; (ii) swap GPT-2 regex for
marks-aware `o200k` class on identical merges — H1 predicts fertility falls with
unmerged rate fixed only where splits (not merges) were the blocker (Thai/abugida).

---

## 🌐 Website & GitHub Pages — 2 minutes

**This [`docs/preview.html`](docs/preview.html) page *is* the website** (single file,
no build step, works offline): hero + CEO summary + demo GIF + beginner guide +
interactive playground + 6-question quiz with step-by-step answers + live tables +
figures + Pages guide + FAQ.

**Publish it for your fork:**

1. Push this repo to GitHub (keep the `docs/` folder as-is).
2. Open **Settings → Pages**.
3. Under **Build and deployment → Source** choose **Deploy from a branch**.
4. Branch: **main**, folder: **`/docs`** → **Save**.
5. Wait ~1 minute → open **`https://<you>.github.io/<repo>/preview.html`**.

Why `/docs`? Pages serves static files directly — `preview.html`, `demo.gif`,
`screenshot-hero.png`, and `figures/` are all relatively linked, so they render both
locally (`open docs/preview.html`) and on Pages. No action, domain, or build needed.

---

## ❓ FAQ — the questions everyone asks

<details><summary>Do I need a GPU or API key?</summary>No. Everything runs on CPU with live <i>public</i> text. No keys, no weights, no cost.</details>
<details><summary>How long does the full benchmark take?</summary>~2–5 minutes on a laptop (trains a 2000-token BPE on 200KB + evaluates 5 tokenizers × 4 corpora).</details>
<details><summary>Why do numbers differ slightly run to run?</summary>Live pages drift; each run records URL + UTC time + SHA-256 in <code>results/summary.json</code>. Pin <code>data/live/manifest.json</code> for byte-identical reruns.</details>
<details><summary>Can I use this in a course / interview prep?</summary>Yes — Beginner guide → playground → quiz → <code>experiments/</code> in order. Each file is one claim, one page.</details>
<details><summary>Where is the "paper"?</summary>This README is the full study; <code>paper/PAPER.md</code> is the 8-page draft skeleton wired to <code>results/summary.json</code>.</details>
<details><summary>How do I regenerate the GIF?</summary><code>python scripts/make_demo_gif.py</code> → <code>docs/demo.gif</code> (verified 89 KB, 10 frames, infinite loop).</details>

---

## 📄 1. Abstract

Tokenization is the least loved yet most load-bearing stage of the large-language-model
pipeline. This repository re-derives it **from zero**: UTF-8 bytes → byte-pair encoding
(BPE, Gage 1994; Sennrich et al. 2016) → GPT-2 regex pre-tokenization → special tokens
→ evaluation with tokenizer-native metrics (fertility, bytes/token, parity,
unmerged-byte rate; cf. TokEval 2026, Tokka-Bench 2026).

**Contributions.** (i) A clean-room, ~200-line BPE + regex implementation with no copied
code, verified by 6 unit tests. (ii) Eight claim-by-claim experiments (EXP-01…EXP-08),
each mapped to a timestamped segment of the source lecture and each executed on
**live-fetched** public corpora (Wikipedia, Project Gutenberg, CPython stdlib) with
SHA-256 manifests. (iii) A one-command benchmark (`benchmarks/run_all.py`, Docker)
reproducing the headline effects — multilingual tax gradient, code-whitespace fix,
arithmetic fragmentation, JSON/YAML economy, glitch-token candidates — plus one
**new hidden pattern**: the per-corpus fertility is predicted by the BPE merge-failure
(unmerged-byte) rate (r=0.72 on our live sweep).

## 📄 2. Research method (multi-source literature review, 2026–2027)

Findings below survived cross-checking across independent providers and paper families
with distinct query angles (no single source trusted alone). Consensus:

1. **BPE-from-scratch is sufficient** to explain GPT-2/4 behaviour (inference +
merge ranks fully determine encoding; training code was never released).
2. **Standard BPE remains a strong baseline** (recent cross-lingual BPB studies:
SuperBPE/MorphBPE underperform BPE on Hungarian/Mandarin; tokenizers-as-structured-compressors view).
3. **Pre-tokenization is the mechanism, not a detail**: a letters-only word class with
no marks imposes a *training-free fertility floor* up to 9.02× on Thai-class scripts;
the marks-aware class in the newest generation is the documented fix.
4. **Fertility ≠ bytes/token for code** (allocation matters more than raw vocab size;
a smaller balanced vocabulary beats a larger English-leaning one; code efficiency has
converged across recent tokenizers while natural-language profiles still diverge).
5. **Glitch tokens = train/inference distribution mismatch** (under-trained rows of the
embedding table behave as unallocated memory; model-free proxy: never-firing tokens).
6. **Compute-optimal framing**: bytes (not tokens) per parameter is the transferable unit
(~60 bytes/param); byte-level retrofit now matches subword performance — tokenizer-free
modelling is viable but not yet default.

## 📄 7. Threats to validity

Parallel sentences are short and translationese-prone; whitespace-fertility is ill-defined
for some scripts (we also report tokens/char and bytes/token); accuracy-vs-fertility
correlation is confounded by resource level (we report only model-free context-loss);
1MB scan underpowers glitch detection (model-free proxy, not embedding-norm proof);
live URLs drift (mitigated by SHA-256 manifests).

## 📄 8. References

Byte-pair encoding (Gage 1994; Sennrich et al. 2016); GPT-2; SentencePiece
(Kudo & Richardson 2018); EACL 2026 tokenizer-as-design survey; cross-lingual BPB
benchmark 2026; information-theoretic tokenizer study 2026; TokEval 2026; Tokka-Bench
2026; vowel-sign pre-tokenization ceiling 2026; Indic tokenizer-tax study 2026;
parity-aware BPE 2026; BoundlessBPE 2025; compute-optimal tokenization (FAIR) 2026;
byte-level retrofit (Nature) 2026; Fishing-for-Magikarp glitch study 2024; tiktoken;
HuggingFace tokenizers v1.

## 📄 9. Reproduce → extend → publish

- `paper/PAPER.md`: full 8-page draft skeleton with tables/figures placeholders wired to
  `results/summary.json`.
- Next experiments (spec'd, not run): vocab-size sweep 2k→100k (sweet-spot curve);
  Hindi-balanced retrain (H1 causal test); marks-aware regex ablation (Thai/Nepali);
  embedding-norm glitch proof on an open-weights model.
- Cite as: `tokenization-zero-to-hero-phd-2026, live-verified BPE replication + benchmark`.

---

## 📜 License & citation

MIT — use it in courses, interviews, products, and papers. If you publish from it,
please cite the live-run SHA manifest in `results/summary.json` alongside the repo link
so reviewers can regenerate your exact numbers:

```bibtex
@software{tokphd2026,
  title  = {Tokenization Zero-to-Hero: live-verified BPE replication + benchmark},
  year   = {2026},
  note   = {docker compose up --build; results/summary.json (SHA-pinned live corpora)}
}
```
