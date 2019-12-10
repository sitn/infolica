# infolica

## Installation for development
Fork and clone Infolica.  
1. Change directory into your newly created project  
   `cd infolica`
1. Create a Python virtual environment  
   `python3 -m venv env`
1. Launch the virtual environment  
   `env\Scripts\activate`
1. Install requirements  
   `pip install -r requirements.txt`
1. Rename `development.ini.template` to `development.ini`  
   Open the file and adapt `sqlalchemy.url`
1. Install the project in editable mode with its testing requirements  
   `pip install -e ".[testing]"`
1. Upgrade to that revision  
   `alembic -c development.ini upgrade head`

1. Load default data into the database using a script **Pas implémenté**  
   `initialize_infolica_db development.ini`
1. Run your project's tests **Pas implémenté**  
   `pytest`

1. Run your project  
   `pserve development.ini`
