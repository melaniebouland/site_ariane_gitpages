import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
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

class TravauxHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type in ["created", "deleted", "modified", "moved"]:
            print("Changement détecté, mise à jour en cours...")
            generate_json(TRAVAUX_DIR, OUTPUT_JSON)

if __name__ == "__main__":
    event_handler = TravauxHandler()
    observer = Observer()
    observer.schedule(event_handler, TRAVAUX_DIR, recursive=True)
    observer.start()
    
    try:
        print("Surveillance en cours... (Ctrl+C pour arrêter)")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        print("Arrêt de la surveillance.")
    observer.join()
