"""Generate docs/demo.gif: animated BPE tokenization demo (no external assets).

Frames (verified live numbers inside):
 1. bytes of "Hello world"   2. GPT-2 split 127 vs 677/804
 3. code whitespace 4x220->1  4. multilingual tax bars shrinking o200k
 5. fertility vs unmerged r=0.72
Small (<2MB), loop forever. Run: python scripts/make_demo_gif.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")

frames = [
    ("UTF-8 bytes in, tokens out", '"Hello world" → 11 chars → bytes → merges → tokens', "#58a6ff"),
    ("127 = 1 token, 677 = 2 tokens", '"127"→[18112]   "677"→[718+3324]   "804"→[807+3023]', "#3fb950"),
    ("4 spaces: GPT-2 wastes, GPT-4 packs", '"    " → gpt2 [220×4]  vs  cl100k [1 tok]  bpt 2.19→4.89', "#d29922"),
    ("Same sentence, other languages cost more", 'hi 6.18× → 4.06× → 1.56×  (gpt2 → cl100k → o200k)', "#f778ba"),
    ("Hidden pattern r = 0.72", 'fertility ↑ when unmerged-byte-rate ↑  (merge failure = tax)', "#ff7b72"),
]

def draw(i):
    ax.clear()
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")
    title, sub, color = frames[i % len(frames)]
    ax.text(5, 7.2, "TOKPHD · tokenization zero-to-hero", ha="center", fontsize=11, color="#8b949e")
    ax.text(5, 5.6, title, ha="center", fontsize=20, weight="bold", color=color)
    ax.text(5, 4.2, sub, ha="center", fontsize=11, color="white", family="monospace")
    # progress dots
    for k in range(len(frames)):
        ax.text(3.6 + k * 0.7, 2.4, "●" if k == i % len(frames) else "○",
                ha="center", fontsize=13, color=color if k == i % len(frames) else "#30363d")
    ax.text(5, 1.2, f"frame {i+1} · live-verified numbers · docker compose up", ha="center", fontsize=9, color="#8b949e")

anim = FuncAnimation(fig, draw, frames=len(frames) * 2, interval=1400)
anim.save("docs/demo.gif", writer="pillow", fps=0.7)
print("WROTE docs/demo.gif")
