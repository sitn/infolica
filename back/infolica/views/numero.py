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


""" Return all numeros"""
@view_config(route_name='numeros', request_method='GET', renderer='json')
@view_config(route_name='numeros_s', request_method='GET', renderer='json')
def numeros_view(request):
    try:
        query = request.dbsession.query(models.VNumeros).all()
        return Utils.serialize_many(query)
    
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Return numeros by id"""
@view_config(route_name='numero_by_id', request_method='GET', renderer='json')
def numeros_by_id_view(request):
    try:
        # Get controle mutation id    
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.VNumeros).filter(models.VNumeros.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    

""" Add new numeros"""
@view_config(route_name='numeros', request_method='POST', renderer='json')
@view_config(route_name='numeros_s', request_method='POST', renderer='json')
def numeros_new_view(request):
    #nouveau numero
    record = models.Numero()
    record = Utils.set_model_record(record, request.params)
    
    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update numeros"""
@view_config(route_name='numeros', request_method='PUT', renderer='json')
@view_config(route_name='numeros_s', request_method='PUT', renderer='json')
def numeros_update_view(request):

    # Get numero id
    id = request.params['id'] if 'id' in request.params else None

    # Get numero record
    record = request.dbsession.query(models.Numero).filter(
        models.Numero.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Numero.__tablename__, id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


# """ Delete numeros"""
# @view_config(route_name='numeros', request_method='DELETE', renderer='json')
# @view_config(route_name='numeros_s', request_method='DELETE', renderer='json')
# def numeros_delete_view(request):
#     """
#     Les numéros supprimés peuvent être des numéros abandonnés (etat_id = 3) ou supprimés (etat_id = 4).
#     Les numéros ne sont pas supprimés de la base de données, mais mis à jour avec le bon code etat_id.
#     """
#     # Get numero id
#     id = request.params['id'] if 'id' in request.params else None

#     # Get numero record
#     record = request.dbsession.query(models.Numero).filter(
#         models.Numero.id == id).first()

#     if not record:
#         raise CustomError(
#             CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Numero.__tablename__, id))

#     try:
#         with transaction.manager:
#             # Commit transaction
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Numero.__tablename__))

#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
    

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

