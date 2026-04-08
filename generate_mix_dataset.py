import json
import os

def extract_dataset(in_file, out_file):
    metadata = {"name": "load-test-mix-extracted", "version": "0.0.1"}
    
    long_count = 0
    short_count = 0
    
    # Ensure outputs array handles relative paths
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    with open(out_file, 'w', encoding='utf-8') as out_f:
        out_f.write(json.dumps(metadata) + '\n')
        
        try:
            with open(in_file, 'r', encoding='utf-8') as in_f:
                # pass metadata line
                next(in_f)
                
                for line in in_f:
                    if long_count >= 50 and short_count >= 200:
                        break
                        
                    try:
                        record = json.loads(line.strip())
                        input_tokens = int(record.get('tok_input_length', 0))
                        
                        if input_tokens >= 400 and long_count < 50:
                            record['index'] = long_count + short_count
                            out_f.write(json.dumps(record) + '\n')
                            long_count += 1
                        elif input_tokens <= 150 and short_count < 200:
                            record['index'] = long_count + short_count
                            out_f.write(json.dumps(record) + '\n')
                            short_count += 1
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print(f"File {in_file} not found. Please ensure you have the OpenOrca jsonl file locally.")
            return
            
    print(f"Successfully extracted from OpenOrca: {long_count} long RAG prompts and {short_count} short prompts.")

if __name__ == "__main__":
    # OS independent relative paths
    in_file = os.path.join(".", "datasets", "openorca_large_subset_011.jsonl")
    out_file = os.path.join(".", "datasets", "mixed_load_test.jsonl")
    extract_dataset(in_file, out_file)
