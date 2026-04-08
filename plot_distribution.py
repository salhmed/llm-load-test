import json
import matplotlib.pyplot as plt

def plot_distribution(jsonl_file, output_image):
    lengths = []
    
    # Lecture des tailles d'entrée depuis le fichier jsonl
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        # ignorer la première ligne (metadata)
        next(f)
        for line in f:
            try:
                data = json.loads(line.strip())
                if "tok_input_length" in data:
                    lengths.append(int(data["tok_input_length"]))
            except json.JSONDecodeError:
                pass
            
    if not lengths:
        print("Aucune donnée de longueur trouvée.")
        return

    # Configuration du graphique
    plt.figure(figsize=(10, 6))
    
    # bins à intervalles de 50 tokens
    bins = range(0, max(lengths) + 50, 50)
    
    plt.hist(lengths, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
    
    # Ajout de titres et labels
    plt.title('Distribution de la longueur des prompts en entrée (Tokens)', fontsize=14)
    plt.xlabel('Nombre de tokens (Input)', fontsize=12)
    plt.ylabel('Nombre de requêtes (Prompts)', fontsize=12)
    
    # Ajout de repères
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(bins, rotation=45)
    
    # Sauvegarde du graphique
    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    print(f"Le graphique a été généré et sauvegardé avec succès dans : {output_image}")

if __name__ == "__main__":
    input_file = "datasets/mixed_load_test.jsonl"
    output_png = "datasets/distribution.png"
    plot_distribution(input_file, output_png)
