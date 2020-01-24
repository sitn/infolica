from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)

from pyramid.security import remember, forget
from pyramid.response import Response
import json
from ..scripts.utils import Utils

class LDAPQuery():


    @classmethod
    def do_login(cls, request, login, password, operateur):
        response = None
        try:
            headers = forget(request)

            # Check if user exists in LDAP
            connector = get_ldap_connector(request)
            data = connector.authenticate(login, password)

            if data is not None:
                dn = data[0]

                headers = remember(request, dn)

                if operateur :
                    operateur_json = Utils.serialize_one(operateur)

                operateur_json_json = json.dumps(operateur_json) if operateur else ''

                response = Response(operateur_json_json,
                                    content_type='application/json; charset=UTF-8', headers=headers)

            else:
                raise Exception('Invalid credentials')

        except Exception as error:
            raise error

        return response


    @classmethod
    def do_logout(cls, request):
        response = None
        try:
            headers = forget(request)
            response = Response('{"error": "false", "code": 200, "message": "User logged out"}', headers=headers)
            response.headerlist.extend(headers)

        except Exception as error:
            raise error

        return response

    @classmethod
    def get_connected_user(cls, request):
        try:
            user_id = request.authenticated_userid

            connector = get_ldap_connector(request)

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(', ', ',').replace(' , ', ',').replace(' ,', ',').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )
                result, ret = conn.get_response(ret)

            if result is None:
                result = []
            else:
                result = [r['attributes'] for r in result
                          if 'dn' in r and r['dn'] == user_id]
                result = result[0] if result and len(result) > 0 else None

                if result is not None:
                    result = json.loads(json.dumps(dict(result)))

        except Exception as error:
            raise error

        return cls.format_json_attributes(result) if result else {}

