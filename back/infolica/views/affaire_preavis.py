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
# PREAVIS AFFAIRE
###########################################################

""" GET preavis type"""
@view_config(route_name='preavis_type', request_method='GET', renderer='json')
@view_config(route_name='preavis_type_s', request_method='GET', renderer='json')
def preavis_type_view(request):
    try:
        records = request.dbsession.query(models.PreavisType).all()
        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" GET preavis affaire"""
@view_config(route_name='affaire_preavis_by_affaire_id', request_method='GET', renderer='json')
def affaire_preavis_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise HTTPForbidden()

    affaire_id = request.matchdict['id']

    try:
        records = request.dbsession.query(models.VAffairesPreavis)\
            .filter(models.VAffairesPreavis.affaire_id == affaire_id).all()

        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" POST preavis affaire"""
@view_config(route_name='preavis', request_method='POST', renderer='json')
@view_config(route_name='preavis_s', request_method='POST', renderer='json')
def preavis_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['demander_preavis']):
        raise HTTPForbidden()

    model = models.Preavis()
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" UPDATE preavis affaire"""
@view_config(route_name='preavis', request_method='PUT', renderer='json')
@view_config(route_name='preavis_s', request_method='PUT', renderer='json')
def preavis_update_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['demander_preavis']):
        raise HTTPForbidden()

    preavis_id = request.params['id'] if 'id' in request.params else None

    record = request.dbsession.query(models.Preavis).filter(
        models.Preavis.id == preavis_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" DELETE preavis affaire"""
@view_config(route_name='preavis_by_id', request_method='DELETE', renderer='json')
def preavis_delete_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['demander_preavis']):
        raise HTTPForbidden()

    preavis_id = request.matchdict['id']

    record = request.dbsession.query(models.Preavis).filter(
        models.Preavis.id == preavis_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

    try:
        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)



# # Remarques Préavis

# """ GET affaire preavis remarques"""
# @view_config(route_name='preavis_by_affaire_id', request_method='GET', renderer='json')
# def affaire_preavis_remarques_view(request):
#     affaire_id = request.matchdict['id']

#     try:
#         records = request.dbsession.query(models.VAffairesPreavis)\
#             .filter(models.VAffairesPreavis.affaire_id == affaire_id).all()

#         return Utils.serialize_many(records)

#     except DBAPIError as e:
#         log.error(e)
#         return exc.HTTPBadRequest(e)


# """ POST preavis affaire"""
# @view_config(route_name='preavis', request_method='POST', renderer='json')
# @view_config(route_name='preavis_s', request_method='POST', renderer='json')
# def preavis_new_view(request):

#     model = models.Preavis()
#     model = Utils.set_model_record(model, request.params)

#     try:
#         with transaction.manager:
#             request.dbsession.add(model)
#             # Commit transaction
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

#     except DBAPIError as e:
#         log.error(e)
#         return exc.HTTPBadRequest(e)


# """ UPDATE preavis affaire"""
# @view_config(route_name='preavis', request_method='PUT', renderer='json')
# @view_config(route_name='preavis_s', request_method='PUT', renderer='json')
# def preavis_update_view(request):
#     preavis_id = request.params['id'] if 'id' in request.params else None
#     record = request.dbsession.query(models.Preavis).filter(
#         models.Preavis.id == preavis_id).first()

#     if not record:
#         raise CustomError(
#             CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

#     record = Utils.set_model_record(record, request.params)

#     try:
#         with transaction.manager:
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

#     except DBAPIError as e:
#         log.error(e)
#         return exc.HTTPBadRequest(e)


# """ DELETE preavis affaire"""
# @view_config(route_name='preavis_by_id', request_method='DELETE', renderer='json')
# def preavis_delete_view(request):
#     preavis_id = request.matchdict['id']

#     record = request.dbsession.query(models.Preavis).filter(
#         models.Preavis.id == preavis_id).first()

#     if not record:
#         raise CustomError(
#             CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

#     try:
#         with transaction.manager:
#             request.dbsession.delete(record)
#             # Commit transaction
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Preavis.__tablename__))

#     except DBAPIError as e:
#         log.error(e)
#         return exc.HTTPBadRequest(e)
