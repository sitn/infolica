# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import and_, Integer, func
from sqlalchemy.dialects.postgresql import ARRAY

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireNumero, Numero, NumeroDiffere, NumeroEtat
from infolica.models.models import NumeroEtatHisto, NumeroType, VNumeros
from infolica.models.models import VNumerosAffaires, Affaire, Facture
from infolica.scripts.utils import Utils

from datetime import datetime


@view_config(route_name='numeros', request_method='GET', renderer='json')
@view_config(route_name='numeros_s', request_method='GET', renderer='json')
def numeros_view(request):
    """
    Return all numeros
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    numero = int(request.params['numero']) if 'numero' in request.params else None
    cadastre_id = [int(a) for a in request.params['cadastre_id'].split(",")] if 'cadastre_id' in request.params else None
    type_id = [int(a) for a in request.params['type_id'].split(",")] if 'type_id' in request.params else None
    etat_id = [int(a) for a in request.params['etat_id'].split(",")] if 'etat_id' in request.params else None

    query = request.dbsession.query(VNumeros)
    
    if numero:
        query = query.filter(VNumeros.numero == numero)
    if cadastre_id:
        query = query.filter(VNumeros.cadastre_id.in_(cadastre_id))
    if type_id:
        query = query.filter(VNumeros.type_numero_id.in_(type_id))
    if etat_id:
        query = query.filter(VNumeros.etat_id.in_(etat_id))

    query = query.order_by(VNumeros.numero.asc()).all()

    return Utils.serialize_many(query)


@view_config(route_name='types_numeros', request_method='GET', renderer='json')
@view_config(route_name='types_numeros_s', request_method='GET', renderer='json')
def types_numeros_view(request):
    """
    Return all types_numeros
    """
    immeule_thr = request.registry.settings['numero_type_immeuble_thr']
    query = request.dbsession.query(NumeroType).filter(NumeroType.ordre < immeule_thr).order_by(NumeroType.ordre.asc()).all()
    return Utils.serialize_many(query)


@view_config(route_name='types_numeros_mo', request_method='GET', renderer='json')
def types_numeros_mo_view(request):
    """
    Return all types_numeros
    """
    immeule_thr = request.registry.settings['numero_type_immeuble_thr']
    query = request.dbsession.query(NumeroType).filter(NumeroType.ordre >= immeule_thr).order_by(NumeroType.ordre.asc()).all()
    return Utils.serialize_many(query)


@view_config(route_name='etats_numeros', request_method='GET', renderer='json')
@view_config(route_name='etats_numeros_s', request_method='GET', renderer='json')
def etats_numeros_view(request):
    """
    Return all etats_numeros
    """
    id_artefact = request.registry.settings['numero_artefact_id']
    query = request.dbsession.query(NumeroEtat).filter(NumeroEtat.id != id_artefact).all()
    return Utils.serialize_many(query)


@view_config(route_name='numero_by_id', request_method='GET', renderer='json')
def numeros_by_id_view(request):
    """
    Return numeros by id
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    # Get controle mutation id
    id = request.id = request.matchdict['id']
    query = request.dbsession.query(VNumeros).filter(
        VNumeros.id == id).first()
    return Utils.serialize_one(query)


@view_config(route_name='recherche_numeros', request_method='POST', renderer='json')
@view_config(route_name='recherche_numeros_s', request_method='POST', renderer='json')
def numeros_search_view(request):
    """
    Search numeros
    """
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
    query = request.dbsession.query(VNumeros).order_by(
        VNumeros.cadastre,
        VNumeros.numero.desc()
    ).filter(*conditions)

    query = query.filter(VNumeros.type_numero_id <= 4)

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


@view_config(route_name='numeros', request_method='POST', renderer='json')
@view_config(route_name='numeros_s', request_method='POST', renderer='json')
def numeros_new_view(request, params=None):
    """
    Add new numeros
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params
        params['no_access'] = "_".join(str(params['cadastre_id']), str(params['numero']))

    # tester si le numéro à réserver est plus grand que le max +1 déjà existant dans la base. Si oui, répondre par une erreur
    num_max = request.dbsession.query(func.max(Numero.numero)).filter(Numero.cadastre_id == params['cadastre_id']).scalar()
    if int(params['numero']) > num_max + 1:
        raise CustomError(CustomError.NUMBER_REGISTRATION_FAILED.format(params['numero'], params['cadastre_id'], num_max))

    # nouveau numero
    record = Numero()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)
    request.dbsession.flush()

    Utils.get_data_save_response(
            Constant.SUCCESS_SAVE.format(Numero.__tablename__)
    )

    return record.id


@view_config(route_name='numeros', request_method='PUT', renderer='json')
@view_config(route_name='numeros_s', request_method='PUT', renderer='json')
def numeros_update_view(request):
    """
    Update numeros
    """
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

    # update numero state in numero_history if changed
    last_record_etat_id = record.etat_id
    record = Utils.set_model_record(record, request.params)

    if 'etat_id' in request.params:
        if request.params['etat_id'] != last_record_etat_id:
            params = Utils._params(
                numero_id=record.id, numero_etat_id=request.params['etat_id'])
            numeros_etat_histo_new_view(request, params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Numero.__tablename__))


@view_config(route_name='numero_by_id', request_method='DELETE', renderer='json')
def numeros_by_id_delete_view(request):
    """
    Supprimer/abandonner numeros by id
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    projet_id = int(settings['numero_projet_id'])
    abandonne_id = int(settings['numero_abandonne_id'])

    # Get numero by id
    id = request.matchdict['id']
    query = request.dbsession.query(Numero).filter(
        Numero.id == id).first()

    if query:
        if query.etat_id == projet_id:
            query.etat_id = abandonne_id
        elif query.etat_id == abandonne_id:
            query.etat_id = projet_id


