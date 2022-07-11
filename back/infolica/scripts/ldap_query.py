# -*- coding: utf-8 -*--
from pyramid.exceptions import ConfigurationError
from ldap3 import Connection, Server, NTLM

import logging

LOG = logging.getLogger(__name__)


class LDAPQuery(object):

    @classmethod
    def do_login(cls, request, login, password, domain):
        settings = request.registry.settings
        # Check if user exists in LDAP
        try:
            server = Server(settings['ldap_url'])
            with Connection(server=server, user=domain+"\\"+login, password=password, auto_bind=True, authentication=NTLM) as conn:
                result = conn.search(
                    search_base=settings['ldap_login_base_dn'],
                    search_filter=settings['ldap_login_filter_tmpl'].format(login),
                    search_scope=settings['ldap_login_scope'],
                    attributes=settings['ldap_login_attributes'].split(",")
                )

                if result is True:
                    resp_json = {}
                    resp_json['dn'] = conn.entries[0]
                    return resp_json
                
                else:
                    raise Exception('LDAP authentication failed')

        except ConfigurationError as error:
            LOG.error('Connector is not well configured. Error is : {}'.format(error))
