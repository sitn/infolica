# -*- coding: utf-8 -*--
from pyramid.response import Response
from pyramid.security import forget
from infolica.models.models import Operateur
from sqlalchemy import func
import logging



LOG = logging.getLogger(__name__)


def do_logout(request):
    headers = forget(request)
    request.response.headers = headers
    response = Response('{"error": "false", "code": 200, "message": "User logged out"}', headers=headers)
    return response


def check_connected(request, services=None):
    """
    check connection
    """
    if services is None:
        services = [request.registry.settings['service_mo'].replace(' ', '')]

    user = request.authenticated_userid

    if user is None:
        return False
    
    operateur = request.dbsession.query(Operateur).filter(
        func.lower(Operateur.login) == user
    ).first()

    if operateur.service in services:
        return True
    else:
        return False


def get_user_functions(request):
    
    results = {}

    operateur = request.dbsession.query(Operateur).filter(
        func.lower(Operateur.login) == request.authenticated_userid
    ).first()

    if operateur:
        fonctions = operateur.role.fonctions
        results['role_id'] = operateur.role.id
        results['role_name'] = operateur.role.nom
        results['fonctions'] = [x.nom for x in fonctions]
    
    return results
