# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import NotesMAJ, Operateur
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
from datetime import datetime


@view_config(route_name='notes_maj', request_method='GET', renderer='json')
def notes_maj_view(request):
    """
    Return all notes_maj
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()
    
    lastNoteMaj_id = request.params ["lastNoteMaj_id"] if "lastNoteMaj_id" in request.params else None

    query = request.dbsession.query(NotesMAJ)
    
    if not lastNoteMaj_id is None:
        if lastNoteMaj_id == 'null':
            lastNoteMaj_id = 0
        query = query.filter(NotesMAJ.id > lastNoteMaj_id)

    query = query.order_by(NotesMAJ.id.desc()).all()

    return Utils.serialize_many(query)


@view_config(route_name='version', request_method='GET', renderer='json')
def version_view(request):
    """
    Return version
    """
    model_version = request.dbsession.query(NotesMAJ).order_by(NotesMAJ.id.desc()).first()
    model_delai = request.dbsession.query(NotesMAJ).order_by(NotesMAJ.delai.desc()).first()
    model_lastId = request.dbsession.query(NotesMAJ).order_by(NotesMAJ.id.desc()).first()

    now = datetime.now()

    version = {
        'version': model_version.version,
        'isNew': datetime.combine(model_delai.delai, datetime.min.time()) >= now,
        'lastId': model_lastId.id
    }

    return version


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


@view_config(route_name='operateur_notes_maj', request_method='PUT', renderer='json')
def operateur_notes_maj_update_view(request):
    """
    Update last seen notes_maj in operateur
    """
    # Check authorization
    if not check_connected(request):
        raise exc.HTTPForbidden()

    # Get operateur_id
    operateur_id = request.params['operateur_id'] if 'operateur_id' in request.params else None
    last_notes_maj_id = request.params['last_notes_maj_id'] if 'last_notes_maj_id' in request.params else None

    model = request.dbsession.query(Operateur).filter(Operateur.id == operateur_id).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(Operateur.__tablename__, operateur_id))

    # Read params operateur
    model.last_notemaj_id = last_notes_maj_id

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Operateur.__tablename__))