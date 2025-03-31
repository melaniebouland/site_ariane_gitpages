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
            <base href= ".">
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" sizes="180x180" href="assets/img/logoAriane.jpg">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
            <link rel="stylesheet" href="assets/main.css">
            <title>Calendrier - {axe}</title>
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
            </style>
        </head>
        <body class="container">
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
                                    <a class="dropdown-item dropdown-toggle" href="axe1/axe1.html">Axe 1</a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="axe1/GT1/GT1.html">GT1</a></li>
                                        <li><a class="dropdown-item" href="axe1/GT2/GT2.html">GT2</a></li>
                                        <li><a class="dropdown-item" href="axe1/GT3/GT3.html">GT3</a></li>
                                    </ul>
                                </li>
                                <li class="dropdown-submenu">
                                    <a class="dropdown-item dropdown-toggle" href="axe2/axe2.html">Axe 2</a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="axe2/GT4/GT4.html">GT4</a></li>
                                        <li><a class="dropdown-item" href="axe2/GT5/GT5.html">GT5</a></li>
                                        <li><a class="dropdown-item" href="axe2/GT6/GT6.html">GT6</a></li>
                                    </ul>
                                </li>
                                <li class="dropdown-submenu">
                                    <a class="dropdown-item dropdown-toggle" href="axe3/axe3.html">Axe 3</a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="axe3/ethique/ethique.html">Enjeux éthiques</a></li>
                                        <li><a class="dropdown-item" href="axe3/juridique/juridique.html">Questions juridiques</a></li>
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
                                        <li><a class="dropdown-item" href="axe1/GT1/travaux_GT1.html">GT1</a></li>
                                        <li><a class="dropdown-item" href="axe1/GT2/travaux_GT2.html">GT2</a></li>
                                        <li><a class="dropdown-item" href="axe1/GT3/travaux_GT3.html">GT3</a></li>
                                    </ul>
                                </li>
                                <li class="dropdown-submenu">
                                    <a class="dropdown-item dropdown-toggle">Axe 2</a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="axe2/GT4/travaux_GT4.html">GT4</a></li>
                                        <li><a class="dropdown-item" href="axe2/GT5/travaux_GT5.html">GT5</a></li>
                                        <li><a class="dropdown-item" href="axe2/GT6/travaux_GT6.html">GT6</a></li>
                                    </ul>
                                </li>
                                <li class="dropdown-submenu">
                                    <a class="dropdown-item dropdown-toggle">Axe 3</a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="axe3/ethique/travaux_ethique.html">Enjeux éthiques</a></li>
                                        <li><a class="dropdown-item" href="axe3/juridique/travaux_juridique.html">Questions juridiques</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    <li class="nav-item">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="#">Actualités</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://docs.google.com/forms/d/1nxWiaj88LY7R-poxxlTiUxdvyIH5hL5eBHFjgsfsKGg/viewform?edit_requested=true">Nous rejoindre</a>
                    </li>
                    </ul>
                </nav>
            </div>
        </header>
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