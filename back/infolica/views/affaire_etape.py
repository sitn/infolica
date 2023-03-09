# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import and_

from infolica.scripts.controle_etape import ControleEtapeChecker

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, VEtapesAffaires
from infolica.models.models import Affaire, VAffaire, AffaireType, Facture
from infolica.scripts.mail_templates import MailTemplates
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
import os

###########################################################
# ETAPES AFFAIRE
###########################################################
@view_config(route_name='etapes_index_by_affaire_id', request_method='GET', renderer='json')
def etape_index_by_affaire_id_view(request):
    """
    GET etape index by affaire_id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None

    if affaire_id is None:
        raise exc.HTTPBadRequest(detail="Aucun index spécifié")

    etape = request.dbsession.query(
        AffaireEtapeIndex
    ).join(
        AffaireEtape, AffaireEtape.etape_id == AffaireEtapeIndex.id
    ).filter(
        AffaireEtape.affaire_id == affaire_id,
        AffaireEtapeIndex.ordre != None
    ).order_by(AffaireEtape.datetime.desc()).limit(1).first()

    # get next step id
    logique_processus = request.dbsession.query(
        AffaireType.logique_processus
    ).join(
        Affaire, Affaire.type_id == AffaireType.id
    ).filter(
        Affaire.id == affaire_id
    ).scalar()

    next_step_id = None
    if logique_processus is not None and etape.id in logique_processus:
        idx = logique_processus.index(etape.id)

        if idx < len(logique_processus)-1:
            next_step_id = logique_processus[idx + 1]

    data = {
        'etape': etape.nom if etape is not None else None,
        'predicted_next_step_id': next_step_id
    }


    return data


@view_config(route_name='etapes_index', request_method='GET', renderer='json')
@view_config(route_name='etapes_index_s', request_method='GET', renderer='json')
def etapes_index_view(request):
    """
    GET etapes index
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    records = request.dbsession.query(AffaireEtapeIndex).filter(
        AffaireEtapeIndex.ordre != None
        ).order_by(AffaireEtapeIndex.ordre.asc()).all()
    return Utils.serialize_many(records)


@view_config(route_name='affaire_etapes_by_affaire_id', request_method='GET', renderer='json')
def affaires_etapes_view(request):
    """
    GET etapes affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    records = request.dbsession.query(VEtapesAffaires).filter(
        VEtapesAffaires.affaire_id == affaire_id
    ).order_by(
        VEtapesAffaires.next_datetime.desc()
    ).all()

    return Utils.serialize_many(records)


@view_config(route_name='etapes', request_method='POST', renderer='json')
@view_config(route_name='etapes_s', request_method='POST', renderer='json')
def etapes_new_view(request):
    """
    POST etapes affaire
    """
    # Check authorization
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    chef_equipe_id = request.params['chef_equipe_id'] if 'chef_equipe_id' in request.params else None
    operateur_id = request.params['operateur_id'] if 'operateur_id' in request.params else None
    
    # Add new step
    model = Utils.addNewRecord(request, AffaireEtape)

    # # send mail
    (lastSteps, affaire_etape_index) = MailTemplates.sendMailAffaireEtape(request, model, chef_equipe_id, operateur_id)
    
    # update chef d'équipe in affaire
    affaire = request.dbsession.query(Affaire).filter(Affaire.id == model.affaire_id).first()
    if not affaire.technicien_id == chef_equipe_id and chef_equipe_id is not None:
        affaire.technicien_id = chef_equipe_id

    # Finally erase attribution on affaire if etape_priority == 1 and if last etape was different
    if affaire_etape_index.priorite == int(request.registry.settings['affaire_etape_priorite_1_id']):
        last2Steps = request.dbsession.query(
            AffaireEtape
        ).join(
            AffaireEtapeIndex, AffaireEtapeIndex.id == AffaireEtape.etape_id
        ).filter(
            and_(
                AffaireEtape.affaire_id == affaire_id,
                AffaireEtapeIndex.priorite == 1
            )
        ).order_by(AffaireEtape.datetime.desc()).limit(2).all()

        if not int(last2Steps[0].etape_id) == int(last2Steps[1].etape_id):
            affaire.attribution = None


    # If last step was treatment & client_facture is outside of canton and has no SAP number, send mail to secretariat
    etape_traitement_id = int(request.registry.settings['affaire_etape_traitement_id'])
    
    if (len(lastSteps) > 1 and lastSteps[1].etape_id == etape_traitement_id):
        # get clients_facture
        clients_factures_id = request.dbsession.query(Facture.client_id).filter(Facture.affaire_id == affaire_id).all()
        clients_factures_id = [cl_id[0] for cl_id in clients_factures_id]
        for cl_id in clients_factures_id:
            MailTemplates.sendMailClientHorsCanton(request, cl_id, affaire.id)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(AffaireEtape.__tablename__))


@view_config(route_name='etapes_by_id', request_method='DELETE', renderer='json')
def etapes_delete_view(request):
    """
    DELETE etapes affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_etape_edition']):
        raise exc.HTTPForbidden()

    affaire_etape_id = request.matchdict['id']

    record = request.dbsession.query(AffaireEtape).filter(
        AffaireEtape.id == affaire_etape_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(AffaireEtape.__tablename__, affaire_etape_id))

    request.dbsession.delete(record)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(AffaireEtape.__tablename__))


@view_config(route_name='controle_etape', request_method='GET', renderer='json')
def controle_etape_view(request):
    """
    Controles - étape
    """
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None

    affaire = request.dbsession.query(
        VAffaire
    ).filter(
        VAffaire.id == affaire_id
    ).first()

    results = ControleEtapeChecker.controleEtape(
        request=request,
        affaire_id=affaire_id,
        affaire_type_id=affaire.type_id,
        etape_id=affaire.etape_id
    )

    return results
