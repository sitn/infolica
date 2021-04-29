# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import ReservationNumerosMO, VReservationNumerosMO, Plan, Affaire
from infolica.models.models import VNextNumeroMOAvilable
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

    searchLimit = request.registry.settings['search_limit']
    affaire_id = request.matchdict['id']
    cadastre_id = request.params["cadastre_id"] if "cadastre_id" in request.params else None
    startDate = request.params["startDate"] if "startDate" in request.params else None
    endDate = request.params["endDate"] if "endDate" in request.params else None
    
    query = request.dbsession.query(VReservationNumerosMO).filter(VReservationNumerosMO.affaire_id == affaire_id).order_by(VReservationNumerosMO.id.desc())

    if not cadastre_id is None:
        query = query.filter(VReservationNumerosMO.cadastre_id == cadastre_id)
    
    if not startDate is None:
        query = query.filter(VReservationNumerosMO.date >= startDate)
    
    if not endDate is None:
        query = query.filter(VReservationNumerosMO.date <= endDate)
    
    if request.params == {} or (cadastre_id is None and startDate is None):
        query = query.limit(searchLimit)
    
    query = query.all()

    return Utils.serialize_many(query)



@view_config(route_name='reservation_numeros_mo', request_method='POST', renderer='json')
def reservation_numeros_mo_new_view(request):
    """
    Add new reservation_numeros_mo
    """

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['numero_mo_edition']):
        raise exc.HTTPForbidden()

    # get cadastres jumeaux
    cadastres_ChauxDeFonds_Eplatures_id = [int(i) for i in request.registry.settings['cadastres_ChauxDeFonds_Eplatures_id'].split(",")]
    cadastres_BrotPlamboz_Plamboz_id = [int(i) for i in request.registry.settings['cadastres_BrotPlamboz_Plamboz_id'].split(",")]
    cadastres_Neuchatel_Coudre_id = [int(i) for i in request.registry.settings['cadastres_Neuchatel_Coudre_id'].split(",")]
    cadastres_Sauge_StAubin_id = [int(i) for i in request.registry.settings['cadastres_Sauge_StAubin_id'].split(",")]
    
    # get request params
    cadastre_id = int(request.params["cadastre_id"])
    type_id = int(request.params["type_id"])
    plan_id = request.params["plan_id"] if "plan_id" in request.params else None

    # Corriger la liste des cadastres où la réservation de numéros se fait sur deux cadastres
    if cadastre_id in cadastres_ChauxDeFonds_Eplatures_id:
        # Cadastre de la Chaux-de-Fonds et des Eplatures
        max_reservation = max(
            Utils.last_number_mo(request, cadastres_ChauxDeFonds_Eplatures_id[0], type_id, plan_id),
            Utils.last_number_mo(request, cadastres_ChauxDeFonds_Eplatures_id[1], type_id, plan_id)
        )
    elif cadastre_id in cadastres_BrotPlamboz_Plamboz_id:
        # Cadastre de Brot-Plamboz et Plamboz
        max_reservation = max(
            Utils.last_number_mo(request, cadastres_BrotPlamboz_Plamboz_id[0], type_id, plan_id),
            Utils.last_number_mo(request, cadastres_BrotPlamboz_Plamboz_id[1], type_id, plan_id)
        )
    elif cadastre_id in cadastres_Neuchatel_Coudre_id:
        # Cadastre de Neuchâtel et de la Coudre
        max_reservation = max(
            Utils.last_number_mo(request, cadastres_Neuchatel_Coudre_id[0], type_id, plan_id),
            Utils.last_number_mo(request, cadastres_Neuchatel_Coudre_id[1], type_id, plan_id)
        )
    elif cadastre_id in cadastres_Sauge_StAubin_id:
        # Cadastre de Sauge et de Saint-Aubin
        max_reservation = max(
            Utils.last_number_mo(request, cadastres_Sauge_StAubin_id[0], type_id, plan_id),
            Utils.last_number_mo(request, cadastres_Sauge_StAubin_id[1], type_id, plan_id)
        )
    else:
        max_reservation = Utils.last_number_mo(request, cadastre_id, type_id, plan_id)

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


