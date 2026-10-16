# PAPER DRAFT — Tokenization Is the Model (Before the Model): A Live-Verified Replication

**Track:** reproducibility / tokenizer evaluation. **Artifact:** this repo (code + live data manifests).

## 1. Introduction
Restate README §1 + Karpathy timestamp map (00:00 motivation → 15:21 UTF-8 →
22:59 BPE → 57:37 GPT-2 regex → 1:18:36 special tokens → 1:28:43 SentencePiece →
1:43:29 vocab sizing → 1:50:03 multimodal → 1:51:35 failure tour).

## 2. Related work (2026 voted consensus)
Table: claim | sources (≥2 providers) | status (confirmed / refined / contested).
Rows: BPE baseline strength; pre-tokenization ceiling; parity-aware training;
compute-optimal bytes/param; byteification viability; glitch mechanism.

## 3. Method
3.1 Clean-room BPE + regex (algorithms verbatim; no copied code).
3.2 Metrics (TokEval-compatible definitions).
3.3 Live-data protocol (fetch → SHA256 → fallback flag → parallel-sentence control).
3.4 Voting search protocol (providers × keywords table; Exa first, one-at-a-time, 429 backoff).

## 4. Experiments EXP-01…EXP-08
One subsection each: hypothesis (video timestamp) → procedure → live result →
verdict. Paste outputs from §5 of README (numbers already verified by execution).

## 5. New result H1 (hidden pattern)
Figure: fertility vs unmerged-byte-rate scatter (r=0.72) + parity bars
(`results/figures/parity_*.png`). Compare with Srivastava r=0.89; discuss why ours is
lower (short parallel sentences + mixed domains). Pre-register falsification runs.

## 6. Threats, ethics (glitch-token safety), cost (token-tax fairness)
## 7. Conclusion + artifact checklist
Tables wired to `results/summary.json`; no number without a SHA + timestamp.
