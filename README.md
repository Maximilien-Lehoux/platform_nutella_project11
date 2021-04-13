# 1. Objet du projet 8 - plateforme PurBeurre
Réalisation d'une application qui permet de trouver des substituts plus sains à des aliments trop gras ou trop sucrés à partir de recherches sur la plateforme libre et ouverte OpenFoodFacts dont l'objectif est de répertorier les caractéristiques nutritives de produits alimentaires commercialisés dans le monde entier.

## Branche principale "master"

## 2. Ressources extérieures utilisées :
API OpenFoodFacts.

## 3. Outils
Environnement virtuel
Développement en python 3.7,
Base de données PostgreSQL 13.0,
Gestion des templates et des tables avec Django 3.1,
Design avec Bootstrap 4.
Déploiement sur la plateforme Heroku - lien :

## 4. Installation des dépendances
"""
pip install -r requirements.txt
"""

## 5. Tests
Lancer les tests :
"""
manage.py test
"""

## 6. Lancement en local
Créer et remplir la base de données :
(utilisation de postgreSQL, modifiez-vos donnée serveur dans le fichier setting )

Vous pouvez modifier le nombre de produits pris dans la base de données
d'open-food-fact en le modifiant dans "food/constant.py"


Commande de lancement =
"""
manage.py migrate
manage.py makemigrations
"""

Lancer l'application :
"""
python manage.py runserver
"""