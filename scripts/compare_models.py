#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load_results(results_dir: Path) -> dict:
    results = {}
    for model_dir in results_dir.iterdir():
        if not model_dir.is_dir():
            continue
        model_name = model_dir.name
        results[model_name] = []
        for run_dir in model_dir.iterdir():
            if not run_dir.is_dir():
                continue
            batch_file = run_dir / "batch_results.json"
            if batch_file.exists():
                data = json.loads(batch_file.read_text())
                results[model_name].append(data)
    return results


def compute_stats(results: list) -> dict:
    if not results:
        return {}
    pass_rates = [r["metadata"]["pass_rate"] for r in results if "metadata" in r]
    if not pass_rates:
        return {}
    return {
        "n_runs": len(pass_rates),
        "mean_pass_rate": sum(pass_rates) / len(pass_rates),
        "min_pass_rate": min(pass_rates),
        "max_pass_rate": max(pass_rates),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: compare_models.py <results_dir>")
        sys.exit(1)

    results_dir = Path(sys.argv[1])
    if not results_dir.exists():
        print(f"Directory not found: {results_dir}")
        sys.exit(1)

    results = load_results(results_dir)

    print("Model Comparison")
    print("=" * 60)
    print(f"{'Model':<30} {'Runs':<6} {'Mean':<8} {'Min':<8} {'Max':<8}")
    print("-" * 60)

    for model_name, model_results in sorted(results.items()):
        stats = compute_stats(model_results)
        if stats:
            print(f"{model_name:<30} {stats['n_runs']:<6} "
                  f"{stats['mean_pass_rate']*100:.1f}%    "
                  f"{stats['min_pass_rate']*100:.1f}%    "
                  f"{stats['max_pass_rate']*100:.1f}%")


if __name__ == "__main__":
    main()
