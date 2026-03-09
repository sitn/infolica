# -*- coding: utf-8 -*--
from datetime import datetime
from infolica.models.models import Affaire, Cadastre, Client
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, EtapeMailer
from infolica.models.models import Operateur
from infolica.models.models import VAffaire, VAffairesPreavis, VEtapesAffaires
from infolica.scripts.mailer import send_mail
from infolica.scripts.utils import Utils
from sqlalchemy import func, and_
from pyramid.renderers import render

import os


class MailTemplates(object):
    @classmethod
    def sendMailAffaireEtape(cls, request, model, chef_equipe_id, operateur_id):
        # send mail
        affaire_etape_index = request.dbsession.query(AffaireEtapeIndex).filter(AffaireEtapeIndex.id == model.etape_id).first()
        etape_mailer = request.dbsession.query(EtapeMailer).filter(model.etape_id == EtapeMailer.etape_id).all()
        v_affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == model.affaire_id).first()
        operateur = Utils.getOperateursActifs(request).all()

        # get list of done steps
        lastSteps = request.dbsession.query(VEtapesAffaires).filter(and_(VEtapesAffaires.affaire_id == model.affaire_id, VEtapesAffaires.etape_priorite == int(request.registry.settings["affaire_etape_priorite_1_id"]))).order_by(VEtapesAffaires.next_datetime.desc()).all()

        # only when chef_equipe is specified and chef equipe is not the initiator of new step
        mail_list = []
        if chef_equipe_id and (not chef_equipe_id == operateur_id):
            chef_equipe_mail = Utils.getOperateursActifs(request).filter(Operateur.id == chef_equipe_id).first().mail
            if chef_equipe_mail is not None:
                mail_list.append(chef_equipe_mail)

        # construct mail_list
        for em_i in etape_mailer:
            if em_i.sendmail:
                mail = next((op.mail for op in operateur if op.id == em_i.operateur_id), None)
                if mail:
                    mail_list.append(mail)

        # Send mail only if step prio is 1 and if mail_list not empty
        if affaire_etape_index.priorite == int(request.registry.settings["affaire_etape_priorite_1_id"]) and len(mail_list) > 0:
            subject = "Infolica - Nouvelle étape - Affaire " + str(v_affaire.id) + (" - URGENT" if v_affaire.urgent else "")

            text = render(
                "infolica:templates/emails/etape_notification.html",
                {
                    "title": "Infolica - Nouvelle étape",
                    "admin_mail": request.registry.settings["admin_mail"],
                    "step_list": lastSteps,
                    "infolica_url_base": request.registry.settings["infolica_url_base"],
                    "v_affaire": v_affaire,
                    "affaire_etape_index": affaire_etape_index,
                },
            )

            send_mail(request, mail_list, "", subject, html=text)

        return (lastSteps, affaire_etape_index)

    @classmethod
    def sendMailAffaireUrgente(cls, request, affaire):
        affaire_etape_affaire_urgente_mo_id = request.registry.settings["affaire_etape_affaire_urgente_mo_id"]
        affaire_etape_affaire_urgente_ppe_id = request.registry.settings["affaire_etape_affaire_urgente_ppe_id"]
        affaire_type_ppe_id = request.registry.settings["affaire_type_ppe_id"]
        affaire_type_modification_ppe_id = request.registry.settings["affaire_type_modification_ppe_id"]

        mail_list = []

        operateur_etapeMailer = Utils.getOperateursActifs(request).join(EtapeMailer, EtapeMailer.operateur_id == Operateur.id).filter(EtapeMailer.sendmail == True)

        # Check if user wants to be notified in case of PPE or other MO affaires (based on etape-mailer table)
        if affaire.type_id in (affaire_type_ppe_id, affaire_type_modification_ppe_id):
            operateur_etapeMailer = operateur_etapeMailer.filter(EtapeMailer.etape_id == affaire_etape_affaire_urgente_ppe_id)
        else:
            operateur_etapeMailer = operateur_etapeMailer.filter(EtapeMailer.etape_id == affaire_etape_affaire_urgente_mo_id)

        for op in operateur_etapeMailer.all():
            op_mail = op.mail
            if op_mail is not None:
                mail_list.append(op_mail)

        v_affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == affaire.id).first()

        # Add technicien + creator of affaire
        technicien = operateur_etapeMailer.filter(Operateur.id == affaire.technicien_id).first()
        if technicien and technicien.mail is not None:
            mail_list.append(technicien.mail)

        if len(mail_list) == 0:
            return

        subject = "Infolica - Affaire urgente"

        text = render(
            "infolica:templates/emails/urgent_notification.html",
            {
                "title": subject,
                "admin_mail": request.registry.settings["admin_mail"],
                "infolica_url_base": request.registry.settings["infolica_url_base"],
                "v_affaire": v_affaire,
            },
        )

        send_mail(request, mail_list, "", subject, html=text)
        return

    @classmethod
    def sendMailClientHorsCanton(cls, request, client_id, affaire_id):
        affaire_etape_client_hors_canton_id = int(request.registry.settings["affaire_etape_client_hors_canton_id"])
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first()
        cl = request.dbsession.query(Client).filter(Client.id == client_id).first()

        # contrôle qu'aucune étape de demande de création du client hors canton n'ait été envoyée
        nb_demandes = (
            request.dbsession.query(func.count(AffaireEtape.id))
            .filter(
                # AffaireEtape.affaire_id == affaire_id,
                AffaireEtape.etape_id == affaire_etape_client_hors_canton_id,
                AffaireEtape.remarque == "client_id=" + str(cl.id),
            )
            .scalar()
        )
        if nb_demandes > 0:
            return

        # Contrôle que le client habite hors canton et que son numéros SAP est null
        cl_npa = int(cl.npa) if cl.npa is not None else -1
        if cl.no_sap is None and cl_npa not in request.registry.settings["npa_NE"]:
            operateur_secretariat = request.registry.settings["operateur_secretariat"].split(",")
            operateurs = Utils.getOperateursActifs(request).filter(Operateur.id.in_(operateur_secretariat)).all()
            mail_list = [op.mail for op in operateurs]

            subject = "Infolica - Client hors canton à vérifier"
            client_adress = ", ".join(
                [
                    cl.entreprise if cl.entreprise is not None else " ".join([cl.titre if cl.titre is not None else "", cl.prenom if cl.prenom is not None else "", cl.nom if cl.nom is not None else ""]),
                    cl.adresse if cl.adresse is not None else "",
                    " ".join([cl.npa if cl.npa is not None else "", cl.localite if cl.localite is not None else ""]),
                ]
            )

            text = render(
                "infolica:templates/emails/client_hors_canton_notification.html",
                {
                    "title": subject,
                    "admin_mail": request.registry.settings["admin_mail"],
                    "affaire": affaire,
                    "client_adress": client_adress,
                    "client_id": cl.id,
                    "infolica_url_base": request.registry.settings["infolica_url_base"],
                },
            )

            # update affaire_etape
            affaire_etape = AffaireEtape(affaire_id=affaire_id, operateur_id=Utils.getOperateurFromUser(request).id, etape_id=affaire_etape_client_hors_canton_id, datetime=datetime.now(), remarque="client_id=" + str(cl.id))
            request.dbsession.add(affaire_etape)

            send_mail(request, mail_list, "", subject, html=text)

        return

    @classmethod
    def sendMailPreavisReponse(cls, request, preavis_id):
        preavis = request.dbsession.query(VAffairesPreavis).filter(VAffairesPreavis.id == preavis_id).first()
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == preavis.affaire_id).first()

        subject = "Infolica - Un nouveau préavis a été saisi"

        operateur_coordinateur_projets = request.registry.settings["operateur_coordinateur_projets"].split(",")
        operateurs_liste = Utils.getOperateursActifs(request).filter(Operateur.id.in_(operateur_coordinateur_projets)).all()
        mail_list = [op.mail for op in operateurs_liste]

        text = render(
            "infolica:templates/emails/preavis_reponse_notification.html",
            {
                "title": subject,
                "admin_mail": request.registry.settings["admin_mail"],
                "preavis": preavis,
                "affaire": affaire,
                "infolica_url_base": request.registry.settings["infolica_url_base"],
            },
        )

        send_mail(request, mail_list, "", subject, html=text)

        return

    @classmethod
    def sendMailPreavisDemande(cls, request, preavis_id, service_id, message=None):

        operateurs = Utils.getOperateursActifs(request).filter(Operateur.service_id == service_id).all()

        mail_list = []
        etape_mailer = request.dbsession.query(EtapeMailer)
        for op in operateurs:
            em = etape_mailer.filter(EtapeMailer.operateur_id == op.id).first()
            if em is not None and em.sendmail is True:
                mail_list.append(op.mail)

        if len(mail_list) > 0:
            preavis = request.dbsession.query(VAffairesPreavis).filter(VAffairesPreavis.id == preavis_id).first()
            affaire = request.dbsession.query(Affaire).filter(Affaire.id == preavis.affaire_id).first()
            cadastre = request.dbsession.query(Cadastre).filter(Cadastre.id == affaire.cadastre_id).first().nom

            link = str(os.path.join(request.registry.settings["infolica_url_base"], "preavis/edit", str(preavis_id))).replace("\\", "/")
            subject = "Infolica - Demande de préavis"
            if affaire.urgent:
                subject += " - affaire urgente"

            text = render(
                "infolica:templates/emails/preavis_demande_notification.html",
                {
                    "title": subject,
                    "admin_mail": request.registry.settings["admin_mail"],
                    "affaire": affaire,
                    "cadastre": cadastre,
                    "link": link,
                    "message": message,
                },
            )

            send_mail(request, mail_list, "", subject, html=text)
            return
