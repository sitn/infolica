from datetime import datetime
from pyramid.view import view_config, exception_view_config
import pyramid.httpexceptions as exc
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import logging
log = logging.getLogger(__name__)


""" Return all operateurs"""
@view_config(route_name='operateurs', request_method='GET', renderer='json')
@view_config(route_name='operateurs_s', request_method='GET', renderer='json')
def operateurs_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Operateur).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
    

""" Return operateur by id"""
@view_config(route_name='operateur_by_id', request_method='GET', renderer='json')
def operateur_by_id_view(request):
    merged = None
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Operateur).filter(
            models.Operateur.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Search operateurs"""
@view_config(route_name='recherche_operateurs', request_method='POST', renderer='json')
@view_config(route_name='recherche_operateurs_s', request_method='POST', renderer='json')
def operateurs_search_view(request):
    try:
        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(models.Operateur, request.params)

        query = request.dbsession.query(models.Operateur).order_by(models.Operateur.nom, models.Operateur.prenom).filter(
            *conditions).limit(search_limit).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

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
        return exc.HTTPBadRequest(e)


""" Update operateur"""
@view_config(route_name='operateurs', request_method='PUT', renderer='json')
@view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
def operateurs_update_view(request):
    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Operateur).filter(
        models.Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            models.Operateur.__tablename__, id_operateur))

    # Read params operateur
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:

            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Delete operateur"""
@view_config(route_name='operateurs', request_method='DELETE', renderer='json')
@view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
def operateurs_delete_view(request):
    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Operateur).filter(
        models.Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            models.Operateur.__tablename__, id_operateur))

    model.sortie = datetime.utcnow()

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Operateur.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

