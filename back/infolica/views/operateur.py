from datetime import datetime
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

""" Return all operateurs"""
@view_config(route_name='operateurs', request_method='GET', renderer='json')
@view_config(route_name='operateurs_s', request_method='GET', renderer='json')
def operateurs_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(models.Operateur).all()
    return Utils.serialize_many(query)
    

""" Return operateur by id"""
@view_config(route_name='operateur_by_id', request_method='GET', renderer='json')
def operateur_by_id_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    query = request.dbsession.query(models.Operateur).filter(
        models.Operateur.id == id).first()
    return Utils.serialize_one(query)


""" Search operateurs"""
@view_config(route_name='recherche_operateurs', request_method='POST', renderer='json')
@view_config(route_name='recherche_operateurs_s', request_method='POST', renderer='json')
def operateurs_search_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])
    conditions = Utils.get_search_conditions(models.Operateur, request.params)

    # Check date_sortie is null
    conditions = [] if not conditions or len(conditions) == 0 else conditions
    conditions.append(models.Operateur.sortie == None)

    query = request.dbsession.query(models.Operateur).order_by(models.Operateur.nom, models.Operateur.prenom).filter(
        *conditions).limit(search_limit).all()
    return Utils.serialize_many(query)

""" Add new operateur"""
@view_config(route_name='operateurs', request_method='POST', renderer='json')
@view_config(route_name='operateurs_s', request_method='POST', renderer='json')
def operateurs_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur instance
    model = Utils.set_model_record(models.Operateur(), request.params)

    with transaction.manager:
        request.dbsession.add(model)
        request.dbsession.flush()
        print("model.id = ", model.id)
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))


""" Update operateur"""
@view_config(route_name='operateurs', request_method='PUT', renderer='json')
@view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
def operateurs_update_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

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

    with transaction.manager:

        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))

""" Delete operateur"""
@view_config(route_name='operateurs', request_method='DELETE', renderer='json')
@view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
def operateurs_delete_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(models.Operateur).filter(
        models.Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            models.Operateur.__tablename__, id_operateur))

    model.sortie = datetime.utcnow()

    with transaction.manager:
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Operateur.__tablename__))

