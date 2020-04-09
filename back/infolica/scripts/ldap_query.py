from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)

from pyramid.security import remember, forget
from pyramid.response import Response
import json


class LDAPQuery():


    @classmethod
    def do_login(cls, request, login, password):
        resp_json = None
        try:
            headers = forget(request)

            # Check if user exists in LDAP
            connector = get_ldap_connector(request)
            data = connector.authenticate(login, password)

            if data is not None:
                dn = data[0]

                if dn == 'null':
                    raise Exception('Invalid credentials')

                resp_json = {}

                resp_json['role_name'] = cls.get_user_group_by_dn(request, dn)
                resp_json['dn'] = dn

            else:
                raise Exception('Invalid credentials')

        except Exception as error:
            raise error

        return resp_json


    @classmethod
    def do_logout(cls, request):
        response = None
        try:
            headers = forget(request)
            response = Response('{"error": "false", "code": 200, "message": "User logged out"}', headers=headers)
            #response.headerlist.extend(headers)

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

    @classmethod
    def get_user_group_by_dn(cls, request, dn):
        groups = []
        try:
            connector = get_ldap_connector(request)
            result = connector.user_groups(dn)

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

                if groups and len(groups) > 0:
                    cn_attribute = request.registry.settings['ldap_group_attribute_id']
                    infolica_group_prefix = request.registry.settings['infolica_groups_prefix']

                    for group in groups:
                        group_name = group[cn_attribute]

                        if group_name.startswith(infolica_group_prefix):
                            return group_name

        except Exception as error:
            raise error

        return None

    @classmethod
    def format_json_attributes(cls, json_obj):
        for key in json_obj:
            if isinstance(json_obj[key], list) and len(json_obj[key]) > 0:
                json_obj[key] = json_obj[key][0]

        return json_obj