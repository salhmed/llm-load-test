# Load Test Dataset Generation

This repository includes a synthetic dataset generation script that simulates the usage of an LLM query system. This dataset is optimized to test the response behavior and system capabilities under a mixed workload of RAG (Retrieval-Augmented Generation) queries and straightforward conversational queries.

## Methodology

The dataset is generated via the custom `generate_mix_dataset.ps1` script situated in the root directory. This avoids dependency on external pre-compiled datasets.

We synthesize exactly 250 sample pairs consisting of two primary prompt groups:

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

You can recreate or recalculate the data split by adjusting the modulo arithmetic inside `generate_mix_dataset.ps1`. Currently, `$is_rag = ($i % 5 -eq 0)` assigns a 20% slice accurately corresponding to the 1-in-5 query distribution. Execute `.\generate_mix_dataset.ps1` from your powershell terminal to update records.
