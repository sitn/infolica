from pyramid.paster import get_app, setup_logging
import os

instance = os.environ.get('INSTANCE', 'production')
configfile = f'{instance}.ini'

setup_logging(configfile)
application = get_app(configfile)
