# CLI Usage

## Installation

```bash
pip install -e .
```

## Commands

### Run Single Evaluation

```bash
scbench run path/to/eval.json --agent minisweagent --model anthropic/claude-opus-4-5
```

Options:
- `--agent`: Agent to use (`minisweagent`, `claudecode`)
- `--model`: Model name
- `--keep-workspace`: Keep workspace after completion
- `--verbose`: Verbose output

### Run Batch Evaluations

```bash
scbench batch evals_canonical/ --agent minisweagent --model anthropic/claude-opus-4-5 --output results/
```

Options:
- `--agent`: Agent to use
- `--model`: Model name
- `--output`: Output directory for results
- `--parallel`: Number of parallel workers
- `--keep-workspace`: Keep workspaces

### Validate Evaluation

```bash
scbench validate path/to/eval.json
```

### List Evaluations

```bash
scbench list
scbench list --category qc
```

### Generate Leaderboard

```bash
scbench leaderboard results/ --output leaderboard.json
```

## Environment Variables

- `ANTHROPIC_API_KEY`: Required for Claude models
- `OPENAI_API_KEY`: Required for OpenAI models
- `MSWEA_MODEL_NAME`: Default model for mini-swe-agent
