import os
import requests
from ics import Calendar
import json
import re

# URL du flux iCal public
ICAL_URL = "https://calendar.google.com/calendar/ical/consortium.ariane%40gmail.com/public/basic.ics"

# Télécharger le fichier iCal
response = requests.get(ICAL_URL)
if response.status_code == 200:
    cal = Calendar(response.text)

    # Vérification que le calendrier contient bien des événements
    if not cal.events:
        print("⚠️ Aucun événement trouvé dans le calendrier.")
    
    # Dictionnaire pour stocker les événements par Axe et GT
    events_by_axe = {}

    # Parcourir les événements du calendrier
    for event in cal.events:
        title = event.name.strip() if event.name else "Événement sans titre"
        start = event.begin  # Date et heure de début
        formatted_start = start.strftime("%H:%M")  # Formatage de l'heure
        description = event.description.strip() if event.description else "Pas de description disponible"

        # Extraire l'Axe et le GT
        axe_match = re.search(r'AXE\s*(\d+)', title, re.IGNORECASE)
        gt_match = re.search(r'GT\s*(\d+)', title, re.IGNORECASE)
        
        if axe_match:
            axe = f"Axe {axe_match.group(1)}"
            gt = f"GT {gt_match.group(1)}" if gt_match else "Autres GT"
            
            if axe not in events_by_axe:
                events_by_axe[axe] = {}
            if gt not in events_by_axe[axe]:
                events_by_axe[axe][gt] = []

            events_by_axe[axe][gt].append({
                "title": title,
                "start": formatted_start,
                "description": description
            })

    # Enregistrer les événements dans un fichier JSON
    with open("calendrier.json", "w", encoding="utf-8") as json_file:
        json.dump(events_by_axe, json_file, ensure_ascii=False, indent=4)

    print("Les événements ont été enregistrés dans le fichier calendrier.json.")

    # Créer un dossier pour les pages HTML
    os.makedirs("calendrier_pages", exist_ok=True)

    # Générer une page HTML pour chaque Axe
    for axe, gts in events_by_axe.items():
        safe_axe = re.sub(r'[^a-zA-Z0-9]+', '_', axe)
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Calendrier - {axe}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body class="container">
        <h1 class="mt-4">{axe}</h1>
        """
        
        for gt, events in sorted(gts.items()):  # Trier par GT
            html_content += f"<h2 class='mt-3'>{gt}</h2>"
            for index, event in enumerate(events):
                html_content += f"""
                <div class="card mb-3">
                    <div class="card-body">
                        <h3 class="card-title">{event['title']}</h3>
                        <p class="card-text"><strong>Horaire :</strong> {event['start']}</p>
                        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#desc{safe_axe}_{index}" aria-expanded="false">
                            Description
                        </button>
                        <div class="collapse mt-2" id="desc{safe_axe}_{index}">
                            <div class="card card-body">
                                {event['description']}
                            </div>
                        </div>
                    </div>
                </div>
                """
        
        html_content += """
        </body></html>"""
        
        with open(f"calendrier_pages/{safe_axe}.html", "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    print("Les pages HTML ont été générées dans le dossier calendrier_pages.")
else:
    print("❌ Impossible de récupérer le calendrier")