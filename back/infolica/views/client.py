from datetime import datetime
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


""" Return all types clients"""
@view_config(route_name='types_clients', request_method='GET', renderer='json')
@view_config(route_name='types_clients_s', request_method='GET', renderer='json')
def types_clients_view(request):
    try:
        query = request.dbsession.query(models.ClientType).all()
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return all clients"""
@view_config(route_name='clients', request_method='GET', renderer='json')
@view_config(route_name='clients_s', request_method='GET', renderer='json')
def clients_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Client).all()
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return client by id"""
@view_config(route_name='client_by_id', request_method='GET', renderer='json')
def client_by_id_view(request):
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Client).filter(
            models.Client.id == id).first()
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_one(query)


""" Search clients"""
@view_config(route_name='recherche_clients', request_method='POST', renderer='json')
@view_config(route_name='recherche_clients_s', request_method='POST', renderer='json')
def clients_search_view(request):
    try:
        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(models.Client, request.params)
        query = request.dbsession.query(models.Client).order_by(models.Client.nom, models.Client.prenom).filter(
            *conditions).all()[:search_limit]
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new client"""
@view_config(route_name='clients', request_method='POST', renderer='json')
@view_config(route_name='clients_s', request_method='POST', renderer='json')
def clients_new_view(request):
    # Get client instance
    model = Utils.set_model_record(models.Client(), request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            request.dbsession.flush()
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Client.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update client"""
@view_config(route_name='clients', request_method='PUT', renderer='json')
@view_config(route_name='clients_s', request_method='PUT', renderer='json')
def clients_update_view(request):
    # Get client_id
    id_client = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Client).filter(
        models.Client.id == id_client).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            models.Client.__tablename__, id_client))

    # Read params client
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:

            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Client.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Delete client"""
@view_config(route_name='clients', request_method='DELETE', renderer='json')
@view_config(route_name='clients_s', request_method='DELETE', renderer='json')
def clients_delete_view(request):
    # Get client_id
    id_client = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Client).filter(
        models.Client.id == id_client).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            models.Client.__tablename__, id_client))

    model.sortie = datetime.utcnow()

    try:
        with transaction.manager:

            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Client.__tablename__))

    except DBAPIError as e:
        log.error(e)
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
