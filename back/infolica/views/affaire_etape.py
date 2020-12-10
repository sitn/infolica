# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from sqlalchemy import and_

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, VEtapesAffaires, VAffaire, EtapeMailer, Operateur
from infolica.scripts.utils import Utils
from infolica.scripts.mailer import send_mail

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
    ).all()

    return Utils.serialize_many(records)


@view_config(route_name='etapes', request_method='POST', renderer='json')
@view_config(route_name='etapes_s', request_method='POST', renderer='json')
def etapes_new_view(request):
    """
    POST etapes affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_etape_edition']):
        raise exc.HTTPForbidden()

    model = AffaireEtape()
    model = Utils.set_model_record(model, request.params)

    request.dbsession.add(model)

    # send mail
    affaire_etape_index = request.dbsession.query(AffaireEtapeIndex).filter(AffaireEtapeIndex.id == model.etape_id).first()
    etape_mailer = request.dbsession.query(EtapeMailer).filter(model.etape_id == EtapeMailer.etape_id).all()
    operateur = request.dbsession.query(Operateur).all()
    mail_list = []
    for em_i in etape_mailer:
        if em_i.sendmail:
            mail = next((op.mail for op in operateur if op.id == em_i.operateur_id), None)
            if mail:
                mail_list.append(mail)
    if affaire_etape_index.priorite == int(request.registry.settings['affaire_etape_priorite_1_id']) and len(mail_list)>0:
        # get affaire informations
        affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == model.affaire_id).first()
        # get list of done steps
        lastSteps = request.dbsession.query(VEtapesAffaires).filter(
            and_(
                VEtapesAffaires.affaire_id == model.affaire_id,
                VEtapesAffaires.etape_priorite == int(request.registry.settings['affaire_etape_priorite_1_id'])
            )
        ).order_by(VEtapesAffaires.id.desc()).all()
        lastSteps = "".join(["<tr><td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{} {}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              <td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
                              </tr>".format(i.datetime, i.operateur_prenom, i.operateur_nom, i.etape, i.remarque if i.remarque else "") for i in lastSteps])
        
        text = "L'affaire <b>" + str(affaire.id) + " (" + affaire.nom + ")</b> est en attente pour l'étape <b>"+ affaire_etape_index.nom +"</b>."
        text += ("<br><br><br><h4>Historique de l'affaire</h4><table style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'><tr><th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Horodateur</th><th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Opérateur</th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'><th>Etape</th><th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Remarque</th></tr>" + lastSteps + "</table>") if lastSteps != "" else ""
        subject = "Infolica - affaire " + str(affaire.id)
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
