# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import ReservationNumerosMO, VReservationNumerosMO, Plan, Affaire
from infolica.scripts.utils import Utils

from sqlalchemy import and_, or_, func

import os
import json
from datetime import datetime



@view_config(route_name='reservation_numeros_mo_by_affaire_id', request_method='GET', renderer='json')
def reservation_numeros_mo_by_affaire_id_view(request):
    """
    Return all reservations_numeros_mo by affaire_id
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']
    query = request.dbsession.query(VReservationNumerosMO).filter(VReservationNumerosMO.affaire_id == affaire_id).all()
    return Utils.serialize_many(query)



@view_config(route_name='reservation_numeros_mo', request_method='POST', renderer='json')
def reservation_numeros_mo_new_view(request):
    """
    Add new reservation_numeros_mo
    """

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    cadastre_id = request.params["cadastre_id"]
    type_id = request.params["type_id"]

    # get max number in db by number type, cadastre and plan if necessary
    query = request.dbsession.query(func.max(ReservationNumerosMO.numero_a)).filter(and_(
        ReservationNumerosMO.cadastre_id == cadastre_id,
        ReservationNumerosMO.type_id == type_id
    ))

    if "plan_id" in request.params:
        query = query.filter(ReservationNumerosMO.plan_id == request.params["plan_id"])

    max_reservation = 0 if query.first()[0] is None else query.first()[0]

    # get params into mutable dict
    params = {}
    for key in request.params:
        params[key] = request.params[key]

    # Adjust numbers
    params['numero_de'] = max_reservation + int(params['numero_de'])
    params['numero_a'] = max_reservation + int(params['numero_a'])

    # Save in database
    model = ReservationNumerosMO()
    model = Utils.set_model_record(model, params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(ReservationNumerosMO.__tablename__))
