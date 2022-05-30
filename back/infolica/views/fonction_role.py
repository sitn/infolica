# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

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
    authorized_services = ['SGRF', 'SAT','SU_NE']

    # Check connected
    if not check_connected(request, services=authorized_services):
        raise exc.HTTPForbidden()

    return get_user_functions(request)

