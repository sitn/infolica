# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import NotesMAJ
from infolica.scripts.utils import Utils



@view_config(route_name='notes_maj', request_method='GET', renderer='json')
def notes_maj_view(request):
    """
    Return all notes_maj
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(NotesMAJ).all()
    return Utils.serialize_many(query)


@view_config(route_name='notes_maj', request_method='POST', renderer='json')
def notes_maj_new_view(request):
    """
    Add new notes_maj
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur instance
    model = Utils.set_model_record(NotesMAJ(), request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NotesMAJ.__tablename__))


@view_config(route_name='notes_maj', request_method='PUT', renderer='json')
def notes_maj_update_view(request):
    """
    Update notes_maj
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    notes_maj_id = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(NotesMAJ).filter(
        NotesMAJ.id == notes_maj_id).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            NotesMAJ.__tablename__, notes_maj_id))

    # Read params operateur
    model = Utils.set_model_record(model, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NotesMAJ.__tablename__))


@view_config(route_name='notes_maj', request_method='DELETE', renderer='json')
def notes_maj_delete_view(request):
    """
    Delete notes_maj
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    notes_maj_id = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(NotesMAJ).filter(
        NotesMAJ.id == notes_maj_id).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            NotesMAJ.__tablename__, notes_maj_id))

    request.dbsession.delete(model)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(NotesMAJ.__tablename__))
