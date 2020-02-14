from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from sqlalchemy import desc

from sqlalchemy.exc import DBAPIError
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
    numero_id = request.matchdict["id"]
    
    # get data
    try:
        record = request.dbsession.query(models.VNumerosRelations).filter(models.VNumerosRelations.numero_associe_id == numero_id).all()

        if not record:
            raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.VNumerosRelations.__tablename__, numero_id))

        return Utils.serialize_many(record)

    except Exception as e:
        log.error(e)
        print(e)
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}
        

""" Get new numero_associe_relations """
@view_config(route_name='numero_associe_relations_by_id', request_method='GET', renderer='json')
def numero_associe_relations_view(request):
    numero_id = request.matchdict["id"]
    
    # get data
    try:
        record = request.dbsession.query(models.VNumerosRelations).filter(models.VNumerosRelations.numero_base_id == numero_id).all()

        if not record:
            raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.VNumerosRelations.__tablename__, numero_id))

        return Utils.serialize_many(record)

    except Exception as e:
        log.error(e)
        print(e)
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}
        

