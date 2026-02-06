# Raw Data for SCBench Tables

All data from SCBench v1.0 (February 2026). 95% confidence intervals computed via t-distribution over per-evaluation means across 3 runs.

## Overall Model Performance

| Model ID | Display Name | Provider | Harness | Accuracy (%) | CI Lower | CI Upper | Time (s) | Cost ($) |
|----------|--------------|----------|---------|--------------|----------|----------|----------|----------|
| claude-opus-4-6 | Claude Opus 4.6 | Anthropic | mini-swe-agent | 52.8 | 48.3 | 57.2 | 303.0 | 0.6 |
| claude-opus-4-5 | Claude Opus 4.5 | Anthropic | mini-swe-agent | 49.9 | 45.3 | 54.4 | 154.3 | 0.2 |
| gpt-5.2 | GPT-5.2 | OpenAI | mini-swe-agent | 45.2 | 40.9 | 49.5 | 132.8 | 0.1 |
| claude-sonnet-4-5 | Claude Sonnet 4.5 | Anthropic | mini-swe-agent | 44.2 | 39.9 | 48.6 | 193.3 | 0.1 |
| gpt-5.1 | GPT-5.1 | OpenAI | mini-swe-agent | 37.9 | 33.7 | 42.0 | 94.3 | 0.0 |
| grok-4.1 | Grok-4.1 | xAI | mini-swe-agent | 35.6 | 31.6 | 39.7 | 179.6 | 0.1 |
| grok-4 | Grok-4 | xAI | mini-swe-agent | 33.9 | 30.1 | 37.8 | 202.7 | 0.1 |
| gemini-2.5-pro | Gemini 2.5 Pro | Google | mini-swe-agent | 29.2 | 25.6 | 32.9 | 300.4 | 0.3 |

## Accuracy by Task Category (Summary)

| Model | QC (n=36) | Norm (n=37) | Dim Red (n=69) | Clustering (n=49) | Cell Typing (n=118) | Diff Expr (n=79) | Traj (n=7) |
|-------|-----------|------------|----------------|-------------------|--------------------|--------------------|------------|
| claude-opus-4-6 | 61.1 | 82.4 | 55.4 | 52.7 | 48.2 | 41.4 | 42.9 |
| claude-opus-4-5 | 63.9 | 83.8 | 54.8 | 42.6 | 45.8 | 33.3 | 61.9 |
| gpt-5.2 | 63.0 | 74.8 | 50.0 | 42.6 | 39.5 | 29.9 | 42.9 |
| claude-sonnet-4-5 | 61.1 | 82.9 | 50.7 | 39.0 | 35.6 | 27.4 | 57.1 |
| gpt-5.1 | 60.2 | 62.2 | 47.3 | 33.3 | 29.1 | 25.2 | 38.1 |
| grok-4.1 | 49.1 | 65.8 | 41.1 | 31.2 | 30.2 | 20.1 | 57.1 |
| grok-4 | 40.7 | 51.4 | 38.7 | 34.8 | 29.1 | 25.2 | 42.9 |
| gemini-2.5-pro | 47.2 | 59.5 | 35.1 | 29.8 | 22.0 | 13.7 | 21.4 |

## Task Category CIs (Full Data)

### QC (n=36)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-5 | 63.9 | 48.1 | 79.7 |
| gpt-5.2 | 63.0 | 47.5 | 78.4 |
| claude-opus-4-6 | 61.1 | 45.3 | 76.9 |
| claude-sonnet-4-5 | 61.1 | 45.7 | 76.5 |
| gpt-5.1 | 60.2 | 44.7 | 75.6 |
| grok-4.1 | 49.1 | 34.2 | 64.0 |
| gemini-2.5-pro | 47.2 | 34.2 | 60.3 |
| grok-4 | 40.7 | 27.5 | 54.0 |

### Normalization (n=37)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-5 | 83.8 | 73.1 | 94.5 |
| claude-sonnet-4-5 | 82.9 | 71.6 | 94.2 |
| claude-opus-4-6 | 82.4 | 71.8 | 93.0 |
| gpt-5.2 | 74.8 | 62.1 | 87.4 |
| grok-4.1 | 65.8 | 52.3 | 79.2 |
| gpt-5.1 | 62.2 | 48.3 | 76.1 |
| gemini-2.5-pro | 59.5 | 45.3 | 73.6 |
| grok-4 | 51.4 | 39.5 | 63.2 |

