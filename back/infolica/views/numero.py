from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import and_

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireNumero, Numero, NumeroDiffere, NumeroEtat
from infolica.models.models import NumeroEtatHisto, NumeroType, VNumeros
from infolica.models.models import VNumerosAffaires
from infolica.scripts.utils import Utils

import transaction

import json


""" Return all numeros"""
@view_config(route_name='numeros', request_method='GET', renderer='json')
@view_config(route_name='numeros_s', request_method='GET', renderer='json')
def numeros_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VNumeros).all()
    return Utils.serialize_many(query)


""" Return all types_numeros"""
@view_config(route_name='types_numeros', request_method='GET', renderer='json')
@view_config(route_name='types_numeros_s', request_method='GET', renderer='json')
def types_numeros_view(request):
    query = request.dbsession.query(NumeroType).all()
    return Utils.serialize_many(query)


""" Return all etats_numeros"""
@view_config(route_name='etats_numeros', request_method='GET', renderer='json')
@view_config(route_name='etats_numeros_s', request_method='GET', renderer='json')
def etats_numeros_view(request):
    query = request.dbsession.query(NumeroEtat).all()
    return Utils.serialize_many(query)


""" Return numeros by id"""
@view_config(route_name='numero_by_id', request_method='GET', renderer='json')
def numeros_by_id_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    # Get controle mutation id
    id = request.id = request.matchdict['id']
    query = request.dbsession.query(VNumeros).filter(
        VNumeros.id == id).first()
    return Utils.serialize_one(query)


""" Search numeros"""
@view_config(route_name='recherche_numeros', request_method='POST', renderer='json')
@view_config(route_name='recherche_numeros_s', request_method='POST', renderer='json')
def numeros_search_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])

    params = request.params
    
    matDiff = False
    if 'matDiff' in params: 
        matDiff = True if params['matDiff'] == 'true' else False

    # Set conditions
    conditions = Utils.get_search_conditions(VNumeros, params)

    # filter by conditions
    query = request.dbsession.query(VNumeros).order_by(VNumeros.cadastre,
                                                              VNumeros.numero.desc()).filter(*conditions)
    # if option matDiff selected
    if matDiff:
        query = query.filter(
            and_(
                VNumeros.diff_entree.isnot(None), 
                VNumeros.diff_sortie.is_(None)
                )
            )

    query = query.limit(search_limit).all()
    return Utils.serialize_many(query)


""" Add new numeros"""
@view_config(route_name='numeros', request_method='POST', renderer='json')
@view_config(route_name='numeros_s', request_method='POST', renderer='json')
def numeros_new_view(request, params=None):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params

    # nouveau numero
    record = Numero()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)

    Utils.get_data_save_response(
            Constant.SUCCESS_SAVE.format(Numero.__tablename__)
    )

    return record.id


""" Update numeros"""
@view_config(route_name='numeros', request_method='PUT', renderer='json')
@view_config(route_name='numeros_s', request_method='PUT', renderer='json')
def numeros_update_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # Get numero id
    id = request.params['id'] if 'id' in request.params else None

    # Get numero record
    record = request.dbsession.query(Numero).filter(
        Numero.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Numero.__tablename__, id))

    last_record_etat_id = record.etat_id
    record = Utils.set_model_record(record, request.params)

    if 'etat_id' in request.params:
        if request.params['etat_id'] != last_record_etat_id:
            params = Utils._params(
                numero_id=record.id, numero_etat_id=request.params['etat_id'])
            numeros_etat_histo_new_view(request, params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Numero.__tablename__))


""" Supprimer/abandonner numeros by id"""
@view_config(route_name='numero_by_id', request_method='DELETE', renderer='json')
def numeros_by_id_delete_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # Get numero by id
    id = request.matchdict['id']
    query = request.dbsession.query(Numero).filter(
        Numero.id == id).first()

    if query:
        if query.etat_id == 1:  # projet
            query.etat_id = 3
        elif query.etat_id == 3:  # abandonné
            query.etat_id = 1
        # elif query.etat_id == 2: # vigueur
        #     query.etat_id = 4

###########################################################
# NUMERO ETAT HISTO
###########################################################

""" Add new numero_etat_histo """
@view_config(route_name='numeros_etat_histo', request_method='POST', renderer='json')
@view_config(route_name='numeros_etat_histo_s', request_method='POST', renderer='json')
def numeros_etat_histo_new_view(request, params=None):
    # Check authorization
    settings = request.registry.settings
    if not Utils.has_permission(request, settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params

    # nouveau numero
    record = NumeroEtatHisto()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)

    Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(
        NumeroEtatHisto.__tablename__)
    )
    
    return record.id


###########################################################
# AFFAIRE-NUMERO
###########################################################

""" Return all numeros in affaire"""
@view_config(route_name='affaire_numeros_by_affaire_id', request_method='GET', renderer='json')
def affaire_numeros_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()
    conditions = list()
    affaire_id = request.matchdict["id"]

    # Récupérer les id des numéros de la MO
    settings = request.registry.settings


    numeros_immeubles_type_id = [settings['numero_bf_id'], 
                     settings['numero_ddp_id'], 
                     settings['numero_ppe_id'], 
                     settings['numero_pcop_id']]

    conditions.append(VNumerosAffaires.affaire_id == affaire_id)
    conditions.append(VNumerosAffaires.numero_type_id.in_(numeros_immeubles_type_id))

    if 'affaire_numero_actif' in request.params:
        affaire_numero_actif = request.params['affaire_numero_actif']
        affaire_numero_actif = True if affaire_numero_actif.upper() == 'TRUE' else False
        conditions.append(VNumerosAffaires.affaire_numero_actif == affaire_numero_actif)

    records = request.dbsession.query(VNumerosAffaires).filter(
        *conditions).all()
    return Utils.serialize_many(records)


