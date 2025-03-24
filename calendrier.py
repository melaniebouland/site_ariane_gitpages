import requests
from ics import Calendar
import json


# URL du flux iCal public (remplace par l'URL exacte de ton calendrier)
ICAL_URL = "https://calendar.google.com/calendar/ical/consortium.ariane%40gmail.com/public/basic.ics"

# Télécharger le fichier iCal
response = requests.get(ICAL_URL)
if response.status_code == 200:
    cal = Calendar(response.text)

    # Dictionnaire pour stocker les événements selon leur préfixe
    events_by_category = {}

    # Parcourir les événements du calendrier
    for event in cal.events:
        title = event.name  # Nom de l'événement
        start = event.begin  # Date et heure de début

        # Déterminer la catégorie en fonction du nom (exemple : préfixes "Réunion", "Atelier", etc.)
        category = title.split(" ")[0]  # Premier mot du titre comme catégorie

        # Ajouter l'événement à la bonne catégorie
        if category not in events_by_category:
            events_by_category[category] = []
        events_by_category[category].append({"title": title, "start": start.isoformat()})

    with open("calendrier.json", "w", encoding="utf-8") as json_file:
        json.dump(events_by_category, json_file, ensure_ascii= False, indent=4)
    
    print("Les événements ont été enregistrés dans le fichier calendrier.json.")
else:
    print("❌ Impossible de récupérer le calendrier")

