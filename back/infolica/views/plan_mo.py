# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.models.models import VPlan
from infolica.scripts.utils import Utils


@view_config(route_name='plans_mo', request_method='GET', renderer='json')
def plans_mo_view(request):
    """
    Return all plans_mo
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VPlan).order_by(VPlan.planno.asc()).all()
        
    return Utils.serialize_many(query)
