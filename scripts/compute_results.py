#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats


RAW_RESULTS_DIR = Path(__file__).parent.parent / "trajectories" / "minisweagent"
OUTPUT_DIR = Path(__file__).parent.parent / "results"

MODEL_DISPLAY = {
    "claude-opus-4-6": "Claude Opus 4.6",
    "claude-opus-4-5": "Claude Opus 4.5",
    "claude-sonnet-4-5": "Claude Sonnet 4.5",
    "gpt-5.2": "GPT-5.2",
    "gpt-5.1": "GPT-5.1",
    "grok-4": "Grok-4",
    "grok-4.1": "Grok-4.1",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
}

MODEL_PROVIDER = {
    "claude-opus-4-6": "Anthropic",
    "claude-opus-4-5": "Anthropic",
    "claude-sonnet-4-5": "Anthropic",
    "gpt-5.2": "OpenAI",
    "gpt-5.1": "OpenAI",
    "grok-4": "xAI",
    "grok-4.1": "xAI",
    "gemini-2.5-pro": "Google",
}

PLATFORMS = [
    "chromium",
    "bd_rhapsody",
    "csgenetics",
    "illumina",
    "missionbio",
    "parsebio",
]

TASKS = [
    "qc",
    "normalization",
    "dimensionality_reduction",
    "clustering",
    "cell_typing",
    "differential_expression",
    "trajectory_analysis",
]

TASK_ALIASES = {
    "dimension_reduction": "dimensionality_reduction",
}


def normalize_model_name(raw: str) -> str:
    mapping = {
        "anthropic_claude-opus-4-6": "claude-opus-4-6",
        "anthropic_claude-opus-4-5": "claude-opus-4-5",
        "anthropic_claude-sonnet-4-5": "claude-sonnet-4-5",
        "anthropic/claude-opus-4-6": "claude-opus-4-6",
        "anthropic/claude-opus-4-5": "claude-opus-4-5",
        "anthropic/claude-sonnet-4-5": "claude-sonnet-4-5",
        "gemini_gemini-2-5-pro": "gemini-2.5-pro",
        "gemini_gemini-2.5-pro": "gemini-2.5-pro",
        "openai_gpt-5-1": "gpt-5.1",
        "openai_gpt-5.1": "gpt-5.1",
        "openai_gpt-5-2": "gpt-5.2",
        "openai_gpt-5.2": "gpt-5.2",
        "openai/gpt-5-1": "gpt-5.1",
        "openai/gpt-5-2": "gpt-5.2",
        "xai_grok-4-fast-reasoning": "grok-4",
        "xai_grok-4-1-fast-reasoning": "grok-4.1",
    }
    return mapping.get(raw, raw)


def normalize_task_name(raw: str) -> str | None:
    name = TASK_ALIASES.get(raw, raw)
    if name in TASKS:
        return name
    return None


def parse_model_replicate(dirname: str) -> tuple[str, int] | None:
    m = re.match(r"^(.+)_replicate_(\d+)$", dirname)
    if m:
        return normalize_model_name(m.group(1)), int(m.group(2))
    m = re.match(r"^(.+)_r(\d+)$", dirname)
    if m:
        return normalize_model_name(m.group(1)), int(m.group(2))
    return None


def load_results_evals_layout(mr_dir: Path) -> list[dict]:
    evals_dir = mr_dir / "evals"
    if not evals_dir.is_dir():
        return []
    records = []
    for eval_dir in evals_dir.iterdir():
        if not eval_dir.is_dir():
            continue
        result_file = eval_dir / "_result.json"
        if not result_file.exists():
            continue
        with open(result_file) as f:
            r = json.load(f)
        records.append({
            "eval_id": eval_dir.name,
            "passed": r.get("passed", False),
            "duration_s": r.get("duration_s", 0) or 0,
            "total_cost": r.get("total_cost", 0) or 0,
        })
    return records


