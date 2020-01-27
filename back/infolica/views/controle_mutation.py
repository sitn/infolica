from pyramid.view import view_config
from pyramid.response import Response
from ..scripts.utils import Utils
from ..models import Constant
import transaction

from sqlalchemy.exc import DBAPIError
from ..exceptions.custom_error import CustomError

from .. import models

import logging
log = logging.getLogger(__name__)


""" Return all controles_mutations"""
@view_config(route_name='controles_mutations', request_method='GET', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='GET', renderer='json')
def controles_mutations_view(request):
    try:
        query = request.dbsession.query(models.ControleMutation).all()
        return Utils.serialize_many(query)
    
    except DBAPIError as e:
        log.error(str(e), exc_info=True)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Return controle_mutation by id"""
@view_config(route_name='controle_mutation_by_id', request_method='GET', renderer='json')
def controles_mutations_by_id_view(request):
    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None
    
    try:
        query = request.dbsession.query(models.ControleMutation).filter(models.ControleMutation.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    

""" Add new controle_mutation"""
@view_config(route_name='controles_mutations', request_method='POST', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='POST', renderer='json')
def controles_mutations_new_view(request):

    record = models.ControleMutation()
    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ControleMutation.__tablename__))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update controle_mutation"""
@view_config(route_name='controles_mutations', request_method='PUT', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='PUT', renderer='json')
def controles_mutations_update_view(request):

    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None

    # Get controle mutation record
    record = request.dbsession.query(models.ControleMutation).filter(
        models.ControleMutation.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.ControleMutation.__tablename__, id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ControleMutation.__tablename__))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Delete controle_mutation"""
@view_config(route_name='controles_mutations', request_method='DELETE', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='DELETE', renderer='json')
def controles_mutations_delete_view(request):
    
    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None

    # Get controle mutation record
    record = request.dbsession.query(models.ControleMutation).filter(
        models.ControleMutation.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.ControleMutation.__tablename__, id))
    
    try:
        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.ControleMutation.__tablename__))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    

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

