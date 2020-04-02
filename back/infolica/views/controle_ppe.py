from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from ..exceptions.custom_error import CustomError
from .. import models


""" Return all controles_ppe"""
@view_config(route_name='controles_ppe', request_method='GET', renderer='json')
@view_config(route_name='controles_ppe_s', request_method='GET', renderer='json')
def controles_ppe_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        query = request.dbsession.query(models.ControlePPE).all()
        return Utils.serialize_many(query)

    except Exception as e:
        raise e


""" Return controles_ppe by id"""
@view_config(route_name='controle_ppe_by_id', request_method='GET', renderer='json')
def controles_ppe_by_id_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        # Get controle mutation id
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.ControlePPE).filter(
            models.ControlePPE.id == id).first()
        return Utils.serialize_one(query)

    except Exception as e:
        raise e


""" Return controles_ppe by affaire_id"""
@view_config(route_name='controle_ppe_by_affaire_id', request_method='GET', renderer='json')
def controles_ppe_by_affaire_id_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        # Get controle mutation id
        affaire_id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.ControlePPE).filter(
            models.ControlePPE.affaire_id == affaire_id).first()
        return Utils.serialize_one(query)

    except Exception as e:
        raise e


""" Add new controles_ppe"""
@view_config(route_name='controles_ppe', request_method='POST', renderer='json')
@view_config(route_name='controles_ppe_s', request_method='POST', renderer='json')
def controles_ppe_new_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
            raise exc.HTTPForbidden()

        record = models.ControlePPE()
        record = Utils.set_model_record(record, request.params)

        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ControlePPE.__tablename__))

    except Exception as e:
        raise e


""" Update controles_ppe"""
@view_config(route_name='controles_ppe', request_method='PUT', renderer='json')
@view_config(route_name='controles_ppe_s', request_method='PUT', renderer='json')
def controles_ppe_update_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
            raise exc.HTTPForbidden()

        # Get controle mutation id
        id = request.params['id'] if 'id' in request.params else None

        # Get controle mutation record
        record = request.dbsession.query(models.ControlePPE).filter(
            models.ControlePPE.id == id).first()

        if not record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.ControlePPE.__tablename__, id))

        record = Utils.set_model_record(record, request.params)

        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ControlePPE.__tablename__))

    except Exception as e:
        raise e

""" Delete controles_ppe"""
@view_config(route_name='controles_ppe', request_method='DELETE', renderer='json')
@view_config(route_name='controles_ppe_s', request_method='DELETE', renderer='json')
def controles_ppe_delete_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_controle_edition']):
            raise exc.HTTPForbidden()

        # Get controle mutation id
        id = request.params['id'] if 'id' in request.params else None

        # Get controle mutation record
        record = request.dbsession.query(models.ControlePPE).filter(
            models.ControlePPE.id == id).first()

        if not record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.ControlePPE.__tablename__, id))

        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.ControlePPE.__tablename__))

    except Exception as e:
        raise e
