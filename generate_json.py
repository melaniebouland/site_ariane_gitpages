import os
import json
from datetime import datetime
from generate_html import generate_html_pages

# Dossier contenant les documents
TRAVAUX_DIR = "public/travaux"
OUTPUT_JSON = "public/documents.json"
OUTPUT_DIR = "public/html_pages"

def parse_date(raw_date):
    # Essaye différents formats de date possibles
    for fmt in ("%Y-%m-%d", "%Y.%m", "%Y_%m", "%Y"):
        try:
            parsed = datetime.strptime(raw_date, fmt)
            # Toujours retourner au format YYYY-MM-DD
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Si aucun format ne marche
    return "0001-01-01"  # Valeur par défaut si format inconnu

def extract_info_from_filename(filename):
    name, _ = os.path.splitext(filename)
    parts = name.split("_", 3)  # GT, date, titre (avec underscores possibles)

    if len(parts) < 3:
        return {
            "gt": "inconnu",
            "date": "0001-01-01",
            "title": name
        }

    gt = parts[0]
    raw_date = parts[1]
    title = "_".join(parts[2:])  # Recolle le reste s’il y a des underscores dans le titre
    date = parse_date(raw_date)

    return {
        "gt": gt,
        "date": date,
        "title": title
    }

def generate_json(directory, output_file):
    documents = []

    if not os.path.exists(directory):
        print(f"Le dossier {directory} n'existe pas.")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            info = extract_info_from_filename(filename)
            documents.append({
                "name": filename,
                "path": filepath,
                "gt": info["gt"],
                "date": info["date"],
                "title": info["title"]
            })

    # Tri alphabétique des documents par nom
    documents.sort(key=lambda doc: doc["name"].lower())

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(documents, json_file, indent=4, ensure_ascii=False)

    print(f"Fichier JSON mis à jour : {output_file}")
    generate_html_pages(output_file, OUTPUT_DIR)

if __name__ == "__main__":
    generate_json(TRAVAUX_DIR, OUTPUT_JSON)
