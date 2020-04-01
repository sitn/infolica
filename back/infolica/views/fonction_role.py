from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from .. import models
import logging
log = logging.getLogger(__name__)

###########################################################
# Fonctions roles
###########################################################

""" Return all fonctions
@view_config(route_name='fonctions', request_method='GET', renderer='json')
@view_config(route_name='fonctions_s', request_method='GET', renderer='json')
def fonctions_view(request):
    try:
        query = request.dbsession.query(models.Fonction).all()
        return Utils.serialize_many(query)
    except Exception as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
"""

""" Return all roles
@view_config(route_name='roles', request_method='GET', renderer='json')
@view_config(route_name='roles_s', request_method='GET', renderer='json')
def roles_view(request):
    try:
        query = request.dbsession.query(models.Role).all()
        return Utils.serialize_many(query)
    except Exception as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
"""

""" Return fonctions roles by role id
@view_config(route_name='fonctions_roles_by_id', request_method='GET', renderer='json')
def fonctions_roles_by_id_view(request):
    try:
        id = request.matchdict['id']
        return Utils.get_fonctions_roles_by_id(request, id)

    except Exception as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
"""







