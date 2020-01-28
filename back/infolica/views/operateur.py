from pyramid.view import view_config
from pyramid.response import Response

from pyramid.view import exception_view_config

from pyramid.httpexceptions import (
    HTTPOk,
    HTTPException,
    HTTPBadRequest
)

from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import logging
log = logging.getLogger(__name__)

from datetime import datetime


""" Return all operateurs"""
@view_config(route_name='operateurs', request_method='GET', renderer='json')
@view_config(route_name='operateurs_s', request_method='GET', renderer='json')
def operateurs_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Operateur).all()
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return operateur by id"""
@view_config(route_name='operateur_by_id', request_method='GET', renderer='json')
def operateur_by_id_view(request):
    merged = None
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Operateur).filter(models.Operateur.id == id).first()
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_one(query)


""" Add new operateur"""
@view_config(route_name='operateurs', request_method='POST', renderer='json')
@view_config(route_name='operateurs_s', request_method='POST', renderer='json')
def operateurs_new_view(request):
    # Get operateur instance
    model = Utils.set_model_record(models.Operateur(), request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            request.dbsession.flush()
            print("model.id = ", model.id)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}
    

""" Update operateur"""
@view_config(route_name='operateurs', request_method='PUT', renderer='json')
@view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
def operateurs_update_view(request):
    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Operateur).filter(models.Operateur.id == id_operateur).first()
    
    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Operateur.__tablename__, id_operateur))
    
    # Read params operateur
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


""" Delete operateur"""
@view_config(route_name='operateurs', request_method='DELETE', renderer='json')
@view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
def operateurs_delete_view(request):
    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Operateur).filter(models.Operateur.id == id_operateur).first()
    
    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Operateur.__tablename__, id_operateur))

    model.sortie = datetime.utcnow()

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Operateur.__tablename__))


    except DBAPIError as e:
        log.error(e)
        return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
