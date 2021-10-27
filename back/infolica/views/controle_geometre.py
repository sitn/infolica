# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models import Constant
from infolica.models.models import ControleGeometre
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected


@view_config(route_name='controle_geometre_by_affaire_id', request_method='GET', renderer='json')
def controle_geometre_by_affaire_id_view(request):
    """
    Return controle_geometre by affaire_id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    # Get controle mutation id
    affaire_id = request.matchdict['id']
    query = request.dbsession.query(ControleGeometre).filter(
        ControleGeometre.affaire_id == affaire_id).first()

    if query is None:
        return None

    return Utils.serialize_one(query)


@view_config(route_name='controle_geometre', request_method='POST', renderer='json')
@view_config(route_name='controle_geometre_s', request_method='POST', renderer='json')
def controle_geometre_new_view(request):
    """
    Add new controle_geometre
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_controle_geometre_edition']):
        raise exc.HTTPForbidden()

    Utils.addNewRecord(request, ControleGeometre)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(ControleGeometre.__tablename__))


@view_config(route_name='controle_geometre', request_method='PUT', renderer='json')
@view_config(route_name='controle_geometre_s', request_method='PUT', renderer='json')
def controle_geometre_update_view(request):
    """
    Update controle_geometre
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_controle_geometre_edition']):
        raise exc.HTTPForbidden()

    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None

    # Get controle mutation record
    record = request.dbsession.query(ControleGeometre).filter(
        ControleGeometre.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(ControleGeometre.__tablename__, id))

    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(ControleGeometre.__tablename__))

