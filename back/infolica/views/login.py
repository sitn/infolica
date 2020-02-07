from ..exceptions.custom_error import CustomError
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy.exc import DBAPIError
from sqlalchemy import exc, func
from .. import models
from ..scripts.ldap_query import LDAPQuery
from ..models import Constant
import logging
log = logging.getLogger(__name__)


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

        response = LDAPQuery.do_login(request, login, password, operateur)

    except Exception as error:
        # log.error(str(error))
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

