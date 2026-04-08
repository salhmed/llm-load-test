# Load Test Dataset Generation

This repository includes a synthetic dataset generation script that simulates the usage of an LLM query system. This dataset is optimized to test the response behavior and system capabilities under a mixed workload of RAG (Retrieval-Augmented Generation) queries and straightforward conversational queries.

## Methodology

The dataset is generated via the cross-platform `generate_mix_dataset.py` Python script situated in the root directory.

We scan the existing `datasets/openorca_large_subset_011.jsonl` dataset and parse the real LLM queries inside to build exactly 250 sample pairs in these categories:

1. **Short prompts / Simple conversations (80%)**: Simulates quick, standalone conversational instructions (e.g. asking to explain a basic concept).
2. **Long prompts / RAG simulations (20%)**: Emulates context-heavy queries by appending repetitive blocks of texts that significantly bulk up the input length.

For both prompt types, random output token counts and accurately estimated input lengths ensure realism when metrics (like Input Tokens and Output Tokens) are calculated.

### Dataset Output Format

The dataset exports to `datasets/mixed_load_test.jsonl` matching the required format for `llm-load-test`. 
The first line yields the config metadata:
```json
{"name":"load-test-mix","version":"0.0.1"}
```

Remaining lines are serialized as follows:
```json
{
  "index": 1,
  "question": "Explain the theory of relativity to a 5-year old. Variation 1.",
  "system_prompt": "You are a helpful and friendly AI assistant.",
  "tok_input_length": 15,
  "tok_output_length": 182
}
```

### Reproducibility

You can recreate or recalculate the data split by adjusting the loops logic inside `generate_mix_dataset.py`. Currently, it locks until it has found exactly 50 long prompts and 200 short ones yielding your 20/80 target metric.

Execute:
```sh
uv run generate_mix_dataset.py
```
