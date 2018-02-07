# Nuclei-challenge
Kaggle challenge

Installation des librairies Python :

- Commencer par installer Miniconda qui te permet d'avoir le gestionnaire de paquets Conda : 
https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

- Lancer la commande suivante (en récupérant d'abord le fichier datascience.yml
**conda env create -f datascience.yml**

Petite explication : Le fichier datascience.yml contient la liste de toutes les librairies nécessaire pour du DeepLearning. La commande va créer un environnement virtuel avec ses propres variables d'environnements. 
Ca évite les conflits avec les librairies Python utilisées par l'OS.

Si jamais il manque des librairies, on peut toujours mettre à jour le fichier yml, et appeler la comande

**conda env update -f datascience.yml**

L'avantage d'utiliser le fichier c'est aussi qu'il gère toutes les dépendances, alors que si tu crées un environnement de développement et que tu fais : **conda install librairie1**, a priori rien ne te garantis que cette librairie sera compatible avec les librairies déjà installées.

- Une fois la commande lancée, il faut faire **source activate datascience** pour entrer dans l'environnement virtuel.

- Pour info, l'IDE c'est spyder, et il y a aussi jupyter notebook qui permet de prototyper plus rapidement. En revanche, tu verras que c'est moins accueillant que Matlab...
