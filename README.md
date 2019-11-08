# infolica

## Installation
1. Fork and clone Infolica
1. install requirements:  
   `pip install -r requirements.txt`

## Developpement
1. Change directory into your newly created project.  
   `cd infolica`
1. Create a Python virtual environment.  
   `python3 -m venv env`
1. Upgrade packaging tools.  
   `env/bin/pip install --upgrade pip setuptools`
1. Install the project in editable mode with its testing requirements.  
   `env/bin/pip install -e ".[testing]"`
1. Initialize and upgrade the database using Alembic.  
   1. Generate your first revision.  
      `env/bin/alembic -c development.ini revision --autogenerate -m "init"`
   1. Upgrade to that revision.  
      `env/bin/alembic -c development.ini upgrade head`
1. Load default data into the database using a script. **Pas implémenté**  
   `env/bin/initialize_infolica_db development.ini`
1. Run your project's tests. **Pas implémenté**  
   `env/bin/pytest`
1. Run your project.  
   `env/bin/pserve development.ini`

## Etapes réalisées
* 08.11.2019 MR - Modification du fichier `infolica/models/mymodel.py`. La base de donnée n'a pas encore été générée ni testée.  
* 08.11.2019 MR - Création du projet avec un cookie-cutter: https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/cookiecutters.html   
