# infolica

## Installation for development
Fork and clone Infolica.  
1. Change directory into your newly created project  
   `cd infolica\back`
1. Create a Python virtual environment  
   `python3 -m venv env`
1. Launch the virtual environment  
   `env\Scripts\activate`
1. Install requirements  
   `pip install -r requirements.txt`
1. Rename `development.ini.template` to `development.ini`  
   Open the file and adapt `sqlalchemy.url`, `ldap_url` and `ldap_passwd`
1. Install the project in editable mode with its testing requirements  
   `pip install -e ".[testing]"`
1. Create the first migration of your database  
   `alembic -c development.ini revision --autogenerate -m "init"`  
   `alembic -c development.ini upgrade head`
1. Run your project  
   `pserve development.ini`

## Testing
Tests are done with pytest python framework.
1. Run your project's tests **Not implemented yet**  
   `pytest`

