import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results"
FIGURES_DIR = Path(__file__).parent.parent / "paper" / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

with open(RESULTS_DIR / "benchmark_results.json") as f:
    bench = json.load(f)
with open(RESULTS_DIR / "results_by_task.json") as f:
    by_task = json.load(f)
with open(RESULTS_DIR / "results_by_platform.json") as f:
    by_platform = json.load(f)

MODEL_ORDER = [
    "claude-opus-4-6",
    "claude-opus-4-5",
    "gpt-5.2",
    "claude-sonnet-4-5",
    "gpt-5.1",
    "grok-4.1",
    "grok-4",
    "gemini-2.5-pro",
]

MODEL_LABELS = {
    "claude-opus-4-6": "Opus 4.6",
    "claude-opus-4-5": "Opus 4.5",
    "gpt-5.2": "GPT-5.2",
    "claude-sonnet-4-5": "Sonnet 4.5",
    "gpt-5.1": "GPT-5.1",
    "grok-4.1": "Grok-4.1",
    "grok-4": "Grok-4",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
}

MODEL_COLORS = {
    "claude-opus-4-6": "#4E79A7",
    "claude-opus-4-5": "#76A3C7",
    "gpt-5.2": "#E15759",
    "claude-sonnet-4-5": "#A0CBE8",
    "gpt-5.1": "#F1A07A",
    "grok-4.1": "#59A14F",
    "grok-4": "#8CD17D",
    "gemini-2.5-pro": "#B07AA1",
}

TASK_ORDER = [
    "normalization",
    "qc",
    "dimensionality_reduction",
    "clustering",
    "cell_typing",
    "differential_expression",
    "trajectory_analysis",
]

TASK_LABELS = {
    "normalization": "Normalization",
    "qc": "QC",
    "dimensionality_reduction": "Dim. Reduction",
    "clustering": "Clustering",
    "cell_typing": "Cell Typing",
    "differential_expression": "Diff. Expression",
    "trajectory_analysis": "Traj. Analysis",
}

PLATFORM_ORDER = [
    "csgenetics",
    "bd_rhapsody",
    "illumina",
    "chromium",
    "parsebio",
    "missionbio",
]

PLATFORM_LABELS = {
    "csgenetics": "CSGenetics",
    "bd_rhapsody": "BD Rhapsody",
    "illumina": "Illumina",
    "chromium": "Chromium",
    "parsebio": "ParseBio",
    "missionbio": "MissionBio",
}

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.titleweight": "medium",
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 6.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.4,
    "ytick.major.width": 0.4,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
})


