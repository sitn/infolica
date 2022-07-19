from pyramid.paster import get_app, setup_logging
import os

configfile = os.environ.get('BACK_INI_FILE', 'production.ini')

setup_logging(configfile)
application = get_app(configfile)
