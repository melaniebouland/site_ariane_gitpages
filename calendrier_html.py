import json
import os
from datetime import datetime

INPUT_JSON = "calendrier.json"
OUTPUT_DIR = "html_pages"
HTML_TEMPLATE = """<!doctype html>
<html lang="fr-fr">
<head>
    <base href=".">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" sizes="180x180" href="assets/img/logoAriane.jpg">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/main.css">
    <title>{title}</title>
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
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT1/GT1.html">GT1</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT2/GT2.html">GT2</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT3/GT3.html">GT3</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle" href="https://consortiumariane.gitpages.huma-num.fr/axe2">Axe 2</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT4/GT4.html">GT4</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT5/GT5.html">GT5</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT6/GT6.html">GT6</a></li>
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
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT1/travaux_GT1.html">GT1</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT2/travaux_GT2.html">GT2</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT3/travaux_GT3.html">GT3</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle">Axe 2</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT4/travaux_GT4.html">GT4</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT5/travaux_GT5.html">GT5</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe2/GT6/travaux_GT6.html">GT6</a></li>
                                </ul>
                            </li>
                            <li class="dropdown-submenu">
                                <a class="dropdown-item dropdown-toggle">Axe 3</a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe3/ethique/travaux_ethique.html">Enjeux éthiques</a></li>
                                    <li><a class="dropdown-item" href="https://consortiumariane.gitpages.huma-num.fr/axe3/juridique/travaux_juridique.html">Questions juridiques</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                  <li class="nav-item">
                    <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://consortiumariane.gitpages.huma-num.fr/axe1/actualites.html">Actualités</a>
                </li>
                  <li class="nav-item">
                    <a class="nav-link text-gray-400 text-xl transition hover:text-gray-400/75" href="https://docs.google.com/forms/d/1nxWiaj88LY7R-poxxlTiUxdvyIH5hL5eBHFjgsfsKGg/viewform?edit_requested=true">Nous rejoindre</a>
                </li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Fil d'Ariane -->
    <nav aria-label="breadcrumb" class="container my-4">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="https://consortiumariane.gitpages.huma-num.fr/axe1.html">Axe 1</a></li>
            <li class="breadcrumb-item"><a href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT{gt_number}.html">GT{gt_number}</a></li>
            <li class="breadcrumb-item"><a href="https://consortiumariane.gitpages.huma-num.fr/axe1/GT{gt_number}/travaux_GT{gt_number}.html">Travaux du GT{gt_number}</a></li>
        </ol>
    </nav>

    <!-- Contenu -->
    <div class="container-fluid">
        <div class="row">
            <main class="col-md-9 content">
                <div class="container-fluid">
                    <div class="container">
                        <div class="title-container">
                            <h1>Les travaux du GT{gt_number}</h1>
                            <hr>
                        </div>
                        <div class="row">
                            {documents_list}
                        </div>
                    </div>
                </div>
            </main>
            <aside class="col-md-3 sidebar">
                <div class="container-fluid" style="background-color:#19191726; padding: 28px;">
                    <div class="container">
                        <h5>Les compte-rendus du {title}</h5>
                        <p>Suivez l'ensemble de l'activité et des réunions du GT.</p>
                        <a href="travaux/#" class="btn btn-primary btn-sm">Voir plus</a>
                    </div>
                </div>
            </aside>
        </div>
    </div>

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
</body>
</html>
"""

def create_html_page(title, gt_number, files, output_path):
    """ Génère une page HTML pour un groupe de travail donné. """
    if not title or not gt_number:
        print(f"Erreur : title ou gt_number est invalide. title={title}, gt_number={gt_number}")
        return

    document_items = "\n".join(
        f"""
        <div class="col-md-4 mb-4 d-flex">
            <div class="card w-100">
                <a href="../{file.get('path', '#')}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="card-body">
                        <h2 class="card-title">{file.get('name', 'Document inconnu')}</h2>
                    </div>
                </a>
            </div>
        </div>
        """ for file in files if isinstance(file, dict)
    )

    if not document_items:
        print("Aucun document à afficher.")
        document_items = "<p>Aucun document disponible.</p>"

    try:
        html_content = HTML_TEMPLATE.format(title=title, gt_number=gt_number, documents_list=document_items)
    except KeyError as e:
        print(f"Erreur : Placeholder manquant dans HTML_TEMPLATE : {e}")
        return

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Page HTML générée : {output_path}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier {output_path}: {e}")

def load_documents(input_json):
    """ Charge les documents à partir du fichier JSON. """
    if not os.path.exists(input_json):
        print("Le fichier JSON n'existe pas. Exécute d'abord generate_json.py.")
        return None

    try:
        with open(input_json, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier JSON: {e}")
        return None

def categorize_documents(documents):
    """ Catégorise les documents par groupe de travail. """
    categories = {}
    for doc in documents:
        if "name" not in doc or "path" not in doc:
            print(f"Document invalide: {doc}")
            continue
        gt_prefix = doc["name"].split("_")[0]
        if gt_prefix not in categories:
            categories[gt_prefix] = []
        categories[gt_prefix].append(doc)

    # Tri des documents : d'abord par nom, puis par date (descendant)
    for gt_prefix in categories:
        categories[gt_prefix].sort(key=lambda x: (x["name"], datetime.strptime(x["date"], "%Y-%m-%d") if "date" in x else datetime.min), reverse=True)

    return categories

def generate_html_pages(input_json, output_dir):
    """ Parse le JSON et génère des pages HTML par groupe de travail. """
    documents = load_documents(input_json)
    if documents is None:
        return

    categories = categorize_documents(documents)

    os.makedirs(output_dir, exist_ok=True)

    for gt, files in categories.items():
        gt_number = gt.replace("GT", "")  # Extraction du numéro
        output_path = os.path.join(output_dir, f"travaux_{gt}.html")
        create_html_page(f"Travaux du {gt}", gt_number, files, output_path)

if __name__ == "__main__":
    generate_html_pages(INPUT_JSON, OUTPUT_DIR)
