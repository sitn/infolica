from pyramid.view import view_config
import pyramid.httpexceptions as exc

from .. import models
from ..scripts.utils import Utils

import logging
log = logging.getLogger(__name__)

###########################################################
# Cadastre
###########################################################

""" GET cadastre"""
@view_config(route_name='cadastres', request_method='GET', renderer='json')
@view_config(route_name='cadastres_s', request_method='GET', renderer='json')
def cadastre_view(request):
    try:
        # Check connected
        #if not Utils.check_connected(request):
            #raise exc.HTTPForbidden()

        records = request.dbsession.query(models.Cadastre).order_by(models.Cadastre.nom).all()
        return Utils.serialize_many(records)

    except Exception as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