def savePointMO(request, affaire_id, cadastre_id, numero_type, n_numeros, etat_id):
    settings = request.registry.settings
    cadastres_ChauxDeFonds_Eplatures_id = settings['cadastres_ChauxDeFonds_Eplatures_id'].split(",")
    cadastres_ChauxDeFonds_Eplatures_id = [
        int(cadastres_ChauxDeFonds_Eplatures_id[0]),
        int(cadastres_ChauxDeFonds_Eplatures_id[1])
    ]
    cadastres_BrotPlamboz_Plamboz_id = settings['cadastres_BrotPlamboz_Plamboz_id'].split(",")
    cadastres_BrotPlamboz_Plamboz_id = [
        int(cadastres_BrotPlamboz_Plamboz_id[0]),
        int(cadastres_BrotPlamboz_Plamboz_id[1])
    ]
    cadastres_Neuchatel_Coudre_id = settings['cadastres_Neuchatel_Coudre_id'].split(",")
    cadastres_Neuchatel_Coudre_id = [
        int(cadastres_Neuchatel_Coudre_id[0]),
        int(cadastres_Neuchatel_Coudre_id[1])
    ]
    cadastres_Sauge_StAubin_id = settings['cadastres_Sauge_StAubin_id'].split(",")
    cadastres_Sauge_StAubin_id = [int(cadastres_Sauge_StAubin_id[0]), int(cadastres_Sauge_StAubin_id[1])]

    # Corriger la liste des cadastres où la réservation de numéros se fait sur deux cadastres
    if cadastre_id == cadastres_ChauxDeFonds_Eplatures_id[0] or cadastre_id == cadastres_ChauxDeFonds_Eplatures_id[1]:
        # Cadastre de la Chaux-de-Fonds et des Eplatures
        ln = max(
            Utils.last_number(request, cadastres_ChauxDeFonds_Eplatures_id[0], [numero_type]),
            Utils.last_number(request, cadastres_ChauxDeFonds_Eplatures_id[1], [numero_type])
        )
    elif cadastre_id == cadastres_BrotPlamboz_Plamboz_id[0] or cadastre_id == cadastres_BrotPlamboz_Plamboz_id[1]:
        # Cadastre de Brot-Plamboz et Plamboz
        ln = max(
            Utils.last_number(request, cadastres_BrotPlamboz_Plamboz_id[0], [numero_type]),
            Utils.last_number(request, cadastres_BrotPlamboz_Plamboz_id[1], [numero_type])
        )
    elif cadastre_id == cadastres_Neuchatel_Coudre_id[0] or cadastre_id == cadastres_Neuchatel_Coudre_id[1]:
        # Cadastre de Neuchâtel et de la Coudre
        ln = max(
            Utils.last_number(request, cadastres_Neuchatel_Coudre_id[0], [numero_type]),
            Utils.last_number(request, cadastres_Neuchatel_Coudre_id[1], [numero_type])
        )
    elif cadastre_id == cadastres_Sauge_StAubin_id[0] or cadastre_id == cadastres_Sauge_StAubin_id[1]:
        # Cadastre de Sauge et de Saint-Aubin
        ln = max(
            Utils.last_number(request, cadastres_Sauge_StAubin_id[0], [numero_type]),
            Utils.last_number(request, cadastres_Sauge_StAubin_id[1], [numero_type])
        )
    else:
        ln = Utils.last_number(request, cadastre_id, [numero_type])

    for i in range(n_numeros):
        # enregistrer un nouveau numéro
        params = Utils._params(
            cadastre_id=cadastre_id, type_id=numero_type, etat_id=etat_id, numero=ln + i+1)
        numero_id = numeros_new_view(request, params)
        # enregistrer le lien affaire-numéro
        params = Utils._params(
            affaire_id=affaire_id, numero_id=numero_id, actif=True, type_id=2)
        affaire_numero_new_view(request, params)



@view_config(route_name='numero_mo_next', request_method='GET', renderer='json')
def numero_mo_next_view(request):
    """
    Return all next available numero MO par cadastre, type et plan
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    cadastre_id = request.params['cadastre_id'] if 'cadastre_id' in request.params else None
    type_id = request.params['type_id'] if 'type_id' in request.params else None
    plan = request.params['plan'] if 'plan' in request.params else None

    query = request.dbsession.query(VNextNumeroMOAvilable)
    if cadastre_id:
        query = query.filter(VNextNumeroMOAvilable.cadastre_id == cadastre_id)
    if type_id:
        query = query.filter(VNextNumeroMOAvilable.numero_type_id == type_id)
    if plan:
        query = query.filter(VNextNumeroMOAvilable.plan == plan)
    
    query = query.all()
        
    return Utils.serialize_many(query)
