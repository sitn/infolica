from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.security import remember
from papyrus.renderers import GeoJSON

#Authentification
from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)
from pyramid_multiauth import MultiAuthenticationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from infolica.scripts.authentication import RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def _create_get_user_from_request(settings):
    def get_user_from_request(request):
        """ Return the User object for the request.
        Return ``None`` if:
        * user is anonymous
        * it does not exist in the database
        * the referer is invalid
        
        """
        from infolica.scripts.ldap_query import LDAPQuery

        if not hasattr(request, "_user"):
            request._user = None
            username = request.authenticated_userid

            if username is not None:
                username = username.lower()
                # We know we will need the role object of the
                # user so we use joined loading
                dn = LDAPQuery.ldap_get_user(request, username)
                #user = DBSession.query(User) \
#                    .filter_by(username=username) \
#                    .first()

                if dn is not None:
                    headers = remember(request, dn)
                    print('headers')
                    print(headers)
                    request.response.headerlist.extend(headers)
                    request._dn = dn

        return request._dn
    return get_user_from_request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_mako')
        config.include('.routes')
        config.include('pyramid_ldap3')
        config.scan()
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

        # Add the "geojson" renderer
        config.add_renderer("geojson", GeoJSON())

        authtkt_authentication_policy = AuthTktAuthenticationPolicy(
            settings['authtkt_secret'],
            cookie_name=settings['authtkt_cookie_name'],
            hashalg='sha512'
        )

        remote_auth_policy = RemoteUserAuthenticationPolicy(
                environ_key='Remote-User'
        )
        
        authentication_policy = MultiAuthenticationPolicy([
           remote_auth_policy,
           authtkt_authentication_policy
        ])

        config.set_authentication_policy(authentication_policy)

        config.set_authorization_policy(
            ACLAuthorizationPolicy()
        )

        config.add_request_method(
            _create_get_user_from_request(settings),
            name="dn",
            property=True
        )

        config.ldap_setup(
            settings['ldap_url'],
            bind=settings['ldap_bind'],
            passwd=settings['ldap_passwd'])

        config.ldap_set_login_query(
            base_dn=settings['ldap_login_query_base_dn'],
            filter_tmpl=settings['ldap_login_query_filter_tmpl'],
            attributes=settings['ldap_login_query_attributes'].replace(', ', ',').replace(' , ', ',').replace(' ,',
                                                                                                              ',').split(
                ','),
            scope=settings['ldap_login_query_scope'])

        config.ldap_set_groups_query(
            base_dn=settings['ldap_group_query_base_dn'],
            filter_tmpl=settings['ldap_group_query_filter_tmpl'],
            scope=settings['ldap_group_query_scope'],
            cache_period=int(settings['ldap_group_query_cache_period']),
            attributes=settings['ldap_group_attributes'].replace(', ', ',').replace(' , ', ',').replace(' ,',
                                                                                                        ',').split(','))

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