def load_results_converted_layout(mr_dir: Path) -> list[dict]:
    cr_dir = mr_dir / "converted_results"
    if not cr_dir.is_dir():
        return []
    records = []
    for fname in cr_dir.iterdir():
        if not fname.name.startswith("result_") or not fname.name.endswith(".json"):
            continue
        eval_id = fname.name.removeprefix("result_").removesuffix(".json")
        if eval_id.startswith("._"):
            continue
        with open(fname) as f:
            d = json.load(f)
        gr = d.get("grader_result") or {}
        passed = gr.get("passed", False)
        duration_ms = d.get("duration_ms", 0) or 0
        records.append({
            "eval_id": eval_id,
            "passed": passed,
            "duration_s": duration_ms / 1000.0,
            "total_cost": 0,
        })
    return records


def load_results_json_layout(mr_dir: Path) -> list[dict]:
    results_file = mr_dir / "results.json"
    if not results_file.exists():
        return []
    with open(results_file) as f:
        d = json.load(f)
    records = []
    for r in d.get("results", []):
        records.append({
            "eval_id": r.get("eval", ""),
            "passed": r.get("passed", False),
            "duration_s": r.get("duration_s", 0) or 0,
            "total_cost": r.get("total_cost", 0) or 0,
        })
    return records


def load_model_rep_results(mr_dir: Path) -> list[dict]:
    if (mr_dir / "evals").is_dir():
        return load_results_evals_layout(mr_dir)
    if (mr_dir / "converted_results").is_dir():
        return load_results_converted_layout(mr_dir)
    if (mr_dir / "results.json").exists():
        return load_results_json_layout(mr_dir)
    return []


def get_eval_ids_for_mr(mr_dir: Path) -> set[str]:
    if (mr_dir / "evals").is_dir():
        return {d.name for d in (mr_dir / "evals").iterdir() if d.is_dir()}
    if (mr_dir / "converted_results").is_dir():
        return {
            f.name.removeprefix("result_").removesuffix(".json")
            for f in (mr_dir / "converted_results").iterdir()
            if f.name.startswith("result_")
            and f.name.endswith(".json")
            and not f.name.startswith("result_._")
        }
    if (mr_dir / "results.json").exists():
        with open(mr_dir / "results.json") as f:
            d = json.load(f)
        return {r.get("eval", "") for r in d.get("results", [])} - {""}
    return set()


def resolve_platform_dir(platform: str, harness: str) -> Path | None:
    with_harness = RAW_RESULTS_DIR / platform / harness
    if with_harness.is_dir():
        return with_harness
    without_harness = RAW_RESULTS_DIR / platform
    if without_harness.is_dir():
        return without_harness
    return None


def build_canonical_task_map(harness: str = "minisweagent") -> dict[tuple[str, str], str]:
    canonical: dict[tuple[str, str], str] = {}

    for platform in PLATFORMS:
        platform_dir = resolve_platform_dir(platform, harness)
        if platform_dir is None:
            continue

        for task_dir in platform_dir.iterdir():
            if not task_dir.is_dir() or task_dir.name.startswith("."):
                continue
            task = normalize_task_name(task_dir.name)
            if task is None:
                continue

            min_evals: set[str] | None = None
            for mr_dir in task_dir.iterdir():
                if not mr_dir.is_dir() or mr_dir.name.startswith("."):
                    continue
                evals_here = get_eval_ids_for_mr(mr_dir)
                if evals_here:
                    if min_evals is None or len(evals_here) < len(min_evals):
                        min_evals = evals_here

            if min_evals:
                for eval_id in min_evals:
                    key = (platform, eval_id)
                    if key not in canonical:
                        canonical[key] = task

    return canonical


