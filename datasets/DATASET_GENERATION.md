# Load Test Dataset Generation

This repository includes a synthetic dataset generation script that simulates the usage of an LLM query system. This dataset is optimized to test the response behavior and system capabilities under a mixed workload of RAG (Retrieval-Augmented Generation) queries and straightforward conversational queries.

## Methodology

The dataset is generated via the cross-platform `generate_mix_dataset.py` Python script situated in the root directory.

We scan the existing `datasets/openorca_large_subset_011.jsonl` dataset to read the first 10,000 valid samples. From this large population, we randomly sample exactly 300 records to create our load test dataset.

*Mathematical Reality*: By sampling uniformly across a massive block of 10,000 entries, the resulting 300 instances perfectly retain and mimic the original dataset's token length curve without imposing artificial distribution tiers. This accurately simulates realistic organic LLM input variation.

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

You can recreate or recalculate the data split by running `generate_mix_dataset.py`. The script uses `random.sample()` across the first 10,000 items with a fixed `random.seed(42)` to ensure identical outputs on repeated generation.

Execute:
```sh
uv run generate_mix_dataset.py
```
