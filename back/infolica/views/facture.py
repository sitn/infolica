from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from ..exceptions.custom_error import CustomError
from .. import models


###########################################################
# FACTURE
###########################################################

""" Return all factures"""
@view_config(route_name='factures', request_method='GET', renderer='json')
@view_config(route_name='factures_s', request_method='GET', renderer='json')
def factures_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        query = request.dbsession.query(models.Facture).all()
        return Utils.serialize_many(query)
    except Exception as e:
        raise e


""" Return all factures in affaire"""
@view_config(route_name='affaires_factures_by_affaire_id', request_method='GET', renderer='json')
def affaires_factures_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        affaire_id = request.matchdict["id"]

        query = request.dbsession.query(models.Facture)\
            .filter(models.Facture.affaire_id == affaire_id).all()
        return Utils.serialize_many(query)
    except Exception as e:
        raise e


""" Add new facture"""
@view_config(route_name='factures', request_method='POST', renderer='json')
@view_config(route_name='factures_s', request_method='POST', renderer='json')
def factures_new_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
            raise exc.HTTPForbidden()

        model = models.Facture()
        model = Utils.set_model_record(model, request.params)

        with transaction.manager:
            request.dbsession.add(model)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Facture.__tablename__))

    except Exception as e:
        raise e


""" Update facture"""
@view_config(route_name='factures', request_method='PUT', renderer='json')
@view_config(route_name='factures_s', request_method='PUT', renderer='json')
def factures_update_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
            raise exc.HTTPForbidden()

        # id_facture
        id_facture = None

        if 'id' in request.params:
            id_facture = request.params['id']

        # Get the facture
        facture_record = request.dbsession.query(models.Facture).filter(
            models.Facture.id == id_facture).first()

        if not facture_record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id_facture))

        facture_record = Utils.set_model_record(facture_record, request.params)

        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Facture.__tablename__))

    except Exception as e:
        raise e

""" Delete facture"""
@view_config(route_name='factures', request_method='DELETE', renderer='json')
@view_config(route_name='factures_s', request_method='DELETE', renderer='json')
def factures_delete_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
            raise exc.HTTPForbidden()

        id = request.params['id'] if 'id' in request.params else None

        facture = request.dbsession.query(models.Facture).filter(models.Facture.id == id).first()

        if not facture:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id))

        with transaction.manager:
            request.dbsession.delete(facture)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Facture.__tablename__))

    except Exception as e:
        raise e


