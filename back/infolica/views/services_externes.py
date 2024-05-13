# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Cadastre, Service
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
from sqlalchemy import or_
from datetime import datetime

###########################################################
# SERVICES EXTERNES
###########################################################


@view_config(route_name='service_by_id', request_method='GET', renderer='json')
def service_by_id_view(request):
    """
    GET service by id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    service_id = request.matchdict['id']

    record = request.dbsession.query(Service).filter(
        Service.id == service_id
    ).first()

    return Utils.serialize_one(record)


@view_config(route_name='services', request_method='GET', renderer='json')
@view_config(route_name='services_s', request_method='GET', renderer='json')
def services_view(request):
    """
    GET services
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    now = datetime.now()

    cadastre_id = request.params['cadastre_id'] if 'cadastre_id' in request.params else None

    records = request.dbsession.query(Service).filter(
        Service.service_principal == True,
        or_(
            Service.date_sortie == None,
            Service.date_sortie > now,
        )
    )

    if cadastre_id is not None:
        cadastre = request.dbsession.query(Cadastre).filter(Cadastre.id == cadastre_id).first()

        if cadastre.service_urbanisme_id is not None:
            records = records.union(request.dbsession.query(Service).filter(Service.id == cadastre.service_urbanisme_id))

    records = records.order_by(Service.ordre.asc()).all()

    return Utils.serialize_many(records)


@view_config(route_name='services', request_method='POST', renderer='json')
@view_config(route_name='services_s', request_method='POST', renderer='json')
def services_new_view(request):
    """
    Add preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    model = Service()
    model = Utils.set_model_record(model, request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Service.__tablename__))


@view_config(route_name='services', request_method='PUT', renderer='json')
@view_config(route_name='services_s', request_method='PUT', renderer='json')
def services_update_view(request):
    """
    UPDATE service
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    service_id = request.params['id'] if 'id' in request.params else None
    record = request.dbsession.query(Service).filter(
        Service.id == service_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Service.__tablename__, service_id))

    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Service.__tablename__))

