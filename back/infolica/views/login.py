# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.response import Response
from pyramid.security import remember

from sqlalchemy import func

from infolica.models.models import Operateur
from infolica.scripts.authentication import do_logout
from infolica.scripts.ldap_query import LDAPQuery
from infolica.scripts.utils import Utils

import logging
log = logging.getLogger(__name__)


@view_config(route_name='login', request_method='POST', renderer='json')
@view_config(route_name='login_s', request_method='POST', renderer='json')
def login_view(request):
    """
    Login
    """
    login = None
    password = None

    if 'login' in request.params:
        login = request.params['login'].lower()

    if 'password' in request.params:
        password = request.params['password']

    # Check if user exists in DB
    query = request.dbsession.query(Operateur)
    log.info('Attempt to log with: {}'.format(login))
    operateur = query.filter(func.lower(
        Operateur.login) == login).first()

    if not operateur:
        return exc.HTTPNotFound('Username {} was not found'.format(login))

    try:
        resp_json = LDAPQuery.do_login(request, login, password)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    operateur_json = None

    if resp_json and 'dn' in resp_json:
        headers = remember(request, login)
        request.response.headerlist.extend(headers)

        if operateur:
            operateur_json = Utils.serialize_one(operateur)

    return operateur_json


@view_config(route_name='logout', request_method='GET', renderer='json')
def logout_view(request):
    """
    Logout
    """
    response = None
    try:
        response = do_logout(request)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response
