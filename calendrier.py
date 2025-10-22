import os
import requests
from ics import Calendar
import json
import re
from datetime import datetime, timezone

# URL du flux iCal public
ICAL_URL = "https://calendar.google.com/calendar/ical/consortium.ariane%40gmail.com/public/basic.ics"

# Télécharger le fichier iCal
response = requests.get(ICAL_URL)
if response.status_code == 200:
    cal = Calendar(response.text)

    # Vérification que le calendrier contient bien des événements
    if not cal.events:
        print("⚠️ Aucun événement trouvé dans le calendrier.")
    
    # Dictionnaire pour stocker les événements par catégorie (Axe, AMIS) et GT
    events_by_category = {}
    # Obtenir la date actuelle (naive, sans fuseau horaire)
    today = datetime.now()

    # Parcourir les événements du calendrier
    for event in cal.events:
        title = event.name.strip() if event.name else "Événement sans titre"
        start = event.begin  # Date et heure de début
        formatted_start = start.strftime("%H:%M")  # Heure
        formatted_date = start.strftime("%d/%m/%Y")  # Date
        year = start.year
        description = event.description.strip() if event.description else "Pas de description disponible"
        location = event.location.strip() if event.location else "Lieu non spécifié"

        # Extraire l'Axe, GT ou AMIS
        axe_match = re.search(r'AXE\s*(\d+)', title, re.IGNORECASE)
        gt_match = re.search(r'GT\s*(\d+)', title, re.IGNORECASE)
        amis_match = re.search(r'AMIS', title, re.IGNORECASE)
        
        category = None
        subcategory = None
        
        if axe_match:
            category = f"Axe {axe_match.group(1)}"
            subcategory = f"GT {gt_match.group(1)}" if gt_match else "Autres GT"
        elif amis_match:
            category = "AMIS"
            subcategory = "Actualités AMIS"

        if category:
            # Convertir la date en naive (sans fuseau horaire) pour la comparaison
            event_datetime = start.datetime
            if hasattr(event_datetime, 'tzinfo') and event_datetime.tzinfo is not None:
                # Si la date a un fuseau horaire, on la convertit en naive
                event_datetime = event_datetime.replace(tzinfo=None)
            
            events_by_category.setdefault(category, {}).setdefault(subcategory, {}).setdefault(year, []).append({
                "title": title,
                "start": formatted_start,
                "date": formatted_date,
                "datetime": event_datetime,  # Garder l'objet datetime pour le tri
                "description": description,
                "Localisation": location
            })

    # Trier les événements par date (les plus récents/à venir en premier)
    for category in events_by_category:
        for subcategory in events_by_category[category]:
            for year in events_by_category[category][subcategory]:
                events_by_category[category][subcategory][year].sort(
                    key=lambda x: x['datetime'],
                    reverse=True
                )

    # Enregistrer les événements dans un fichier JSON (sans le datetime pour sérialisation)
    events_for_json = {}
    for category, subcats in events_by_category.items():
        events_for_json[category] = {}
        for subcat, years in subcats.items():
            events_for_json[category][subcat] = {}
            for year, events in years.items():
                events_for_json[category][subcat][year] = [
                    {k: v for k, v in event.items() if k != 'datetime'}
                    for event in events
                ]

    with open("public/calendrier.json", "w", encoding="utf-8") as json_file:
        json.dump(events_for_json, json_file, ensure_ascii=False, indent=4)

    print("Les événements ont été enregistrés dans le fichier calendrier.json.")

    # Créer un dossier pour les pages HTML
    output_dir = "public/calendrier_pages"
    os.makedirs(output_dir, exist_ok=True)

    # Générer une page HTML pour chaque catégorie (Axe ou AMIS)
    for category, subcats in events_by_category.items():
        safe_category = re.sub(r'[^a-zA-Z0-9]+', '_', category)
        
        html_content = f"""<!doctype html>
<html lang="fr-fr">
<head>
    <base href=".">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" sizes="180x180" href="assets/img/logoAriane.jpg">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <link rel="stylesheet" href="../assets/main.css">
    <title>Calendrier - {category}</title>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        .dropdown:hover>.dropdown-menu {{
            display: block;
        }}
        .dropdown-submenu {{
            position: relative;
        }}
        .dropdown-submenu:hover>.dropdown-menu {{
            display: block;
        }}
        .dropdown-submenu .dropdown-menu {{
            top: 0;
            left: 100%;
            margin-top: -1px;
        }}
        .event-upcoming {{
            border-left: 4px solid rgb(143 0 6);
        }}
        .event-past {{
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <!-- Header consortium -->
    <header class="relative bg-white mb-2 w-100" style="box-shadow: 0 0 10px rgba(143, 0, 6, 0.1);">
        <div class="border-top border-danger"></div>
        <div class="header-content container">
            <div class="header-logos d-flex align-items-center">
                <!--Logo Ariane-->
                <a href="https://cst-ariane.huma-num.fr/" class="me-2">
                    <img src="assets/img/logoAriane.jpg" alt="CST-HN ARIANE logo">
                </a>
                <!--Logo Humanum-->
                <a href="https://www.huma-num.fr/">
                    <img src="assets/img/HN.png" alt="Huma-Num logo">
                </a>
            </div>
            <!--Menu-->
            <nav>
                <ul class="nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75 dropdown-toggle" href="#" id="axesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                          Axes
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="axesDropdown">
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle" href="https://consortiumariane.gitpages.huma-num.fr/axe1">Axe 1</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT1/GT1.html">GT1 - Labellisation</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT2/GT2.html">GT2 - Acquisition de données et transcription par ordinateur</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT3/GT3.html">GT3 - Outils et pratiques éditoriales</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle" href="https://consortiumariane.gitpages.huma-num.fr/axe2">Axe 2</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT4/GT4.html">GT4 - Analyse automatique de texte</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT5/GT5.html">GT5 - Métadonnées et modélisation de données</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT6/GT6.html">GT6 - Open French Corpus</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle" href="https://consortiumariane.gitpages.huma-num.fr/axe3">Axe 3</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe3/ethique/ethique.html">Enjeux éthiques</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe3/juridique/juridique.html">Questions juridiques</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75 dropdown-toggle" href="#" id="axesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                          Travaux
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="axesDropdown">
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle">Axe 1</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT1.html">GT1 - Labellisation</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT2.html">GT2 - Acquisition de données et transcription par ordinateur</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT3.html">GT3 - Outils et pratiques éditoriales</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle">Axe 2</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT4.html">GT4 - Analyse automatique de texte</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT5.html">GT5 - Métadonnées et modélisation de données</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_GT6.html">GT6 - Open French Corpus</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle">Axe 3</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_ethique.html">Enjeux éthiques</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/html_pages/travaux_juridique.html">Questions juridiques</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://consortiumariane.gitpages.huma-num.fr/outils/index.html">Outils</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75 dropdown-toggle" href="#" id="axesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                          Actualités
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="axesDropdown">
                            <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/calendrier_pages/Axe_1.html">Axe 1</a></li>
                            <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/calendrier_pages/Axe_2.html">Axe 2</a></li>
                            <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/calendrier_pages/Axe_3.html">Axe 3</a></li>
                            <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/calendrier_pages/AMIS.html">AMIS</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://docs.google.com/forms/d/1nxWiaj88LY7R-poxxlTiUxdvyIH5hL5eBHFjgsfsKGg/viewform?edit_requested=true">Nous rejoindre</a>
                    </li>
                </ul>
            </nav>
        </div>
    </header>
    <div class="container">
        <h1 class="mt-4">{category}</h1>
"""

        for subcat, years in sorted(subcats.items()):
            safe_subcat = re.sub(r'[^a-zA-Z0-9]+', '_', subcat)
            html_content += f"<h2 class='mt-3'>{subcat}</h2>"

            html_content += f"<ul class='nav nav-tabs' id='yearTabs-{safe_subcat}' role='tablist'>"
            sorted_years = sorted(years.keys(), reverse=True)
            for idx, year in enumerate(sorted_years):
                active_class = "active" if idx == 0 else ""
                html_content += f"""
                <li class='nav-item' role='presentation'>
                    <button class='nav-link {active_class}' id='tab-{safe_subcat}-{year}' data-bs-toggle='tab' data-bs-target='#content-{safe_subcat}-{year}' type='button' role='tab'>
                        {year}
                    </button>
                </li>
                """
            html_content += "</ul>"

            html_content += f"<div class='tab-content mt-3' id='tabContent-{safe_subcat}'>"
            for idx, year in enumerate(sorted_years):
                active_class = "show active" if idx == 0 else ""
                events = years[year]
                
                html_content += f"""
                <div class='tab-pane fade {active_class}' id='content-{safe_subcat}-{year}' role='tabpanel'>
                """
                
                for event_idx, event in enumerate(events):
                    # Déterminer si l'événement est à venir ou passé
                    is_upcoming = event['datetime'] >= today
                    card_class = "event-upcoming" if is_upcoming else "event-past"
                    status_badge = '<span class="badge bg-success">À venir</span>' if is_upcoming else '<span class="badge bg-secondary">Passé</span>'
                    
                    html_content += f"""
                    <div class="card mb-3 {card_class}">
                        <div class="card-body">
                            <h3 class="card-title">{event['title']} {status_badge}</h3>
                            <p><strong>Date :</strong> {event['date']}</p>
                            <p class="card-text"><strong>Horaire :</strong> {event['start']} - {event.get('end', 'Heure de fin non spécifiée')}</p>
                            <p class="card-text"><strong>Localisation :</strong> {event['Localisation']}</p>
                            <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#desc{safe_subcat}-{year}-{event_idx}" aria-expanded="false">
                                Description
                            </button>
                            <div class="collapse mt-2" id="desc{safe_subcat}-{year}-{event_idx}">
                                <div class="card card-body">
                                    <p>{event['description']}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                html_content += "</div>"
            html_content += "</div>"

        html_content += """
    </div>
</body>
</html>
"""

        with open(f"{output_dir}/{safe_category}.html", "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    print("Les pages HTML ont été générées avec filtrage par année, tri par date et statut des événements.")
else:
    print("❌ Impossible de récupérer le calendrier")