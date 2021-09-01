# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import and_

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, VEtapesAffaires, VAffaire, EtapeMailer, Operateur, Affaire
from infolica.scripts.utils import Utils
from infolica.scripts.mailer import send_mail

import os

###########################################################
# ETAPES AFFAIRE
###########################################################
@view_config(route_name='etapes_index', request_method='GET', renderer='json')
@view_config(route_name='etapes_index_s', request_method='GET', renderer='json')
def etapes_index_view(request):
    """
    GET etapes index
    """
    # Check connected
    if not Utils.check_connected(request):
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
    if not Utils.check_connected(request):
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
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    chef_equipe_id = request.params['chef_equipe_id'] if 'chef_equipe_id' in request.params else None
    
    # Add new step
    model = Utils.addNewRecord(request, AffaireEtape)

    # send mail
    affaire_etape_index = request.dbsession.query(AffaireEtapeIndex).filter(AffaireEtapeIndex.id == model.etape_id).first()
    etape_mailer = request.dbsession.query(EtapeMailer).filter(model.etape_id == EtapeMailer.etape_id).all()
    operateur = request.dbsession.query(Operateur).all()
    mail_list = []

    # only when chef_equipe is specified
    if chef_equipe_id:
        mail_list.append( request.dbsession.query(Operateur).filter(Operateur.id == chef_equipe_id).first().mail )
        # update chef d'équipe in affaire
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == model.affaire_id).first()
        affaire.technicien_id = chef_equipe_id

    # construct mail_list
    for em_i in etape_mailer:
        if em_i.sendmail:
            mail = next((op.mail for op in operateur if op.id == em_i.operateur_id), None)
            if mail:
                mail_list.append(mail)
    
    # Send mail only if step prio is 1 and if mail_list not empty
    if affaire_etape_index.priorite == int(request.registry.settings['affaire_etape_priorite_1_id']) and len(mail_list)>0:
        # get affaire informations
        affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == model.affaire_id).first()
        # get list of done steps
        lastSteps = request.dbsession.query(VEtapesAffaires).filter(
            and_(
                VEtapesAffaires.affaire_id == model.affaire_id,
                VEtapesAffaires.etape_priorite == int(request.registry.settings['affaire_etape_priorite_1_id'])
            )
        ).order_by(VEtapesAffaires.next_datetime.desc()).all()
        lastSteps = "".join(["<tr><td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{} {}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              </tr>".format(
                                  i.etape, 
                                  i.next_operateur_prenom if i.next_operateur_prenom else "", 
                                  i.next_operateur_nom if i.next_operateur_nom else "", 
                                  i.next_datetime.strftime("%d.%m.%Y - %H:%M") if i.next_datetime else "", 
                                  i.next_remarque if i.next_remarque else ""
                                ) for i in lastSteps])
        
        affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""
        text = "L'affaire <b><a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'affaires/edit', str(affaire.id)) + "'>" + str(affaire.id) + affaire_nom + "</a></b>" + (" (avec mention urgente)" if affaire.urgent else "") + " est en attente pour l'étape <b>"+ affaire_etape_index.nom +"</b>."
        text += "<br><br>Cadastre: " + str(affaire.cadastre)
        text += "<br>Description: " + str(affaire.nom)
        text += ("<br><br><br><h4>Historique de l'affaire</h4>\
            <table style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>\
                <tr>\
                    <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Étape</th>\
                    <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Réalisée par</th>\
                    <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Réalisée le</th>\
                    <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Remarque</th>\
                </tr>" + lastSteps + "</table>") if lastSteps != "" else ""
        subject = "Infolica - affaire " + str(affaire.id) + (" - URGENT" if affaire.urgent else "")
        send_mail(request, mail_list, "", subject, html=text)

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
