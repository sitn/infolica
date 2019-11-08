# infolica

## Installation
1. Fork and clone `infolica`
1. Install requirements `pip install -r requirements.txt`

## Getting Started
1. Change directory into your newly created project. 
   `cd infolica`
1. Install the project in editable mode with its testing requirements.
   `env/bin/pip install -e ".[testing]"`
1. Initialize and upgrade the database using Alembic.
   1. Generate your first revision.
      `env/bin/alembic -c development.ini revision --autogenerate -m "init"`
   1. Upgrade to that revision.
      `env/bin/alembic -c development.ini upgrade head`
1. Load default data into the database using a script. (not implemented yet)
   `env/bin/initialize_infolica_db development.ini`
1. Run your project's tests. (not implemented yet)
   `env/bin/pytest`
1. Run your project.
   `env/bin/pserve development.ini --reload`


# Etat d'avancement
* 07.11.2019 MR - modification du fichier `infolica\models\mymodel.py`. La BD n'est pas encore créée
* 07.11.2019 MR - initialisation du projet à l'aide du cookie-cutter (cf https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/cookiecutters.html)
 
