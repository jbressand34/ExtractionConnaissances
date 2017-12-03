# Détection de levée de culture à partir d’images satellites

## Installation

Pour installer l'environnement d'execution du programme faire :
* virtualenv venv
* (utiliser python 3)
* source venv/bin/activate
* pip install -r requirements.txt

## Configuration

Dans le fichier config.json :
* "pathToDataDirectory" : chemin a partir du repertoire courant vers le repertoire contenant les fichiers data_matrix.json, data_parcelles.json etc...
* "pretraitementDejaFait" : par default faux, le programme principal va refaire les pretraitement. Si vous executer le programme et que vous souhaitez reexecuter le programme sans avoir touche au parametre de configuration : "representativite" alors mettre true.
* "represantativite" : voulez-vous pour le pretraitement l'approche chevauchement (faux) ou l'approche chevauchement avec representativite (true).
* "nombreEpoquesEntrainement", "nombreCouches", "nombrNoeudFullyConnected", "tailleSequenceInputModele" : parametres du modele CNN.
* "visualisationPrediction" : voulez-vous visualiser les predictions faites par le modele ?

## Execution

python main.py
Regarder les performances du modele dans path+"performancesModele.txt"
## Auteurs

* Anastasiia Prysiazhniuk 
* Jeremy Bressand
