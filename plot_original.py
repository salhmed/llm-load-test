import json
import matplotlib.pyplot as plt

def plot_original_distribution(jsonl_file, output_image, limit=5000):
    lengths = []
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        # ignorer la première ligne (metadata)
        try:
            next(f)
        except StopIteration:
            pass
            
        count = 0
        for line in f:
            if count >= limit:
                break
            try:
                data = json.loads(line.strip())
                if "tok_input_length" in data:
                    lengths.append(int(data["tok_input_length"]))
                    count += 1
            except json.JSONDecodeError:
                pass
            
    if not lengths:
        print("Aucune donnée de longueur trouvée.")
        return

    plt.figure(figsize=(12, 6))
    
    # Use an automatic number of bins rather than forcing a bin every 50 tokens
    # which causes overlapping xticks if the max token count is huge.
    plt.hist(lengths, bins=50, color='coral', edgecolor='black', alpha=0.7)
    
    plt.title(f'Distribution de la longueur des prompts (OpenOrca Original - {limit} premiers)', fontsize=14)
    plt.xlabel('Nombre de tokens (tok_input_length)', fontsize=12)
    plt.ylabel('Nombre de requêtes', fontsize=12)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Let matplotlib automatically decide the best xticks for readability
    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    print(f"Le graphique a été généré et sauvegardé avec succès dans : {output_image}")

if __name__ == "__main__":
    input_file = "datasets/openorca_large_subset_011.jsonl"
    output_png = "datasets/distribution_openorca_5000.png"
    plot_original_distribution(input_file, output_png, 5000)
