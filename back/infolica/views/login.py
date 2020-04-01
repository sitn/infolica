from ..exceptions.custom_error import CustomError
from pyramid.response import Response
from pyramid.security import remember
import json
from pyramid.view import view_config
from sqlalchemy import func
from .. import models
from ..scripts.ldap_query import LDAPQuery
import logging
log = logging.getLogger(__name__)
from ..scripts.utils import Utils

########################################################
# Login
########################################################
@view_config(route_name='login', request_method='POST', renderer='json')
@view_config(route_name='login_s', request_method='POST', renderer='json')
def login_view(request):
    response = None

    try:
        login = None
        password = None

        if 'login' in request.params:
            login = request.params['login']

        if 'password' in request.params:
            password = request.params['password']

        # Check if user exists in DB
        query = request.dbsession.query(models.Operateur)
        operateur = query.filter(func.lower(
            models.Operateur.login) == func.lower(login)).first()

        if not operateur:
            raise Exception(CustomError.USER_NOT_FOUND_EXCEPTION)

        resp_json = LDAPQuery.do_login(request, login, password)

        if resp_json and 'dn' in resp_json:
            headers = remember(request, resp_json['dn'])

            if operateur:
                operateur_json = Utils.serialize_one(operateur)

                operateur_json['role_id'] = Utils.get_role_id_by_name(request, resp_json['role_name'])
                operateur_json['role_name'] = resp_json['role_name']
                operateur_json['fonctions'] = Utils.get_fonctions_roles_by_id(request, operateur_json['role_id'])
                operateur_json['fonctions'] = [x["nom"] for x in operateur_json['fonctions']]

                operateur_json = json.dumps(operateur_json) if operateur else ''

                response = Response(operateur_json, content_type='application/json; charset=UTF-8', headers=headers)

    except Exception as error:
        log.error(str(error), exc_info=True)
        request.response.status = 403
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response


########################################################
# Logout
########################################################
@view_config(route_name='logout', request_method='GET', renderer='json')
def logout_view(request):
    response = None
    try:
        response = LDAPQuery.do_logout(request)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response

