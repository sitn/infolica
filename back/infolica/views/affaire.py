from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.httpexceptions import HTTPForbidden
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import logging
log = logging.getLogger(__name__)


###########################################################
# AFFAIRE
###########################################################

""" Return all affaires"""
@view_config(route_name='affaires', request_method='GET', renderer='json')
@view_config(route_name='affaires_s', request_method='GET', renderer='json')
def affaires_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        query = request.dbsession.query(models.VAffaire).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Return affaires by id"""
@view_config(route_name='affaire_by_id', request_method='GET', renderer='json')
def affaire_by_id_view(request):
    try:
       # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        id = request.matchdict['id']
        query = request.dbsession.query(models.VAffaire)
        one = query.filter(models.VAffaire.id == id).first()
        return Utils.serialize_one(one)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Search affaires"""
@view_config(route_name='recherche_affaires', request_method='POST', renderer='json')
@view_config(route_name='recherche_affaires_s', request_method='POST', renderer='json')
def affaires_search_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(
            models.VAffaire, request.params)
        query = request.dbsession.query(models.VAffaire).filter(
            *conditions).order_by(models.VAffaire.date_ouverture.desc()).limit(search_limit).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Return all types affaires"""
@view_config(route_name='types_affaires', request_method='GET', renderer='json')
@view_config(route_name='types_affaires_s', request_method='GET', renderer='json')
def types_affaires_view(request):
    try:
        query = request.dbsession.query(models.AffaireType).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Add new affaire"""
@view_config(route_name='affaires', request_method='POST', renderer='json')
def affaires_new_view(request):
    # Get role depending on affaire type
    affaire_type = request.params['type_id'] if 'type_id' in request.params else None
    role = request.registry.settings['editer_affaire_ppe'] if affaire_type == request.registry.settings[
        'affaire_type_ppe_id'] else request.registry.settings['editer_affaire_autre']

    # Check authorization
    if not Utils.has_permission(request, role):
        raise HTTPForbidden()

    model = models.Affaire()
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Update affaire"""
@view_config(route_name='affaires', request_method='PUT', renderer='json')
@view_config(route_name='affaires_s', request_method='PUT', renderer='json')
def affaires_update_view(request):
    # id_affaire
    id_affaire = request.params['id_affaire'] if 'id_affaire' in request.params else None

    # Get the affaire
    record = request.dbsession.query(models.Affaire).filter(
        models.Affaire.id == id_affaire).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))

    # Get role depending on affaire type
    affaire_type = request.params['type_id'] if 'type_id' in request.params else record.type_id
    role = request.registry.settings['editer_affaire_ppe'] if affaire_type == request.registry.settings['affaire_type_ppe_id'] else request.registry.settings['editer_affaire_autre']

    # Check authorization
    if not Utils.has_permission(request, role):
        raise HTTPForbidden()

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


# """ Delete affaire"""
# @view_config(route_name='affaire_by_id', request_method='DELETE', renderer='json')
# def affaires_delete_view(request):
#     # id_affaire
#     id_affaire = request.params['id_affaire'] if 'id_affaire' in request.params else None

#     # Get the affaire
#     record = request.dbsession.query(models.Affaire).filter(
#         models.Affaire.id == id_affaire).first()

#     if not record:
#         raise CustomError(
#             CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))

#     try:
#         with transaction.manager:
#             request.dbsession.delete(record)
#             # Commit transaction
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Affaire.__tablename__))

#     except DBAPIError as e:
#         log.error(e)
#         return Response(db_err_msg, content_type='text/plain', status=500)