###########################################################
# NUMERO ETAT HISTO
###########################################################


@view_config(route_name='numeros_etat_histo', request_method='POST', renderer='json')
@view_config(route_name='numeros_etat_histo_s', request_method='POST', renderer='json')
def numeros_etat_histo_new_view(request, params=None):
    """
    Add new numero_etat_histo
    """
    # Check authorization
    settings = request.registry.settings
    if not Utils.has_permission(request, settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params

    # check if etat already exists
    numEtatHisto = request.dbsession.query(NumeroEtatHisto).filter(
        NumeroEtatHisto.numero_id == params['numero_id']
    ).filter(
        NumeroEtatHisto.numero_etat_id == params['numero_etat_id']
    ).first()

    if not numEtatHisto is None:
        return

    # nouveau numero
    record = NumeroEtatHisto()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)
    request.dbsession.flush()

    Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(
        NumeroEtatHisto.__tablename__)
    )

    return record.id

###########################################################
# AFFAIRE-NUMERO
###########################################################


@view_config(route_name='affaire_numeros_by_affaire_id', request_method='GET', renderer='json')
def affaire_numeros_view(request):
    """
    numero_affaire
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()
    conditions = list()
    affaire_id = request.matchdict["id"]

    # Récupérer les id des numéros de la MO
    settings = request.registry.settings

    numeros_immeubles_type_id = [
        settings['numero_bf_id'],
        settings['numero_ddp_id'],
        settings['numero_ppe_id'],
        settings['numero_pcop_id']
    ]

    conditions.append(VNumerosAffaires.affaire_id == affaire_id)
    conditions.append(VNumerosAffaires.numero_type_id.in_(numeros_immeubles_type_id))

    if 'affaire_numero_actif' in request.params:
        affaire_numero_actif = request.params['affaire_numero_actif']
        affaire_numero_actif = True if affaire_numero_actif.upper() == 'TRUE' else False
        conditions.append(VNumerosAffaires.affaire_numero_actif == affaire_numero_actif)

    records = request.dbsession.query(VNumerosAffaires).filter(
        *conditions).order_by(VNumerosAffaires.numero.desc()).all()
    return Utils.serialize_many(records)


@view_config(route_name='affaire_numeros', request_method='PUT', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='PUT', renderer='json')
def affaire_numero_update_view(request):
    """
    Update numeros_affaires
    """
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    affnum_id = request.params["id"] if "id" in request.params else None

    record = request.dbsession.query(AffaireNumero).filter(AffaireNumero.id == affnum_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(AffaireNumero.__tablename__, affnum_id))

    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(AffaireNumero.__tablename__))


@view_config(route_name='affaire_numeros', request_method='DELETE', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='DELETE', renderer='json')
def affaire_numero_delete_view(request):
    """
    delete numeros_affaires
    """
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    affnum_id = None
    affaire_id = None
    numero_id = None
    record = None
    if "id" in request.params:
        affnum_id = request.params["id"]
        record = request.dbsession.query(AffaireNumero).filter(AffaireNumero.id == affnum_id).first()
    elif "affaire_id" in request.params and "numero_id" in request.params:
        affaire_id = int(request.params["affaire_id"])
        numero_id = int(request.params["numero_id"])
        record = request.dbsession.query(AffaireNumero).filter(and_(
            AffaireNumero.affaire_id == affaire_id,
            AffaireNumero.numero_id == numero_id
        )).first()
    else:
        raise CustomError(CustomError.INCOMPLETE_REQUEST)

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(AffaireNumero.__tablename__, affnum_id))


    # Get affaire_type_id and config values
    affaire_type_id = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().type_id
    affaire_type_cadastration_id = int(request.registry.settings['affaire_type_cadastration_id'])

    # supprimer la facture du numéro si c'est une affaire de cadastration
    if affaire_type_id == affaire_type_cadastration_id:
        factNum = request.dbsession.query(Facture).filter(and_(
            Facture.affaire_id == affaire_id,
            Facture.numeros.op("@>")("{" + str(numero_id) + "}")
        )).all()

        for fact in factNum:
            request.dbsession.delete(fact)



    request.dbsession.delete(record)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(AffaireNumero.__tablename__))


@view_config(route_name='affaire_numeros', request_method='POST', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='POST', renderer='json')
def affaire_numero_new_view(request, params=None):
    """
    Add new affaire-numero
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if not params:
        params = request.params

    # check if affaire_numero relation already exists
    affaireNumero = request.dbsession.query(AffaireNumero).filter(
        AffaireNumero.affaire_id == params['affaire_id']
    ).filter(
        AffaireNumero.numero_id == params['numero_id']
    ).filter(
        AffaireNumero.type_id == params['type_id']
    ).first()

    if not affaireNumero is None:
        return

    # nouveau affaire_numero
    record = AffaireNumero()
    record = Utils.set_model_record(record, params)

    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(AffaireNumero.__tablename__))


