import json
import random

def generate_dataset(num_samples=250, filename="datasets/mixed_load_test.jsonl"):
    metadata = {"name": "load-test-mix", "version": "0.0.1"}
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(metadata) + '\n')
        
        for i in range(num_samples):
            is_rag = (i % 2 == 0)
            
            if is_rag:
                context = " ".join(["The company performance in Q3 was exceptional due to cost cutting measures and successful product launches."] * 100)
                question = f"Based on the following context, summarize the key points. Question {i}:\nContext: {context}"
                system_prompt = "You are a knowledgeable assistant. Use the provided context to answer the user's question accurately."
                tok_input_length = len(question) // 4 # rough estimate for RAG prompt
                tok_output_length = random.randint(50, 100)
            else:
                question = f"Explain the theory of relativity to a 5-year old. Variation {i}."
                system_prompt = "You are a helpful and friendly AI assistant."
                tok_input_length = len(question) // 4 # rough estimate for simple prompt
                tok_output_length = random.randint(150, 300)
            
            record = {
                "index": i,
                "question": question,
                "system_prompt": system_prompt,
                "tok_input_length": tok_input_length,
                "tok_output_length": tok_output_length
            }
            f.write(json.dumps(record) + '\n')

if __name__ == "__main__":
    generate_dataset()
    print("Dataset generated at datasets/mixed_load_test.jsonl")