def fig_aggregate():
    models_data = {m["id"]: m for m in bench["models"]}
    active_models = [m for m in MODEL_ORDER if m in models_data]
    means = [models_data[m]["accuracy"]["mean"] for m in active_models]
    ci_lo = [models_data[m]["accuracy"]["ci_lower"] for m in active_models]
    ci_hi = [models_data[m]["accuracy"]["ci_upper"] for m in active_models]
    errs = [[m - lo for m, lo in zip(means, ci_lo)],
            [hi - m for m, hi in zip(means, ci_hi)]]
    colors = [MODEL_COLORS[m] for m in active_models]
    labels = [MODEL_LABELS[m] for m in active_models]

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    x = np.arange(len(active_models))
    bars = ax.bar(x, means, yerr=errs, capsize=2.5, color=colors,
                  edgecolor="white", linewidth=0.3, width=0.65,
                  error_kw={"linewidth": 0.8, "color": "#444"})
    for bar, val, hi in zip(bars, means, ci_hi):
        ax.text(bar.get_x() + bar.get_width() / 2, hi + 1.5,
                f"{val:.1f}", ha="center", va="bottom", fontsize=5.5,
                color="#333")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=6.5)
    ax.set_ylabel("Accuracy (%)")
    max_hi = max(ci_hi)
    ax.set_ylim(0, max_hi + 12)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
    ax.grid(axis="y", which="major", linewidth=0.5, color="#ccc", zorder=0)
    ax.grid(axis="y", which="minor", linewidth=0.3, color="#eee", zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    n_evals = bench["metadata"]["n_evaluations"]
    ax.set_title(f"Aggregate Model Performance ({n_evals} evaluations)", fontsize=8)
    fig.savefig(FIGURES_DIR / "aggregate_performance.pdf")
    fig.savefig(FIGURES_DIR / "aggregate_performance.png")
    plt.close(fig)


def fig_task_heatmap():
    task_data = by_task["tasks"]
    active_tasks = [t for t in TASK_ORDER if t in task_data]
    active_models = [m for m in MODEL_ORDER if any(
        m in task_data.get(t, {}).get("models", {}) for t in active_tasks
    )]
    grid = np.full((len(active_tasks), len(active_models)), np.nan)
    for i, task in enumerate(active_tasks):
        for j, model in enumerate(active_models):
            v = task_data.get(task, {}).get("models", {}).get(model, {})
            if v:
                grid[i, j] = v["mean"]

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    im = ax.imshow(grid, cmap="YlOrRd", aspect="auto", vmin=0, vmax=90)
    ax.set_xticks(np.arange(len(active_models)))
    ax.set_xticklabels([MODEL_LABELS[m] for m in active_models], rotation=35, ha="right")
    ax.set_yticks(np.arange(len(active_tasks)))
    ax.set_yticklabels([TASK_LABELS[t] for t in active_tasks])
    for i in range(len(active_tasks)):
        for j in range(len(active_models)):
            val = grid[i, j]
            if np.isnan(val):
                continue
            color = "white" if val > 55 else "black"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=7.5, color=color, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Accuracy (%)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    ax.set_title("Performance by Task Category")
    fig.savefig(FIGURES_DIR / "task_heatmap.pdf")
    fig.savefig(FIGURES_DIR / "task_heatmap.png")
    plt.close(fig)


def _grouped_bar(ax, categories, cat_labels, data_fn, active_models):
    n_cats = len(categories)
    n_models = len(active_models)
    bar_w = 0.8 / n_models
    x = np.arange(n_cats)
    for j, model in enumerate(active_models):
        entries = [data_fn(c, model) for c in categories]
        vals = [e["mean"] if isinstance(e, dict) else e for e in entries]
        offset = (j - n_models / 2 + 0.5) * bar_w
        ax.bar(x + offset, vals, bar_w,
               label=MODEL_LABELS[model], color=MODEL_COLORS[model],
               edgecolor="white", linewidth=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels)
    ax.set_ylabel("Accuracy (%)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.grid(axis="y", linewidth=0.3, color="#ddd", zorder=0)
    ax.set_axisbelow(True)


def fig_task_grouped():
    task_data = by_task["tasks"]
    active_tasks = [t for t in TASK_ORDER if t in task_data]
    active_models = [m for m in MODEL_ORDER if any(
        m in task_data.get(t, {}).get("models", {}) for t in active_tasks
    )]
    labels = [TASK_LABELS[t] for t in active_tasks]

    fig, ax = plt.subplots(figsize=(8, 3.2))
    _grouped_bar(
        ax, active_tasks, labels,
        lambda t, m: task_data.get(t, {}).get("models", {}).get(m, {"mean": 0}),
        active_models,
    )
    ax.set_ylim(0, 95)
    ax.legend(ncol=4, loc="upper right", framealpha=0.9, edgecolor="none")
    ax.set_title("Performance by Task Category")
    fig.savefig(FIGURES_DIR / "task_comparison.pdf")
    fig.savefig(FIGURES_DIR / "task_comparison.png")
    plt.close(fig)


def fig_platform_grouped():
    plat_data = by_platform["platforms"]
    active_plats = [p for p in PLATFORM_ORDER if p in plat_data]
    active_models = [m for m in MODEL_ORDER if any(
        m in plat_data.get(p, {}).get("models", {}) for p in active_plats
    )]
    labels = [PLATFORM_LABELS[p] for p in active_plats]

    fig, ax = plt.subplots(figsize=(7, 3.2))
    _grouped_bar(
        ax, active_plats, labels,
        lambda p, m: plat_data.get(p, {}).get("models", {}).get(m, {"mean": 0}),
        active_models,
    )
    ax.set_ylim(0, 85)
    ax.legend(ncol=4, loc="upper right", framealpha=0.9, edgecolor="none")
    ax.set_title("Performance by Sequencing Platform")
    fig.savefig(FIGURES_DIR / "platform_comparison.pdf")
    fig.savefig(FIGURES_DIR / "platform_comparison.png")
    plt.close(fig)


def fig_task_platform_combined():
    task_data = by_task["tasks"]
    plat_data = by_platform["platforms"]
    active_tasks = [t for t in TASK_ORDER if t in task_data]
    active_plats = [p for p in PLATFORM_ORDER if p in plat_data]
    active_models = [m for m in MODEL_ORDER if any(
        m in task_data.get(t, {}).get("models", {}) for t in active_tasks
    )]

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5), gridspec_kw={"wspace": 0.35})

    ax = axes[0]
    grid = np.full((len(active_tasks), len(active_models)), np.nan)
    for i, task in enumerate(active_tasks):
        for j, model in enumerate(active_models):
            v = task_data.get(task, {}).get("models", {}).get(model, {})
            if v:
                grid[i, j] = v["mean"]
    im = ax.imshow(grid, cmap="YlOrRd", aspect="auto", vmin=0, vmax=90)
    ax.set_xticks(np.arange(len(active_models)))
    ax.set_xticklabels([MODEL_LABELS[m] for m in active_models], rotation=40, ha="right")
    ax.set_yticks(np.arange(len(active_tasks)))
    ax.set_yticklabels([TASK_LABELS[t] for t in active_tasks])
    for i in range(len(active_tasks)):
        for j in range(len(active_models)):
            val = grid[i, j]
            if np.isnan(val):
                continue
            color = "white" if val > 55 else "black"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=6.5, color=color, fontweight="bold")
    ax.set_title("(a) By Task Category", fontsize=9)

    ax = axes[1]
    grid2 = np.full((len(active_plats), len(active_models)), np.nan)
    for i, plat in enumerate(active_plats):
        for j, model in enumerate(active_models):
            v = plat_data.get(plat, {}).get("models", {}).get(model, {})
            if v:
                grid2[i, j] = v["mean"]
    im2 = ax.imshow(grid2, cmap="YlOrRd", aspect="auto", vmin=0, vmax=90)
    ax.set_xticks(np.arange(len(active_models)))
    ax.set_xticklabels([MODEL_LABELS[m] for m in active_models], rotation=40, ha="right")
    ax.set_yticks(np.arange(len(active_plats)))
    ax.set_yticklabels([PLATFORM_LABELS[p] for p in active_plats])
    for i in range(len(active_plats)):
        for j in range(len(active_models)):
            val = grid2[i, j]
            if np.isnan(val):
                continue
            color = "white" if val > 55 else "black"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=6.5, color=color, fontweight="bold")
    ax.set_title("(b) By Platform", fontsize=9)

    cbar = fig.colorbar(im2, ax=axes, shrink=0.75, pad=0.02, location="bottom",
                        aspect=40)
    cbar.set_label("Accuracy (%)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    fig.savefig(FIGURES_DIR / "task_platform_heatmap.pdf")
    fig.savefig(FIGURES_DIR / "task_platform_heatmap.png")
    plt.close(fig)


def fig_pareto():
    models_data = {m["id"]: m for m in bench["models"]}

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.2), gridspec_kw={"wspace": 0.35})

    for ax, metric_key, xlabel, title_suffix in [
        (axes[0], "cost_usd", "Cost per Eval (USD)", "Cost"),
        (axes[1], "time_s", "Latency per Eval (s)", "Latency"),
    ]:
        points = []
        for m_id in MODEL_ORDER:
            m = models_data.get(m_id)
            if m is None or metric_key not in m:
                continue
            points.append((m_id, m[metric_key]["mean"], m["accuracy"]["mean"]))

        points.sort(key=lambda p: p[1])
        best_acc = -1
        frontier = []
        for m_id, x_val, acc in points:
            if acc > best_acc:
                frontier.append(m_id)
                best_acc = acc

        for m_id, x_val, acc in points:
            m = models_data[m_id]
            acc_lo = m["accuracy"]["ci_lower"]
            acc_hi = m["accuracy"]["ci_upper"]
            x_lo = m[metric_key]["ci_lower"]
            x_hi = m[metric_key]["ci_upper"]
            ax.errorbar(
                x_val, acc,
                yerr=[[acc - acc_lo], [acc_hi - acc]],
                xerr=[[x_val - x_lo], [x_hi - x_val]],
                fmt="none", ecolor="#999", elinewidth=0.6, capsize=2, capthick=0.5,
                zorder=2,
            )
            ax.scatter(
                x_val, acc, s=50, color=MODEL_COLORS[m_id],
                edgecolor="white", linewidth=0.4, zorder=3,
            )
            ax.annotate(
                MODEL_LABELS[m_id], (x_val, acc_hi),
                textcoords="offset points", xytext=(0, 3),
                ha="center", va="bottom", fontsize=6.5,
            )

        if len(frontier) >= 2:
            frontier_pts = [(models_data[m][metric_key]["mean"], models_data[m]["accuracy"]["mean"]) for m in frontier]
            frontier_pts.sort(key=lambda p: p[0])
            fx, fy = zip(*frontier_pts)
            ax.plot(fx, fy, color="#999", linewidth=1, linestyle="--", zorder=1)

        ax.set_xlabel(xlabel)
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(f"Accuracy vs. {title_suffix}")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="both", linewidth=0.3, color="#ddd", zorder=0)
        ax.set_axisbelow(True)

    fig.savefig(FIGURES_DIR / "pareto_cost_latency.pdf")
    fig.savefig(FIGURES_DIR / "pareto_cost_latency.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_aggregate()
    print("Generated aggregate_performance.pdf")
    fig_task_heatmap()
    print("Generated task_heatmap.pdf")
    fig_task_grouped()
    print("Generated task_comparison.pdf")
    fig_platform_grouped()
    print("Generated platform_comparison.pdf")
    fig_task_platform_combined()
    print("Generated task_platform_heatmap.pdf")
    fig_pareto()
    print("Generated pareto_cost_latency.pdf")
    print(f"All figures saved to {FIGURES_DIR}")
