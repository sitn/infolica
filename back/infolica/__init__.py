from pyramid.config import Configurator
from pyramid.events import NewRequest
from papyrus.renderers import GeoJSON

from pyramid.renderers import JSONP

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import os

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_mako')
        config.include('.routes')
        config.scan()
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)
        config.add_renderer('jsonp', JSONP(param_name='callback'))
        # Add the "geojson" renderer
        config.add_renderer("geojson", GeoJSON())

        config.set_authentication_policy(
            AuthTktAuthenticationPolicy(
                settings["authtkt_secret"],
                cookie_name=settings["authtkt_cookie_name"],
                samesite=settings["authtk_samesite"],
                secure=settings["authtk_secure"]
            )
        )
        config.set_authorization_policy(
            ACLAuthorizationPolicy()
        )

        # store postal codes of canton de Neuchâtel
        config.add_settings({'npa_NE': getPostalCodesNeuchatel()})

    return config.make_wsgi_app()

#Add Header
def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': request.registry.settings['access_control_allow_origin'],
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


#Get NPA of canton de Neuchâtel
def getPostalCodesNeuchatel():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(parent_dir, "static", "npa_NE.txt"), "r") as f:
        lines = f.readlines()
        npa_NE = [int(line.rstrip()) for line in lines]
        return npa_NE
