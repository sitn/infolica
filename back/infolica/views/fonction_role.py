# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from infolica.models import Role
from infolica.scripts.utils import Utils


from infolica.scripts.authentication import check_connected, get_user_functions

import logging
log = logging.getLogger(__name__)

###########################################################
# Fonctions roles
###########################################################

@view_config(route_name='fonctions_roles_current_user', request_method='GET', renderer='json')
def fonctions_roles_current_user_view(request):
    """
    Return fonctions of current user
    """
    authorized_services = [*[request.registry.settings['service_mo'].replace(' ', '')], *request.registry.settings['preavis_services_externes'].replace(' ', '').split(',')]

    # Check connected
    if not check_connected(request, services=authorized_services):
        raise exc.HTTPForbidden()

    return get_user_functions(request)


@view_config(route_name='user_roles', request_method='GET', renderer='json')
def fonctions_user_roles_view(request):
    """
    Return user roles
    """
    if not check_connected(request):
        raise exc.HTTPForbidden()

    roles = request.dbsession.query(Role).all()

    return Utils.serialize_many(roles)