""" Return all new numeros MO in affaire"""
@view_config(route_name='affaire_new_numeros_MO_by_affaire_id', request_method='GET', renderer='json')
def affaire_new_numeros_mo_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict["id"]

    # Récupérer les id des numéros de la MO
    settings = request.registry.settings

    numeros_mo_type_id = [settings['numero_pfp3_id'], 
                     settings['numero_bat_id'], 
                     settings['numero_pcs_id'], 
                     settings['numero_paux_id'], 
                     settings['numero_pdet_id'], 
                     settings['numero_dp_id']]

    # Contenu de la table VNumerosAffaires avec les numéros de la MO
    query = request.dbsession.query(VNumerosAffaires).filter(
        and_(
            VNumerosAffaires.affaire_id == affaire_id,
            VNumerosAffaires.numero_type_id.in_(numeros_mo_type_id)
        )
    )

    records = query.all()

    cadastres_id = list()
    types_id = list()
    plans_id = list()
    for record in records:
        cadastres_id.append(record.numero_cadastre_id)
        types_id.append(record.numero_type_id)
        plans_id.append(record.numero_plan_id)
    # Retient les valeurs uniques
    cadastres_id = set(cadastres_id)
    types_id = set(types_id)
    plans_id = set(plans_id)
    
    reservations_ranges = list()
    for cadastre_id in cadastres_id:
        for type_id in types_id:
            for plan_id in plans_id:
                records = query.filter(
                    and_(
                        VNumerosAffaires.numero_cadastre_id == cadastre_id,
                        VNumerosAffaires.numero_type_id == type_id,
                        VNumerosAffaires.numero_plan_id == plan_id
                    )
                ).order_by(VNumerosAffaires.numero.asc()).all()

                if len(records) == 0:
                    continue

                numeros = list()
                for record in records:
                    numeros.append(record.numero)

                # Get lists of consecutive numbers [[de, à], [de, à], etc]
                consecutive_diff = [x - numeros[i - 1] for i, x in enumerate(numeros)][1:]
                diff_index_greaterthan1 = list(filter(lambda x: consecutive_diff[x]>1, range(len(consecutive_diff))))
                
                n_diff_idx = len(diff_index_greaterthan1)
                last_diff_idx = 0
                for i, diff_idx in enumerate(diff_index_greaterthan1):
                    reservations_ranges.append({"cadastre_id": cadastre_id, 
                                                "type_id": type_id, 
                                                "plan_id": plan_id, 
                                                "numero_de": numeros[last_diff_idx], 
                                                "numero_a": numeros[diff_idx], 
                                                "cadastre": record.numero_cadastre, 
                                                "numero_type": record.numero_type, 
                                                "nombre": numeros[diff_idx] - numeros[last_diff_idx] + 1 })
                    last_diff_idx = diff_idx + 1

                # Ne pas oublier la dernière série...    
                reservations_ranges.append({"cadastre_id": cadastre_id, 
                                            "type_id": type_id, 
                                            "plan_id": plan_id, 
                                            "numero_de": numeros[last_diff_idx], 
                                            "numero_a": numeros[-1], 
                                            "cadastre": record.numero_cadastre, 
                                            "numero_type": record.numero_type,
                                            "nombre": numeros[-1] - numeros[last_diff_idx] + 1 })

    return json.loads(json.dumps(reservations_ranges))


"""Update numeros_affaires"""
@view_config(route_name='affaire_numeros', request_method='PUT', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='PUT', renderer='json')
def affaire_numero_update_view(request):
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    affnum_id = request.params["id"] if "id" in request.params else None

    record = request.dbsession.query(AffaireNumero).filter(AffaireNumero.id == affnum_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(AffaireNumero.__tablename__, affnum_id))

    record = Utils.set_model_record(record, request.params)

    return 


""" Add new affaire-numero """
@view_config(route_name='affaire_numeros', request_method='POST', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='POST', renderer='json')
def affaire_numero_new_view(request, params=None):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params
    # nouveau affaire_numero
    record = AffaireNumero()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)
    
    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(AffaireNumero.__tablename__))


###########################################################
# NUMERO- AFFAIRE
###########################################################

""" Return all affaires touching one numero """
@view_config(route_name='numero_affaires_by_numero_id', request_method='GET', renderer='json')
def numeros_affaire_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    numero_id = request.matchdict['id']

    query = request.dbsession.query(VNumerosAffaires).filter(
        VNumerosAffaires.numero_id == numero_id).all()

    if not query:
        raise CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            VNumerosAffaires.__tablename__, numero_id)

    return Utils.serialize_many(query)


###########################################################
# NUMERO DIFFERE
###########################################################

""" Add new numero_differe """
@view_config(route_name='numeros_differes', request_method='POST', renderer='json')
@view_config(route_name='numeros_differes_s', request_method='POST', renderer='json')
def numero_differe_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # nouveau numero_differe
    record = NumeroDiffere()
    record = Utils.set_model_record(record, request.params)

    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroDiffere.__tablename__))


""" Update numero_differe """
@view_config(route_name='numeros_differes', request_method='PUT', renderer='json')
@view_config(route_name='numeros_differes_s', request_method='PUT', renderer='json')
def numero_differe_update_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    numdiff_id = request.params["id"] if "id" in request.params else None

    # update numero_differe
    record = request.dbsession.query(NumeroDiffere).filter(NumeroDiffere.id == numdiff_id).first()
    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroDiffere.__tablename__))