def collect_all_results(harness: str = "minisweagent") -> list[dict]:
    all_records = []

    for platform in PLATFORMS:
        platform_dir = resolve_platform_dir(platform, harness)
        if platform_dir is None:
            continue

        for task_dir in platform_dir.iterdir():
            if not task_dir.is_dir() or task_dir.name.startswith("."):
                continue
            task = normalize_task_name(task_dir.name)
            if task is None:
                continue

            for mr_dir in task_dir.iterdir():
                if not mr_dir.is_dir() or mr_dir.name.startswith("."):
                    continue
                parsed = parse_model_replicate(mr_dir.name)
                if parsed is None:
                    continue
                model, replicate = parsed

                records = load_model_rep_results(mr_dir)
                for rec in records:
                    if not rec["eval_id"]:
                        continue
                    all_records.append({
                        "platform": platform,
                        "task": task,
                        "model": model,
                        "replicate": replicate,
                        "eval_id": rec["eval_id"],
                        "passed": rec["passed"],
                        "duration_s": rec["duration_s"],
                        "total_cost": rec["total_cost"],
                    })

    return all_records


def deduplicate_cross_task(
    records: list[dict], canonical_map: dict[tuple[str, str], str]
) -> list[dict]:
    deduped = []
    for r in records:
        key = (r["platform"], r["eval_id"])
        assigned_task = canonical_map.get(key)
        if assigned_task is not None:
            if r["task"] == assigned_task:
                deduped.append(r)
        else:
            deduped.append(r)
    return deduped


def compute_ci(values: list[float], confidence: float = 0.95) -> dict:
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0}
    mean = float(np.mean(values))
    if n == 1:
        return {"mean": round(mean, 1), "ci_lower": round(mean, 1), "ci_upper": round(mean, 1)}
    se = float(np.std(values, ddof=1) / np.sqrt(n))
    t_crit = float(stats.t.ppf((1 + confidence) / 2, df=n - 1))
    return {
        "mean": round(mean, 1),
        "ci_lower": round(mean - t_crit * se, 1),
        "ci_upper": round(mean + t_crit * se, 1),
    }


def two_stage_aggregate(
    records: list[dict],
    group_keys: list[str],
) -> dict[tuple, dict]:
    grouped = defaultdict(lambda: defaultdict(list))
    for r in records:
        group = tuple(r[k] for k in group_keys)
        eval_key = (r["platform"], r["eval_id"])
        grouped[group][eval_key].append(1.0 if r["passed"] else 0.0)

    results = {}
    for group, eval_scores in grouped.items():
        eval_means = [float(np.mean(scores)) for scores in eval_scores.values()]
        pass_rate_values = [m * 100 for m in eval_means]
        results[group] = {
            "n_evals": len(eval_means),
            "accuracy": compute_ci(pass_rate_values),
        }
    return results


def compute_cost_latency(records: list[dict]) -> dict[str, dict]:
    model_costs = defaultdict(list)
    model_latencies = defaultdict(list)
    for r in records:
        if r["total_cost"] and r["total_cost"] > 0:
            model_costs[r["model"]].append(r["total_cost"])
        if r["duration_s"] and r["duration_s"] > 0:
            model_latencies[r["model"]].append(r["duration_s"])

    out = {}
    for model in set(list(model_costs.keys()) + list(model_latencies.keys())):
        out[model] = {}
        if model_costs[model]:
            out[model]["cost_usd"] = compute_ci(model_costs[model])
        if model_latencies[model]:
            out[model]["time_s"] = compute_ci(model_latencies[model])
    return out


