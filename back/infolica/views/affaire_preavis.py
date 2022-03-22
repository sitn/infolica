# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Affaire, VAffaire, Operateur
from infolica.models.models import Preavis, PreavisType, VAffairesPreavis
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected

from datetime import datetime
import time

from sqlalchemy import func

###########################################################
# PREAVIS AFFAIRE
###########################################################


@view_config(route_name='preavis_type', request_method='GET', renderer='json')
@view_config(route_name='preavis_type_s', request_method='GET', renderer='json')
def preavis_type_view(request):
    """
    GET preavis type
    """
    records = request.dbsession.query(PreavisType).all()
    return Utils.serialize_many(records)


@view_config(route_name='affaire_preavis_by_affaire_id', request_method='GET', renderer='json')
def affaire_preavis_view(request):
    """
    GET preavis affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    records = request.dbsession.query(VAffairesPreavis).filter(
        VAffairesPreavis.affaire_id == affaire_id
        ).all()

    return Utils.serialize_many(records)


@view_config(route_name='preavis', request_method='POST', renderer='json')
@view_config(route_name='preavis_s', request_method='POST', renderer='json')
def preavis_new_view(request):
    """
    POST preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    model = Preavis()
    model = Utils.set_model_record(model, request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Preavis.__tablename__))


@view_config(route_name='preavis', request_method='PUT', renderer='json')
@view_config(route_name='preavis_s', request_method='PUT', renderer='json')
def preavis_update_view(request):
    """
    UPDATE preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    preavis_id = request.params['id'] if 'id' in request.params else None

    record = request.dbsession.query(Preavis).filter(
        Preavis.id == preavis_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Preavis.__tablename__, preavis_id))

    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Preavis.__tablename__))


@view_config(route_name='preavis', request_method='DELETE', renderer='json')
@view_config(route_name='preavis_s', request_method='DELETE', renderer='json')
def preavis_delete_view(request):
    """
    DELETE preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None

    record = request.dbsession.query(Preavis).filter(
        Preavis.id == preavis_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Preavis.__tablename__, preavis_id))

    request.dbsession.delete(record)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Preavis.__tablename__))



# ====================================================================
#    ROUTES POUR LES SERVICES EXTERNES
# ====================================================================

def getOperateurFromUser(request):
    user = request.authenticated_userid    
    operateur = request.dbsession.query(Operateur).filter(
        func.lower(Operateur.login) == user
    ).first()
    return operateur

@view_config(route_name='service_externe_preavis', request_method='GET', renderer='json')
def service_externe_preavis_view(request):
    """
    GET preavis for service externe
    """
    # Check connected
    if not check_connected(request, ["SAT"]):
        raise exc.HTTPForbidden()

    # get service from user
    operateur = getOperateurFromUser(request)

    if operateur.service_id is None:
        exc.HTTPForbidden(detail="Opérateur non autorisé à accéder à ce contenu")

    records = request.dbsession.query(
        Preavis.id,
        Preavis.date_demande,
        Preavis.date_reponse,
        Preavis.affaire_id,
        VAffaire.cadastre,
        VAffaire.nom
    ).join(
        VAffaire, Preavis.affaire_id == VAffaire.id
    ).filter(
        Preavis.date_reponse == None
    ).filter(
        Preavis.service_id == operateur.service_id
    ).order_by(Preavis.date_demande.desc()).all()

    results = []
    for rec in records:
        results.append({
            'preavis_id': rec[0],
            'preavis_date_demande': datetime.strftime(rec[1], "%d.%M.%Y"),
            'preavis_date_demande_int': time.mktime(rec[1].timetuple()),
            'preavis_date_reponse': datetime.strftime(rec[2], "%d.%M.%Y") if rec[2] is not None else None,
            'preavis_date_reponse_int': time.mktime(rec[2].timetuple()) if rec[2] is not None else None,
            'preavis_affaire_id': rec[3],
            'affaire_cadastre': rec[4],
            'affaire_description': rec[5],
        })

    return results

@view_config(route_name='service_externe_affaire', request_method='GET', renderer='json')
def service_externe_affaire_view(request):
    """
    GET affaire for service externe
    """
    # Check connected
    if not check_connected(request, ["SAT"]):
        raise exc.HTTPForbidden()

    # get service from user
    operateur = getOperateurFromUser(request)
    if operateur.service_id is None:
        exc.HTTPForbidden(detail="Opérateur non autorisé à accéder à ce contenu")
    
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    if affaire_id is None:
        exc.HTTPInternalServerError(detail="L'identidifiant de l'affaire est manquant")

    testPreavis = request.dbsession.query(Affaire).join(
        Preavis, Preavis.affaire_id == Affaire.id
    ).filter(
        Preavis.service_id == operateur.service_id
    ).first()

    if testPreavis is None:
        exc.HTTPForbidden(detail="Opérateur non autorisé à accéder à ce contenu")


    record = request.dbsession.query(
        VAffaire.id,
        VAffaire.nom,
        VAffaire.client_commande_type_id,
        VAffaire.client_commande_entreprise,
        VAffaire.client_commande_titre,
        VAffaire.client_commande_nom,
        VAffaire.client_commande_prenom,
        VAffaire.client_commande_complement,
        VAffaire.client_commande_adresse,
        VAffaire.client_commande_co,
        VAffaire.client_commande_npa,
        VAffaire.client_commande_localite,
        VAffaire.client_commande_tel_fixe,
        VAffaire.client_commande_tel_portable,
        VAffaire.client_commande_mail,
        VAffaire.type_affaire,
        VAffaire.cadastre,
        VAffaire.date_ouverture
    ).filter(
        VAffaire.id == affaire_id
    ).first()

    client = ", ".join(filter(None, [
        record[3],
        record[7],
        " ".join(filter(None, [record[4], record[6],  record[5]])),
        " ".join(filter(None, [record[10], record[11]])),
        record[12],
        record[13],
        record[14]
    ]))

    result = {
        'id': record[0],
        'nom': record[1],
        'client': client,
        'type_affaire': record[15],
        'cadastre': record[16],
        'date_ouverture': datetime.strftime(record[17], "%d.%M.%Y")
    }

    return result

