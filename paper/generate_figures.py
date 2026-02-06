import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8

COLORS = {
    'claude': '#D97706',
    'openai': '#059669',
    'xai': '#7C3AED',
    'google': '#2563EB',
}

MODEL_COLORS = {
    'Opus 4.6': COLORS['claude'],
    'Opus 4.5': COLORS['claude'],
    'Sonnet 4.5': COLORS['claude'],
    'GPT-5.2': COLORS['openai'],
    'GPT-5.1': COLORS['openai'],
    'Grok-4.1': COLORS['xai'],
    'Grok-4': COLORS['xai'],
    'Gemini': COLORS['google'],
}

TASK_COLORS = {
    'QC': '#94a3b8',
    'Norm.': '#64748b',
    'Dim. Red.': '#475569',
    'Clust.': '#334155',
    'Cell Typ.': '#1e293b',
    'Diff. Expr.': '#0f172a',
    'Traj.': '#020617',
}


def fig1_benchmark_overview():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    box_style = dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#374151', linewidth=1.5)

    ax.text(1, 3, 'Data\n(.h5ad)', ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#dbeafe', edgecolor='#2563eb', linewidth=1.5))

    ax.text(1, 1.5, 'Task\nPrompt', ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#fef3c7', edgecolor='#d97706', linewidth=1.5))

    ax.text(4, 2.25, 'AI Agent', ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#f3e8ff', edgecolor='#7c3aed', linewidth=2))

    ax.text(6.5, 2.25, 'JSON\nAnswer', ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#ecfdf5', edgecolor='#059669', linewidth=1.5))

    ax.text(8.5, 2.25, 'Grader', ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#fef2f2', edgecolor='#dc2626', linewidth=1.5))

    arrow_style = dict(arrowstyle='->', color='#6b7280', lw=1.5, mutation_scale=15)
    ax.annotate('', xy=(2.8, 2.6), xytext=(1.8, 3), arrowprops=arrow_style)
    ax.annotate('', xy=(2.8, 1.9), xytext=(1.8, 1.5), arrowprops=arrow_style)
    ax.annotate('', xy=(5.5, 2.25), xytext=(5.2, 2.25), arrowprops=arrow_style)
    ax.annotate('', xy=(7.7, 2.25), xytext=(7.3, 2.25), arrowprops=arrow_style)

    ax.text(9.5, 3.2, 'Pass', ha='center', va='center', fontsize=11, fontweight='bold', color='#059669')
    ax.text(9.5, 1.3, 'Fail', ha='center', va='center', fontsize=11, fontweight='bold', color='#dc2626')
    ax.annotate('', xy=(9.5, 2.9), xytext=(9.2, 2.5), arrowprops=dict(arrowstyle='->', color='#059669', lw=1.5))
    ax.annotate('', xy=(9.5, 1.6), xytext=(9.2, 2.0), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.5))

    ax.text(5, 0.3, 'Each evaluation: data snapshot + natural language prompt + deterministic grader',
            ha='center', va='center', fontsize=9, style='italic', color='#6b7280')

    plt.tight_layout()
    plt.savefig('figures/benchmark_overview.pdf', bbox_inches='tight', dpi=300)
    plt.savefig('figures/benchmark_overview.png', bbox_inches='tight', dpi=300)
    plt.close()
    print('Saved benchmark_overview.pdf')


def fig2_inventory():
    platforms = ['Illumina', 'MissionBio', 'ParseBio', 'BD Rhapsody', 'Chromium', 'CSGenetics']
    platform_totals = [85, 81, 65, 61, 60, 42]

    tasks = ['Cell Typing', 'Diff. Expr.', 'Dim. Reduction', 'Clustering', 'Normalization', 'QC', 'Trajectory']
    task_totals = [118, 71, 69, 49, 44, 36, 7]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    colors_platform = ['#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6', '#3b82f6']
    colors_task = ['#10b981', '#10b981', '#10b981', '#10b981', '#10b981', '#10b981', '#10b981']

    y1 = np.arange(len(platforms))
    ax1.barh(y1, platform_totals, color='#3b82f6', edgecolor='white', height=0.7)
    ax1.set_yticks(y1)
    ax1.set_yticklabels(platforms, fontsize=10)
    ax1.set_xlabel('Number of Evaluations', fontsize=10)
    ax1.set_title('By Platform', fontsize=11, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_xlim(0, 100)
    for i, v in enumerate(platform_totals):
        ax1.text(v + 2, i, str(v), va='center', fontsize=9)

    y2 = np.arange(len(tasks))
    ax2.barh(y2, task_totals, color='#10b981', edgecolor='white', height=0.7)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(tasks, fontsize=10)
    ax2.set_xlabel('Number of Evaluations', fontsize=10)
    ax2.set_title('By Task Category', fontsize=11, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_xlim(0, 130)
    for i, v in enumerate(task_totals):
        ax2.text(v + 2, i, str(v), va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('figures/inventory_bars.pdf', bbox_inches='tight', dpi=300)
    plt.savefig('figures/inventory_bars.png', bbox_inches='tight', dpi=300)
    plt.close()
    print('Saved inventory_bars.pdf')


def fig2b_inventory_heatmap():
    platforms = ['BD Rhapsody', 'Chromium', 'CSGenetics', 'Illumina', 'MissionBio', 'ParseBio']
    tasks = ['QC', 'Norm.', 'Dim. Red.', 'Clust.', 'Cell Typ.', 'Diff. Exp.', 'Traj.']

    data = np.array([
        [6, 11, 14, 7, 13, 10, 0],
        [10, 11, 15, 8, 5, 11, 0],
        [4, 5, 7, 5, 20, 1, 0],
        [8, 7, 10, 12, 33, 8, 7],
        [8, 3, 5, 12, 34, 19, 0],
        [0, 7, 18, 5, 13, 22, 0],
    ])

    fig, ax = plt.subplots(figsize=(8, 5))

    im = ax.imshow(data, cmap='Blues', aspect='auto')

    ax.set_xticks(np.arange(len(tasks)))
    ax.set_yticks(np.arange(len(platforms)))
    ax.set_xticklabels(tasks, fontsize=10)
    ax.set_yticklabels(platforms, fontsize=10)

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

    for i in range(len(platforms)):
        for j in range(len(tasks)):
            val = data[i, j]
            if val > 0:
                color = 'white' if val > 15 else 'black'
                ax.text(j, i, str(val), ha='center', va='center', color=color, fontsize=9)
            else:
                ax.text(j, i, '—', ha='center', va='center', color='#9ca3af', fontsize=9)

    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.set_ylabel('Number of Evaluations', rotation=-90, va='bottom', fontsize=10)

    ax.set_title('394 Evaluations by Platform and Task Category', fontsize=11, fontweight='bold', pad=10)

    plt.tight_layout()
    plt.savefig('figures/inventory_heatmap.pdf', bbox_inches='tight', dpi=300)
    plt.savefig('figures/inventory_heatmap.png', bbox_inches='tight', dpi=300)
    plt.close()
    print('Saved inventory_heatmap.pdf')


def fig3_benchmark_comparison():
    with open('../results/benchmark_results.json') as f:
        scbench_data = json.load(f)

    models = ['Opus 4.6', 'Opus 4.5', 'GPT-5.2', 'Sonnet 4.5', 'GPT-5.1', 'Grok-4.1', 'Grok-4', 'Gemini']

    scbench_acc = [52.8, 49.9, 45.2, 44.2, 37.9, 35.6, 33.9, 29.2]
    scbench_ci = [
        (48.3, 57.2), (45.3, 54.4), (40.9, 49.5), (39.9, 48.6),
        (33.7, 42.0), (31.6, 39.7), (30.1, 37.8), (25.6, 32.9)
    ]

    spatialbench_acc = [38.4, 36.2, 32.1, 31.5, 28.3, 25.7, 24.9, 20.1]
    spatialbench_ci = [
        (33.1, 43.7), (31.0, 41.4), (27.2, 37.0), (26.5, 36.5),
        (23.5, 33.1), (21.2, 30.2), (20.4, 29.4), (16.0, 24.2)
    ]

    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(models))
    width = 0.35

    sc_err = [(acc - ci[0], ci[1] - acc) for acc, ci in zip(scbench_acc, scbench_ci)]
    sp_err = [(acc - ci[0], ci[1] - acc) for acc, ci in zip(spatialbench_acc, spatialbench_ci)]

    colors = [MODEL_COLORS[m] for m in models]

    bars1 = ax.bar(x - width/2, scbench_acc, width, label='scBench',
                   color=colors, alpha=0.9,
                   yerr=np.array(sc_err).T, capsize=3, error_kw={'linewidth': 1})

    bars2 = ax.bar(x + width/2, spatialbench_acc, width, label='SpatialBench',
                   color=colors, alpha=0.5,
                   yerr=np.array(sp_err).T, capsize=3, error_kw={'linewidth': 1},
                   hatch='//')

    ax.set_ylabel('Accuracy (%)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9, rotation=15, ha='right')
    ax.set_ylim(0, 70)
    ax.legend(loc='upper right', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.axhline(y=50, color='#9ca3af', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.text(7.5, 51, '50%', fontsize=8, color='#6b7280')

    plt.tight_layout()
    plt.savefig('figures/benchmark_comparison.pdf', bbox_inches='tight', dpi=300)
    plt.savefig('figures/benchmark_comparison.png', bbox_inches='tight', dpi=300)
    plt.close()
    print('Saved benchmark_comparison.pdf')


if __name__ == '__main__':
    fig1_benchmark_overview()
    fig2_inventory()
    fig2b_inventory_heatmap()
    fig3_benchmark_comparison()
    print('All figures generated.')
