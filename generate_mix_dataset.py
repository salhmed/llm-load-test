import json
import os
import random

def extract_dataset(in_file, out_file):
    metadata = {"name": "load-test-mix-extracted-true-distribution", "version": "0.0.1"}
    
    # 1. Read first 10,000 valid samples
    population = []
    
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    try:
        with open(in_file, 'r', encoding='utf-8') as in_f:
            # pass metadata line
            next(in_f)
            
            for line in in_f:
                if len(population) >= 10000:
                    break
                    
                try:
                    record = json.loads(line.strip())
                    # Ensure it has token lengths properties before adding
                    if 'tok_input_length' in record:
                        population.append(record)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"File {in_file} not found.")
        return

    # Error handling if less than 300 prompts were found
    sample_size = min(300, len(population))
    
    # 2. Extract exactly 300 random samples uniformally to maintain natural distribution
    random.seed(42) # set a seed for reproducibility
    sampled_prompts = random.sample(population, sample_size)
    
    # Optional sort by size if needed by load-test tool, but original was ordered by length
    # sampled_prompts.sort(key=lambda x: int(x['tok_input_length']))

    # 3. Write out to the final mixed load test jsonl
    with open(out_file, 'w', encoding='utf-8') as out_f:
        out_f.write(json.dumps(metadata) + '\n')
        
        for i, record in enumerate(sampled_prompts):
            record['index'] = i
            out_f.write(json.dumps(record) + '\n')
            
    print(f"Successfully drew {sample_size} prompts from {len(population)} elements respecting exact original distribution.")

if __name__ == "__main__":
    in_file = os.path.join(".", "datasets", "openorca_large_subset_011.jsonl")
    out_file = os.path.join(".", "datasets", "mixed_load_test.jsonl")
    extract_dataset(in_file, out_file)
