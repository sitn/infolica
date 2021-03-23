# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.models.models import VNextNumeroMOAvilable
from infolica.scripts.utils import Utils


@view_config(route_name='numero_mo_next', request_method='GET', renderer='json')
def numero_mo_next_view(request):
    """
    Return all next available numero MO par cadastre, type et plan
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    cadastre_id = request.params['cadastre_id'] if 'cadastre_id' in request.params else None
    type_id = request.params['type_id'] if 'type_id' in request.params else None
    plan = request.params['plan'] if 'plan' in request.params else None

    query = request.dbsession.query(VNextNumeroMOAvilable)
    if cadastre_id:
        query = query.filter(VNextNumeroMOAvilable.cadastre_id == cadastre_id)
    if type_id:
        query = query.filter(VNextNumeroMOAvilable.numero_type_id == type_id)
    if plan:
        query = query.filter(VNextNumeroMOAvilable.plan == plan)
    
    query = query.all()
        
    return Utils.serialize_many(query)
