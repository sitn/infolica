from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..exceptions.custom_error import CustomError

from .. import models

import logging
log = logging.getLogger(__name__)

###########################################################
# NUMERO ETAT HISTO
###########################################################

""" Get new numero_base_relations """
@view_config(route_name='numero_base_relations_by_id', request_method='GET', renderer='json')
def numero_base_relations_view(request):
    # get data
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        numero_id = request.matchdict["id"]

        record = request.dbsession.query(models.VNumerosRelations).filter(models.VNumerosRelations.numero_associe_id == numero_id).all()

        if record:
            return Utils.serialize_many(record)
        else:
            return None

    except Exception as e:
        log.error(e)
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}
        

""" Get new numero_associe_relations """
@view_config(route_name='numero_associe_relations_by_id', request_method='GET', renderer='json')
def numero_associe_relations_view(request):
    # get data
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        numero_id = request.matchdict["id"]

        record = request.dbsession.query(models.VNumerosRelations).filter(models.VNumerosRelations.numero_base_id == numero_id).all()

        if record:
            return Utils.serialize_many(record)
        else:
            return None

    except Exception as e:
        log.error(e)
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}
        

