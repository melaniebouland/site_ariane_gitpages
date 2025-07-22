# L'ajout et la modification des documents de travaux



## Introduction
L'ensemble des documents des travaux des GT sont rassemblés dans ce dossier. Vous pouvez les ajouter, modifier leur dénomination ou les retirer à partir du Web EDI, accessible à l'onglet "Modifier" de la page. 
L'ensemble de la page des travaux est généré à partir d'un script Python, imposant des règles de nommage pour un affichage correct dans la page. Si les règles suivantes ne sont pas respectées, les documents ne seront pas reconnus par le script. 

## Règles de nommage
Afin d'intégrer un document au site, ce dernier doit être nommé de la façon suivante :
```
GT*_Annee-mois-jour_Titre_du_document
```
Le script Python filtre les documents d'abord selon le GT mentionné puis classe les documents en fonction de la date, allant du plus récent au plus ancien document. 
Si l'année est uniquement mentionnée, sans le mois ou le jour, le script placera le document en question au début de l'année en question (Le script ajout, par défaut les caractères suivants à une année : 2024-00-00 par exemple).

Attention, les dates ne sont pas mentionnées dans la page du site, elles servent uniquement de filtre. Vous pouvez ainsi mettre un nom de document plus complet au besoin. Pour rappel, les caractères spéciaux ne doivent pas être inclus, afin d'éviter des problèmes d'affichage ou de recherche des documents.

## Pour le GT3
Pour le GT3  et afin d'affiner le triage des documents par ateliers, une règle de nommage s'ajoute. Il est nécessaire de mentionner l'acronyme de l'atelier afin de permettre un tri par atelier. 
```
GT*_Annee-mois-jour_SigleAtelier_Titre_du_document
```