def main():
    import sys
    harness = sys.argv[1] if len(sys.argv) > 1 else "minisweagent"

    print(f"Using harness: {harness}")
    print("Building canonical eval->task map...")
    canonical_map = build_canonical_task_map(harness)
    print(f"  Canonical map entries: {len(canonical_map)}")

    print("Collecting results...")
    records = collect_all_results(harness)
    print(f"  Raw records: {len(records)}")

    records = deduplicate_cross_task(records, canonical_map)
    print(f"  After dedup: {len(records)}")

    unique_evals = set((r["platform"], r["eval_id"]) for r in records)
    print(f"  Unique evals: {len(unique_evals)}")

    models = sorted(set(r["model"] for r in records))
    print(f"  Models: {models}")
    platforms = sorted(set(r["platform"] for r in records))
    print(f"  Platforms: {platforms}")
    tasks = sorted(
        set(r["task"] for r in records),
        key=lambda t: TASKS.index(t) if t in TASKS else 99,
    )
    print(f"  Tasks: {tasks}")

    print("\nEval counts per platform x task:")
    for platform in platforms:
        for task in tasks:
            n = len(set(
                r["eval_id"] for r in records
                if r["platform"] == platform and r["task"] == task
            ))
            if n > 0:
                print(f"  {platform}/{task}: {n}")

    print("\nComputing aggregate model performance...")
    model_agg = two_stage_aggregate(records, ["model"])

    print("\nComputing per-task performance...")
    task_agg = two_stage_aggregate(records, ["model", "task"])

    print("\nComputing per-platform performance...")
    platform_agg = two_stage_aggregate(records, ["model", "platform"])

    print("\nComputing cost/latency...")
    cost_latency = compute_cost_latency(records)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    benchmark_results = {
        "metadata": {
            "benchmark_version": "1.0",
            "n_evaluations": len(unique_evals),
            "n_runs_per_model": 3,
            "harness": harness,
            "date": "2026-02-03",
            "ci_method": "t-distribution based, 95% confidence, computed over per-evaluation means",
        },
        "models": [],
        "by_task": {},
        "by_platform": {},
    }

    for model in sorted(models, key=lambda m: -model_agg[(m,)]["accuracy"]["mean"]):
        entry = {
            "id": model,
            "display_name": MODEL_DISPLAY.get(model, model),
            "provider": MODEL_PROVIDER.get(model, "Unknown"),
            "harness": harness,
            "accuracy": model_agg[(model,)]["accuracy"],
            "n_evals": model_agg[(model,)]["n_evals"],
        }
        cl = cost_latency.get(model, {})
        if "cost_usd" in cl:
            entry["cost_usd"] = cl["cost_usd"]
        if "time_s" in cl:
            entry["time_s"] = cl["time_s"]
        benchmark_results["models"].append(entry)

    for task in tasks:
        task_evals = set(r["eval_id"] for r in records if r["task"] == task)
        task_results = []
        for model in sorted(
            models,
            key=lambda m: -task_agg.get((m, task), {}).get("accuracy", {}).get("mean", 0),
        ):
            key = (model, task)
            if key in task_agg:
                task_results.append({
                    "model": model,
                    "accuracy": task_agg[key]["accuracy"]["mean"],
                })
        benchmark_results["by_task"][task] = {
            "n_evals": len(task_evals),
            "results": task_results,
        }

    for platform in platforms:
        plat_evals = set(r["eval_id"] for r in records if r["platform"] == platform)
        plat_results = []
        for model in sorted(
            models,
            key=lambda m: -platform_agg.get((m, platform), {}).get("accuracy", {}).get("mean", 0),
        ):
            key = (model, platform)
            if key in platform_agg:
                plat_results.append({
                    "model": model,
                    "accuracy": platform_agg[key]["accuracy"]["mean"],
                })
        benchmark_results["by_platform"][platform] = {
            "n_evals": len(plat_evals),
            "results": plat_results,
        }

    suffix = f"_{harness}" if harness != "minisweagent" else ""
    with open(OUTPUT_DIR / f"benchmark_results{suffix}.json", "w") as f:
        json.dump(benchmark_results, f, indent=2)
        f.write("\n")
    print(f"\nWrote {OUTPUT_DIR / f'benchmark_results{suffix}.json'}")

    results_by_task = {
        "metadata": {
            "description": "Accuracy by task category with 95% confidence intervals",
            "n_runs": 3,
            "ci_method": "t-distribution, computed over per-evaluation means",
        },
        "tasks": {},
    }
    for task in tasks:
        task_evals = set(r["eval_id"] for r in records if r["task"] == task)
        task_models = {}
        for model in models:
            key = (model, task)
            if key in task_agg:
                task_models[model] = task_agg[key]["accuracy"]
        results_by_task["tasks"][task] = {
            "n_evals": len(task_evals),
            "models": task_models,
        }

    with open(OUTPUT_DIR / f"results_by_task{suffix}.json", "w") as f:
        json.dump(results_by_task, f, indent=2)
        f.write("\n")
    print(f"Wrote {OUTPUT_DIR / f'results_by_task{suffix}.json'}")

    results_by_platform = {
        "metadata": {
            "description": "Accuracy by platform with 95% confidence intervals",
            "n_runs": 3,
            "ci_method": "t-distribution, computed over per-evaluation means",
        },
        "platforms": {},
    }
    for platform in platforms:
        plat_evals = set(r["eval_id"] for r in records if r["platform"] == platform)
        plat_models = {}
        for model in models:
            key = (model, platform)
            if key in platform_agg:
                plat_models[model] = platform_agg[key]["accuracy"]
        results_by_platform["platforms"][platform] = {
            "n_evals": len(plat_evals),
            "models": plat_models,
        }

    with open(OUTPUT_DIR / f"results_by_platform{suffix}.json", "w") as f:
        json.dump(results_by_platform, f, indent=2)
        f.write("\n")
    print(f"Wrote {OUTPUT_DIR / f'results_by_platform{suffix}.json'}")

    print("\n=== SUMMARY TABLE ===")
    print(f"{'Model':<22} {'Accuracy':>10} {'95% CI':>16} {'Cost/Eval':>12} {'Latency':>10}")
    print("-" * 72)
    for entry in benchmark_results["models"]:
        acc = entry["accuracy"]
        cost = entry.get("cost_usd", {}).get("mean", "—")
        time = entry.get("time_s", {}).get("mean", "—")
        cost_str = f"${cost:.2f}" if isinstance(cost, float) else cost
        time_str = f"{time:.0f}s" if isinstance(time, float) else time
        print(
            f"{entry['display_name']:<22} {acc['mean']:>8.1f}%"
            f"  ({acc['ci_lower']:.1f}, {acc['ci_upper']:.1f})"
            f"  {cost_str:>10} {time_str:>10}"
        )

    print(f"\n=== BY TASK ===")
    header = f"{'Task':<28}"
    for m in sorted(models, key=lambda m: -model_agg[(m,)]["accuracy"]["mean"]):
        header += f" {MODEL_DISPLAY.get(m, m):>14}"
    print(header)
    print("-" * (28 + 15 * len(models)))
    for task in tasks:
        row = f"{task:<28}"
        for m in sorted(models, key=lambda m_: -model_agg[(m_,)]["accuracy"]["mean"]):
            key = (m, task)
            if key in task_agg:
                row += f" {task_agg[key]['accuracy']['mean']:>13.1f}%"
            else:
                row += f" {'—':>14}"
        print(row)

    print(f"\n=== BY PLATFORM ===")
    header = f"{'Platform':<16}"
    for m in sorted(models, key=lambda m: -model_agg[(m,)]["accuracy"]["mean"]):
        header += f" {MODEL_DISPLAY.get(m, m):>14}"
    print(header)
    print("-" * (16 + 15 * len(models)))
    for platform in platforms:
        row = f"{platform:<16}"
        for m in sorted(models, key=lambda m_: -model_agg[(m_,)]["accuracy"]["mean"]):
            key = (m, platform)
            if key in platform_agg:
                row += f" {platform_agg[key]['accuracy']['mean']:>13.1f}%"
            else:
                row += f" {'—':>14}"
        print(row)


if __name__ == "__main__":
    main()
