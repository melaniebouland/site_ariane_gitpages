import json
import os
from datetime import datetime
from collections import defaultdict

# Charger les documents depuis documents.json
with open("documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Organiser les documents par GT puis par année
gt_docs_by_year = defaultdict(lambda: defaultdict(list))
all_gts = set()
all_years = set()

for doc in documents:
    gt = doc.get("gt")
    date_str = doc.get("date")
    title = doc.get("title")
    path = doc.get("path")

    if not (gt and date_str and title and path):
        continue

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.year == 1:
            continue
        year = str(date_obj.year)
    except ValueError:
        continue

    all_gts.add(gt)
    all_years.add(year)
    gt_docs_by_year[gt][year].append({"title": title, "path": path})

for gt in gt_docs_by_year:
    for year in gt_docs_by_year[gt]:
        gt_docs_by_year[gt][year].sort(key=lambda d: d["title"].lower())

# Générer les filtres GT et année
def generate_filters_html(gts, years):
    return f'''
<div class="filters my-4 p-3 border rounded bg-light">
  <div class="row">
    <div class="col-md-6 mb-2">
      <label for="gt-filter" class="form-label">Filtrer par GT :</label>
      <select id="gt-filter" class="form-select">
        <option value="all">Tous</option>
        {''.join(f'<option value="{gt}">{gt}</option>' for gt in sorted(gts))}
      </select>
    </div>
    <div class="col-md-6 mb-2">
      <label for="year-filter" class="form-label">Filtrer par année :</label>
      <select id="year-filter" class="form-select">
        <option value="all">Toutes</option>
        {''.join(f'<option value="{year}">{year}</option>' for year in sorted(years, reverse=True))}
      </select>
    </div>
  </div>
</div>
'''

# Générer les sections HTML par GT et année
def generate_sections_html(gt_docs):
    html = ""
    for gt in sorted(gt_docs.keys()):
        html += f'<section class="gt-section mb-5" data-gt="{gt}">\n'
        html += f'  <h2 class="mt-5">{gt}</h2>\n'
        for year in sorted(gt_docs[gt].keys(), reverse=True):
            html += f'  <div class="year-block mb-3" data-year="{year}">\n'
            html += f'    <h4 class="text-secondary">{year}</h4>\n'
            html += '    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">\n'
            for doc in gt_docs[gt][year]:
                html += f'''<div class="col">
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">{doc["title"]}</h5>
      <a href="../{doc["path"]}" target="_blank" class="btn btn-primary btn-sm">Consulter</a>
    </div>
  </div>
</div>\n'''
            html += '    </div>\n  </div>\n'
        html += '</section>\n'
    return html

# HTML complet
html_output = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" sizes="180x180" href="assets/img/logoAriane.jpg">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/main.css">
    <title>Ariane | Travaux</title>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        .dropdown:hover>.dropdown-menu {{display: block;}}
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
        body {{ background-color: #f8f9fa; }}
        .card-title {{ font-size: 1rem; }}
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
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://docs.google.com/forms/d/1nxWiaj88LY7R-poxxlTiUxdvyIH5hL5eBHFjgsfsKGg/viewform?edit_requested=true">Nous rejoindre</a>
                    </li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <h1 class="mb-4">Travaux classés par GT</h1>
        {generate_filters_html(all_gts, all_years)}
        {generate_sections_html(gt_docs_by_year)}
    </main>
    <!-- Footer -->
    <footer class="bg-light py-3">
        <div class="container d-flex justify-content-between align-items-center">
          <div class="text-center flex-grow-1 me-5">
            <p class="mb-0">&copy; 2024 Consortium HN Ariane. Tous droits réservés.</p>
          </div>
          <div class="ms-5">
            <a href="https://consortiumariane.gitpages.huma-num.fr/axe1/credits.html" class="mx-2">Crédits</a>
          </div>
          <div class="ms-5">
            <a href="https://consortiumariane.gitpages.huma-num.fr/axe1/mentions_legales.html" class="mx-2">Mentions légales</a>
          </div>
          <div class="ms-5">
            <a href="https://hal.science/CONSORTIUM-HN-ARIANE" target="_blank" rel="noopener noreferrer">
              <img src="assets/img/HAL_logotype-rvb_fond-clair_fr.png" class="img-fluid">
            </a>
          </div>
        </div>
      </footer>

    <script>
        const gtFilter = document.getElementById("gt-filter");
        const yearFilter = document.getElementById("year-filter");

        function applyFilters() {{
            const selectedGT = gtFilter.value;
            const selectedYear = yearFilter.value;

            document.querySelectorAll(".gt-section").forEach(section => {{
                const gt = section.dataset.gt;
                let showSection = (selectedGT === "all" || gt === selectedGT);
                
                let yearBlocks = section.querySelectorAll(".year-block");
                let hasVisibleBlock = false;

                yearBlocks.forEach(block => {{
                    const year = block.dataset.year;
                    const showBlock = (selectedYear === "all" || year === selectedYear);
                    block.style.display = showBlock ? "" : "none";
                    if (showBlock) hasVisibleBlock = true;
                }});

                section.style.display = (showSection && hasVisibleBlock) ? "" : "none";
            }});
        }}

        gtFilter.addEventListener("change", applyFilters);
        yearFilter.addEventListener("change", applyFilters);
    </script>
</body>
</html>
"""

# Sauvegarde
output_dir = "public/html_pages"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "travaux_CS.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Fichier 'html_pages/travaux_CS.html' généré avec une présentation améliorée.")
