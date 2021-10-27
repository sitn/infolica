# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import func

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Operateur
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
from datetime import datetime


@view_config(route_name='operateurs', request_method='GET', renderer='json')
@view_config(route_name='operateurs_s', request_method='GET', renderer='json')
def operateurs_view(request):
    """
    Return all operateurs
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(Operateur).filter(Operateur.sortie == None).all()
    return Utils.serialize_many(query)


@view_config(route_name='operateur_by_id', request_method='GET', renderer='json')
def operateur_by_id_view(request):
    """
    Return operateur by id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    query = request.dbsession.query(Operateur).filter(
        Operateur.id == id).first()
    return Utils.serialize_one(query)


@view_config(route_name='recherche_operateurs', request_method='POST', renderer='json')
@view_config(route_name='recherche_operateurs_s', request_method='POST', renderer='json')
def operateurs_search_view(request):
    """
    Search operateurs
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])
    conditions = Utils.get_search_conditions(Operateur, request.params)

    # Check date_sortie is null
    conditions = [] if not conditions or len(conditions) == 0 else conditions
    conditions.append(Operateur.sortie == None)

    query = request.dbsession.query(Operateur).order_by(Operateur.nom, Operateur.prenom).filter(
        *conditions).limit(search_limit).all()
    return Utils.serialize_many(query)


@view_config(route_name='operateurs', request_method='POST', renderer='json')
@view_config(route_name='operateurs_s', request_method='POST', renderer='json')
def operateurs_new_view(request):
    """
    Add new operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur instance
    model = Utils.set_model_record(Operateur(), request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Operateur.__tablename__))


@view_config(route_name='operateurs', request_method='PUT', renderer='json')
@view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
def operateurs_update_view(request):
    """
    Update operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(Operateur).filter(
        Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            Operateur.__tablename__, id_operateur))

    # Read params operateur
    model = Utils.set_model_record(model, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Operateur.__tablename__))


@view_config(route_name='operateurs', request_method='DELETE', renderer='json')
@view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
def operateurs_delete_view(request):
    """
    Delete operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(Operateur).filter(
        Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            Operateur.__tablename__, id_operateur))

    model.sortie = datetime.utcnow()

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Operateur.__tablename__))