### Dimensionality Reduction (n=69)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 55.4 | 43.7 | 67.1 |
| claude-opus-4-5 | 54.8 | 42.8 | 66.7 |
| claude-sonnet-4-5 | 50.7 | 39.8 | 61.7 |
| gpt-5.2 | 50.0 | 38.7 | 61.3 |
| gpt-5.1 | 47.3 | 35.4 | 59.2 |
| grok-4.1 | 41.1 | 30.0 | 52.1 |
| grok-4 | 38.7 | 27.3 | 50.1 |
| gemini-2.5-pro | 35.1 | 24.8 | 45.4 |

### Clustering (n=49)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 52.7 | 40.6 | 64.9 |
| claude-opus-4-5 | 42.6 | 29.5 | 55.6 |
| gpt-5.2 | 42.6 | 30.0 | 55.1 |
| claude-sonnet-4-5 | 39.0 | 26.9 | 51.1 |
| grok-4 | 34.8 | 24.6 | 44.9 |
| gpt-5.1 | 33.3 | 21.3 | 45.4 |
| grok-4.1 | 31.2 | 20.5 | 41.9 |
| gemini-2.5-pro | 29.8 | 20.4 | 39.2 |

### Cell Typing (n=118)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 48.2 | 40.1 | 56.2 |
| claude-opus-4-5 | 45.8 | 37.6 | 53.9 |
| gpt-5.2 | 39.5 | 32.3 | 46.8 |
| claude-sonnet-4-5 | 35.6 | 28.2 | 43.0 |
| grok-4.1 | 30.2 | 23.6 | 36.8 |
| gpt-5.1 | 29.1 | 22.8 | 35.4 |
| grok-4 | 29.1 | 22.6 | 35.6 |
| gemini-2.5-pro | 22.0 | 16.3 | 27.8 |

### Differential Expression (n=79)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 41.4 | 31.7 | 51.0 |
| claude-opus-4-5 | 33.3 | 23.8 | 42.9 |
| gpt-5.2 | 29.9 | 21.0 | 38.8 |
| claude-sonnet-4-5 | 27.4 | 18.5 | 36.2 |
| gpt-5.1 | 25.2 | 17.1 | 33.4 |
| grok-4 | 25.2 | 17.0 | 33.4 |
| grok-4.1 | 20.1 | 12.3 | 27.9 |
| gemini-2.5-pro | 13.7 | 7.9 | 19.4 |

### Trajectory Analysis (n=7)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-5 | 61.9 | 20.4 | 103.4 |
| claude-sonnet-4-5 | 57.1 | 27.8 | 86.5 |
| grok-4.1 | 57.1 | 22.8 | 91.4 |
| claude-opus-4-6 | 42.9 | 4.2 | 81.5 |
| gpt-5.2 | 42.9 | 0.3 | 85.4 |
| grok-4 | 42.9 | 10.9 | 74.8 |
| gpt-5.1 | 38.1 | -3.4 | 79.6 |
| gemini-2.5-pro | 21.4 | -15.0 | 57.8 |

## Accuracy by Platform (Summary)

| Model | BD Rhapsody (n=61) | Chromium (n=60) | CS Genetics (n=42) | Illumina (n=85) | Mission Bio (n=81) | Parse Bio (n=65) |
|-------|-------------------|-----------------|--------------------|-----------------|--------------------|------------------|
| claude-opus-4-6 | 53.0 | 51.7 | 74.6 | 52.5 | 42.0 | 53.2 |
| claude-opus-4-5 | 55.7 | 47.1 | 77.0 | 50.6 | 37.9 | 41.7 |
| gpt-5.2 | 54.6 | 46.6 | 65.1 | 54.5 | 23.0 | 35.9 |
| claude-sonnet-4-5 | 53.6 | 46.0 | 70.6 | 41.2 | 34.2 | 33.3 |
| gpt-5.1 | 41.5 | 46.0 | 46.8 | 50.0 | 20.2 | 25.0 |
| grok-4.1 | 42.6 | 42.5 | 46.0 | 43.1 | 18.9 | 25.0 |
| grok-4 | 30.1 | 40.8 | 40.5 | 38.8 | 24.7 | 32.1 |
| gemini-2.5-pro | 30.6 | 33.0 | 52.4 | 34.1 | 10.3 | 26.3 |

## Platform CIs (Full Data)

