# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Affaire_tele, VAffaire_tele, Etape_tele, SuiviAffaire_tele, VSuiviAffaire_tele, AffaireType_tele
from infolica.scripts.utils import Utils


# AFFAIRE TYPE

@view_config(route_name='affaire_type_tele', request_method='GET', renderer='json')
def affaire_type_tele_view(request):
    """
    Return all affaire_type_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(AffaireType_tele).order_by(AffaireType_tele.id.asc()).all()
    return Utils.serialize_many(query)


# AFFAIRE ETAPE

@view_config(route_name='affaire_etape_tele', request_method='GET', renderer='json')
def affaire_etape_tele_view(request):
    """
    Return all affaire_type_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(Etape_tele).order_by(Etape_tele.ordre.asc()).all()
    return Utils.serialize_many(query)


# SUIVI AFFAIRE


@view_config(route_name='suivi_affaire_tele', request_method='GET', renderer='json')
def suivi_affaire_tele_view(request):
    """
    Return all suivi_affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VSuiviAffaire_tele)

    affaire_id = request.params["affaire_id"] if "affaire_id" in request.params else None
    if affaire_id:
        query = query.filter(VSuiviAffaire_tele.affaire_id == affaire_id)

    query = query.all()
    return Utils.serialize_many(query)


@view_config(route_name='suivi_affaire_tele', request_method='POST', renderer='json')
def suivi_affaire_tele_new_view(request):
    """
    Add new suivi_affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    record = SuiviAffaire_tele()
    record = Utils.set_model_record(record, request.params)

    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(SuiviAffaire_tele.__tablename__))


@view_config(route_name='suivi_affaire_tele', request_method='PUT', renderer='json')
def suivi_affaire_tele_update_view(request):
    """
    Update suivi_affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    record_id = request.params["id"] if "id" in request.params else None

    record = request.dbsession.query(SuiviAffaire_tele).filter(SuiviAffaire_tele.id == record_id).first()
    
    if not record:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(SuiviAffaire_tele.__tablename__, record_id))
    
    record = Utils.set_model_record(record, request.params)
    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(SuiviAffaire_tele.__tablename__))


# AFFAIRE

@view_config(route_name='affaire_tele', request_method='GET', renderer='json')
def affaire_tele_view(request):
    """
    Return all affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VAffaire_tele).filter(VAffaire_tele.datetime_cloture == None).order_by(VAffaire_tele.affaire_id.desc()).all()
    return Utils.serialize_many(query)


@view_config(route_name='affaire_tele', request_method='POST', renderer='json')
def affaire_tele_new_view(request):
    """
    Add new affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    record = Affaire_tele()
    record = Utils.set_model_record(record, request.params)

    request.dbsession.add(record)
    request.dbsession.flush()

    return record.id


@view_config(route_name='affaire_tele', request_method='PUT', renderer='json')
def affaire_tele_update_view(request):
    """
    Update affaire_tele
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    record_id = request.params["id"] if "id" in request.params else None

    record = request.dbsession.query(Affaire_tele).filter(Affaire_tele.id == record_id).first()
    
    if not record:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(Affaire_tele.__tablename__, record_id))
    
    record = Utils.set_model_record(record, request.params)
    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Affaire_tele.__tablename__))
