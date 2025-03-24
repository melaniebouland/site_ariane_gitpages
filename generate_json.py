import os
import json
from generate_html import generate_html_pages

# Dossier contenant les documents
TRAVAUX_DIR = "travaux"
OUTPUT_JSON = "documents.json"
OUTPUT_DIR = "html_pages"

def generate_json(directory, output_file):
    documents = []
    
    if not os.path.exists(directory):
        print(f"Le dossier {directory} n'existe pas.")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            documents.append({"name": filename, "path": filepath})

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(documents, json_file, indent=4, ensure_ascii=False)

    print(f"Fichier JSON mis à jour : {output_file}")
    generate_html_pages(output_file, OUTPUT_DIR)

if __name__ == "__main__":
    generate_json(TRAVAUX_DIR, OUTPUT_JSON)
