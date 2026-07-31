# Figure generation for the Effective Composition paper.
# Draws the five reference bipartite relations of the possibilistic layer, with their
# maximal independence blocks (maximal bicliques) highlighted.
# Deterministic output: set SOURCE_DATE_EPOCH=0 before running so the PDF metadata is stable.
# Pinned environment: see requirements.txt (matplotlib==3.10.8).
# Usage (from the repository root):
#   SOURCE_DATE_EPOCH=0 python3 code/make_figures.py
# Output: out/fig_relations.pdf (git-ignored; identity carried by ARTIFACT_SHA256SUMS).

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RELATIONS = [
    ("complete", 2, 2, [(a, b) for a in range(2) for b in range(2)],
     [([0, 1], [0, 1])]),
    ("diagonal", 2, 2, [(0, 0), (1, 1)],
     [([0], [0]), ([1], [1])]),
    ("L-shape", 2, 2, [(0, 0), (0, 1), (1, 0)],
     [([0], [0, 1]), ([0, 1], [0])]),
    ("two rectangles", 4, 4,
     [(a, b) for a in (0, 1) for b in (0, 1)] + [(a, b) for a in (2, 3) for b in (2, 3)],
     [([0, 1], [0, 1]), ([2, 3], [2, 3])]),
    ("6-cycle", 3, 3, [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 0)],
     [([0], [0, 1]), ([1], [1, 2]), ([2], [0, 2]), ([0, 1], [1]), ([1, 2], [2]), ([0, 2], [0])]),
]

BLOCK_COLORS = ["#1b7837", "#762a83", "#2166ac", "#b2182b", "#e08214", "#35978f"]


def draw_relation(ax, name, nA, nB, edges, max_blocks):
    yA = {a: -(a - (nA - 1) / 2.0) for a in range(nA)}
    yB = {b: -(b - (nB - 1) / 2.0) for b in range(nB)}
    # base edges
    for (a, b) in edges:
        ax.plot([0, 1], [yA[a], yB[b]], color="#bbbbbb", lw=1.2, zorder=1)
    # maximal blocks: overdraw their rectangles in colour
    for k, (SA, SB) in enumerate(max_blocks):
        c = BLOCK_COLORS[k % len(BLOCK_COLORS)]
        for a in SA:
            for b in SB:
                ax.plot([0, 1], [yA[a], yB[b]], color=c, lw=2.0, alpha=0.85, zorder=2)
    for a in range(nA):
        ax.plot(0, yA[a], "o", color="black", ms=6, zorder=3)
        ax.annotate(str(a), (0, yA[a]), textcoords="offset points", xytext=(-12, -3), fontsize=9)
    for b in range(nB):
        ax.plot(1, yB[b], "s", color="black", ms=6, zorder=3)
        ax.annotate(str(b), (1, yB[b]), textcoords="offset points", xytext=(7, -3), fontsize=9)
    ax.set_title(name, fontsize=10)
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(min(min(yA.values()), min(yB.values())) - 0.6,
                max(max(yA.values()), max(yB.values())) + 0.6)
    ax.axis("off")


def main():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")
    os.makedirs(out_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 5, figsize=(11.5, 2.6))
    for ax, (name, nA, nB, edges, blocks) in zip(axes, RELATIONS):
        draw_relation(ax, name, nA, nB, edges, blocks)
    fig.suptitle("Five reference relations $R$ (grey edges) and their maximal independence blocks "
                 "(coloured bicliques)", fontsize=11, y=1.02)
    fig.tight_layout()
    path = os.path.join(out_dir, "fig_relations.pdf")
    fig.savefig(path, bbox_inches="tight")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
