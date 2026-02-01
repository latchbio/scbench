#!/bin/bash

MODELS=(
    "anthropic/claude-opus-4-5"
    "anthropic/claude-sonnet-4-5"
    "openai/gpt-5.2"
    "openai/gpt-5.1"
    "google/gemini-2.5-pro"
)

EVALS_DIR="${1:-evals_canonical}"
OUTPUT_DIR="${2:-results/runs}"
PARALLEL="${3:-1}"

mkdir -p "$OUTPUT_DIR"

for model in "${MODELS[@]}"; do
    model_safe=$(echo "$model" | tr '/' '_')
    timestamp=$(date +%Y%m%d_%H%M%S)
    output_path="$OUTPUT_DIR/$model_safe/$timestamp"

    echo "Running benchmark for $model..."
    mkdir -p "$output_path"

    scbench batch "$EVALS_DIR" \
        --agent minisweagent \
        --model "$model" \
        --parallel "$PARALLEL" \
        --output "$output_path"

    echo "Results saved to $output_path"
    echo ""
done

echo "All benchmarks complete!"
