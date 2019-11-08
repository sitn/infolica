# infolica

## Installation
Fork and clone Infolica.  
Modify `sqlalchemy.url` in `development.ini` to something like `postgresql//username:password@host:port/database`.  
`Push` the developments in the forked project and then `pull request` into sitn/infolica.  

## Developpement
1. Change directory into your newly created project.  
   `cd infolica`
1. Create a Python virtual environment.  
   `python3 -m venv env`
1. Launch the virtual environment.
   `python/bin/activate`
1. Upgrade packaging tools.  
   `pip install --upgrade pip setuptools`
1. Install the project in editable mode with its testing requirements.  
   `pip install -e ".[testing]"`
1. Initialize and upgrade the database using Alembic.  
   1. Generate your first revision.  
      `alembic -c development.ini revision --autogenerate -m "init"`
   1. Upgrade to that revision.  
      `alembic -c development.ini upgrade head`
1. Load default data into the database using a script. **Pas implémenté**  
   `initialize_infolica_db development.ini`
1. Run your project's tests. **Pas implémenté**  
   `pytest`
1. Run your project.  
   `pserve development.ini`

## Etapes réalisées
* 08.11.2019 MR - Modification du fichier `infolica/models/mymodel.py`. La base de donnée n'a pas encore été générée ni testée.  
* 08.11.2019 MR - Création du projet avec un cookie-cutter: https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/cookiecutters.html   

