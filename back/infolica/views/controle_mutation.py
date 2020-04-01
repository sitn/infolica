from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.httpexceptions import HTTPForbidden
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
        # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        query = request.dbsession.query(models.ControleMutation).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Return controle_mutation by id"""
@view_config(route_name='controle_mutation_by_id', request_method='GET', renderer='json')
def controles_mutations_by_id_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        # Get controle mutation id
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.ControleMutation).filter(
            models.ControleMutation.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Return controle_mutation by affaire_id"""
@view_config(route_name='controle_mutation_by_affaire_id', request_method='GET', renderer='json')
def controles_mutations_by_affaire_id_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise HTTPForbidden()

        # Get controle mutation id
        affaire_id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.ControleMutation).filter(
            models.ControleMutation.affaire_id == affaire_id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Add new controle_mutation"""
@view_config(route_name='controles_mutations', request_method='POST', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='POST', renderer='json')
def controles_mutations_new_view(request):

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
        raise HTTPForbidden()

    record = models.ControleMutation()
    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ControleMutation.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Update controle_mutation"""
@view_config(route_name='controles_mutations', request_method='PUT', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='PUT', renderer='json')
def controles_mutations_update_view(request):

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
        raise HTTPForbidden()

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

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Delete controle_mutation"""
@view_config(route_name='controles_mutations', request_method='DELETE', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='DELETE', renderer='json')
def controles_mutations_delete_view(request):

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
        raise HTTPForbidden()

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

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
