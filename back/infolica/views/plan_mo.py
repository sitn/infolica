# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.models.models import VPlan
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected


@view_config(route_name='plans_mo', request_method='GET', renderer='json')
def plans_mo_view(request):
    """
    Return all plans_mo
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VPlan).order_by(
        VPlan.cadastre_id.asc(), 
        VPlan.planno.asc()
    ).all()

    return Utils.serialize_many(query)
