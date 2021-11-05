# -*- coding: utf-8 -*--
from pyramid.exceptions import ConfigurationError
from pyramid_ldap3 import get_ldap_connector

import logging

LOG = logging.getLogger(__name__)


class LDAPQuery(object):

    @classmethod
    def do_login(cls, request, login, password):

        # Check if user exists in LDAP
        try:
            connector = get_ldap_connector(request)
        except ConfigurationError as error:
            LOG.error('Connector is not well configured. Error is : {}'.format(error))
        data = connector.authenticate(login, password)

        if data is not None:
            dn = data[0]

            if dn == 'null':
                raise Exception('Invalid credentials')

            resp_json = {}
            resp_json['dn'] = dn

            return resp_json

        else:
            raise Exception('LDAP authentication failed')