### BD Rhapsody (n=61)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-5 | 55.7 | 44.7 | 66.7 |
| gpt-5.2 | 54.6 | 43.5 | 65.8 |
| claude-sonnet-4-5 | 53.6 | 42.1 | 65.0 |
| claude-opus-4-6 | 53.0 | 41.8 | 64.2 |
| grok-4.1 | 42.6 | 31.8 | 53.4 |
| gpt-5.1 | 41.5 | 30.9 | 52.2 |
| gemini-2.5-pro | 30.6 | 21.2 | 40.0 |
| grok-4 | 30.1 | 21.3 | 38.8 |

### Chromium (n=60)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 51.7 | 40.4 | 62.9 |
| claude-opus-4-5 | 47.1 | 35.5 | 58.7 |
| gpt-5.2 | 46.6 | 35.2 | 57.9 |
| claude-sonnet-4-5 | 46.0 | 35.4 | 56.6 |
| gpt-5.1 | 46.0 | 34.3 | 57.7 |
| grok-4.1 | 42.5 | 32.0 | 53.0 |
| grok-4 | 40.8 | 30.5 | 51.1 |
| gemini-2.5-pro | 33.0 | 22.8 | 43.2 |

### CS Genetics (n=42)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-5 | 77.0 | 65.9 | 88.1 |
| claude-opus-4-6 | 74.6 | 62.5 | 86.7 |
| claude-sonnet-4-5 | 70.6 | 57.8 | 83.5 |
| gpt-5.2 | 65.1 | 53.2 | 77.0 |
| gemini-2.5-pro | 52.4 | 40.2 | 64.6 |
| gpt-5.1 | 46.8 | 33.6 | 60.0 |
| grok-4.1 | 46.0 | 33.5 | 58.6 |
| grok-4 | 40.5 | 27.6 | 53.4 |

### Illumina (n=85)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| gpt-5.2 | 54.5 | 45.9 | 63.1 |
| claude-opus-4-6 | 52.5 | 42.8 | 62.3 |
| claude-opus-4-5 | 50.6 | 40.4 | 60.7 |
| gpt-5.1 | 50.0 | 41.6 | 58.4 |
| grok-4.1 | 43.1 | 34.1 | 52.2 |
| claude-sonnet-4-5 | 41.2 | 31.9 | 50.4 |
| grok-4 | 38.8 | 31.0 | 46.7 |
| gemini-2.5-pro | 34.1 | 26.8 | 41.4 |

### Mission Bio (n=81)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 42.0 | 32.4 | 51.6 |
| claude-opus-4-5 | 37.9 | 28.3 | 47.4 |
| claude-sonnet-4-5 | 34.2 | 25.0 | 43.3 |
| grok-4 | 24.7 | 17.7 | 31.7 |
| gpt-5.2 | 23.0 | 15.2 | 30.9 |
| gpt-5.1 | 20.2 | 13.0 | 27.3 |
| grok-4.1 | 18.9 | 13.0 | 24.9 |
| gemini-2.5-pro | 10.3 | 5.5 | 15.0 |

### Parse Bio (n=65)

| Model | Mean | CI Lower | CI Upper |
|-------|------|----------|----------|
| claude-opus-4-6 | 53.2 | 41.3 | 65.1 |
| claude-opus-4-5 | 41.7 | 28.2 | 55.2 |
| gpt-5.2 | 35.9 | 23.3 | 48.5 |
| claude-sonnet-4-5 | 33.3 | 22.3 | 44.4 |
| grok-4 | 32.1 | 19.6 | 44.5 |
| gemini-2.5-pro | 26.3 | 15.5 | 37.1 |
| gpt-5.1 | 25.0 | 13.5 | 36.5 |
| grok-4.1 | 25.0 | 13.4 | 36.6 |

## Evaluation Counts

### By Platform

| Platform | Evaluations |
|----------|-------------|
| Illumina | 85 |
| Mission Bio | 81 |
| Parse Bio | 65 |
| BD Rhapsody | 61 |
| Chromium | 60 |
| CS Genetics | 42 |
| **Total** | **394** |

### By Task Category

| Task Category | Evaluations |
|---------------|-------------|
| Cell Typing | 118 |
| Differential Expression | 79 |
| Dimensionality Reduction | 69 |
| Clustering | 49 |
| Normalization | 37 |
| QC | 36 |
| Trajectory Analysis | 7 |
| **Total** | **395** |

Note: Task total (395) exceeds platform total (394) by 1 due to an evaluation counted in multiple task categories.