###########################################################
# NUMERO- AFFAIRE
###########################################################

@view_config(route_name='numero_affaires_by_numero_id', request_method='GET', renderer='json')
def numeros_affaire_view(request):
    """
    Get affaires by numero_id
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    numero_id = request.matchdict['id']

    query = request.dbsession.query(VNumerosAffaires).filter(
        VNumerosAffaires.numero_id == numero_id).all()

    return Utils.serialize_many(query)


###########################################################
# NUMERO DIFFERE
###########################################################

@view_config(route_name='numeros_differes', request_method='GET', renderer='json')
def numero_differe_view(request):
    """
    get numero_differe
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    numero_projet_id = int(request.registry.settings['numero_projet_id'])
    numero_vigueur_id = int(request.registry.settings['numero_vigueur_id'])

    role = request.params['role'] if 'role' in request.params else None

    num_agg = func.array_agg(VNumeros.numero, type_=ARRAY(Integer))
    num_id_agg = func.array_agg(VNumeros.id, type_=ARRAY(Integer))
    diff_id_agg = func.array_agg(VNumeros.diff_id, type_=ARRAY(Integer))
    query = request.dbsession.query(
        VNumeros.diff_affaire_id,
        VNumeros.cadastre,
        num_agg,
        num_id_agg,
        diff_id_agg,
        func.min(VNumeros.diff_entree),
        VNumeros.diff_operateur_id,
        VNumeros.diff_operateur_nom,
        VNumeros.diff_operateur_prenom,
        VNumeros.diff_operateur_initiales
    )
    
    if role == "mo":
        user_id = request.params['user_id'] if 'user_id' in request.params else None
        
        if user_id is not None:
            query = query.filter(VNumeros.diff_operateur_id == user_id)

        query = query.filter(and_(
            VNumeros.diff_entree.isnot(None),
            VNumeros.diff_sortie == None
        ))
    
    elif role == "secr":
        query = query.filter(and_(
            VNumeros.diff_req_radiation.isnot(True),
            VNumeros.diff_sortie.isnot(None),
            VNumeros.etat_id.in_((numero_projet_id, numero_vigueur_id)) 
        ))
    
    elif role == "coord":
        query = query.filter(and_(
            VNumeros.diff_sortie.isnot(None),
            VNumeros.diff_controle == None 
        ))

        
    result = query.group_by(
        VNumeros.diff_affaire_id,
        VNumeros.cadastre,
        VNumeros.diff_operateur_id,
        VNumeros.diff_operateur_nom,
        VNumeros.diff_operateur_prenom,
        VNumeros.diff_operateur_initiales
    ).having(func.array_length(num_agg, 1) > 0).all()

    numeros = []
    for num in result:
        numeros.append({
            'diff_affaire_id': num[0],
            'cadastre': num[1],
            'numero': num[2],
            'numero_id': num[3],
            'diff_id': num[4],
            'diff_entree': datetime.strftime(num[5], '%Y-%m-%d'),
            'diff_operateur_id': num[6],
            'diff_operateur_nom': num[7],
            'diff_operateur_prenom': num[8],
            'diff_operateur_initiales': num[9]
        })

    return numeros


@view_config(route_name='numeros_differes', request_method='POST', renderer='json')
@view_config(route_name='numeros_differes_s', request_method='POST', renderer='json')
def numero_differe_new_view(request):
    """
    Add new numero_differe
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # nouveau numero_differe
    record = NumeroDiffere()
    record = Utils.set_model_record(record, request.params)

    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroDiffere.__tablename__))


@view_config(route_name='numeros_differes', request_method='PUT', renderer='json')
@view_config(route_name='numeros_differes_s', request_method='PUT', renderer='json')
def numero_differe_update_view(request):
    """
    Update numero_differe
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    if "numero_diff_id" in request.params:
        numdiff_id = request.params["numero_diff_id"]
        record = request.dbsession.query(NumeroDiffere).filter(NumeroDiffere.id == numdiff_id).first()
    
    if "numero_id" in request.params:
        num_id = request.params["numero_id"]
        record = request.dbsession.query(NumeroDiffere).filter(NumeroDiffere.numero_id == num_id).first()

    # update numero_differe
    record = Utils.set_model_record(record, request.params)
    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroDiffere.__tablename__))
