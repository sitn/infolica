# -*- coding: utf-8 -*--
from datetime import datetime
from infolica.models.models import Affaire, Cadastre, Client
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, EtapeMailer
from infolica.models.models import Operateur
from infolica.models.models import VAffaire, VAffairesPreavis, VEtapesAffaires
from infolica.scripts.mailer import send_mail
from infolica.scripts.utils import Utils
from sqlalchemy import func, and_

import os


class MailTemplates(object):

    @classmethod
    def sendMailAffaireEtape(cls, request, model, chef_equipe_id, operateur_id):
        # send mail
        affaire_etape_index = request.dbsession.query(AffaireEtapeIndex).filter(AffaireEtapeIndex.id == model.etape_id).first()
        etape_mailer = request.dbsession.query(EtapeMailer).filter(model.etape_id == EtapeMailer.etape_id).all()
        v_affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == model.affaire_id).first()
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == model.affaire_id).first()
        operateur = request.dbsession.query(Operateur).all()

        # get list of done steps
        lastSteps = request.dbsession.query(VEtapesAffaires).filter(
            and_(
                VEtapesAffaires.affaire_id == model.affaire_id,
                VEtapesAffaires.etape_priorite == int(request.registry.settings['affaire_etape_priorite_1_id'])
            )
        ).order_by(VEtapesAffaires.next_datetime.desc()).all()
        
        # set affaire_nom
        affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""

        # only when chef_equipe is specified and chef equipe is not the initiator of new step
        mail_list = []
        if chef_equipe_id and (not chef_equipe_id == operateur_id):
            chef_equipe_mail = request.dbsession.query(Operateur).filter(Operateur.id == chef_equipe_id).first().mail
            if chef_equipe_mail is not None:
                mail_list.append( chef_equipe_mail )

        # construct mail_list
        for em_i in etape_mailer:
            if em_i.sendmail:
                mail = next((op.mail for op in operateur if op.id == em_i.operateur_id), None)
                if mail:
                    mail_list.append(mail)
        
        # Send mail only if step prio is 1 and if mail_list not empty
        if affaire_etape_index.priorite == int(request.registry.settings['affaire_etape_priorite_1_id']) and len(mail_list)>0:
            lastSteps_html = "".join(["<tr><td style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>{}</td>\
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
            
            text = "L'affaire <b><a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'affaires/edit', str(v_affaire.id)) + "'>" + str(v_affaire.id) + affaire_nom + "</a></b>" + (" (avec mention urgente)" if v_affaire.urgent else "") + " est en attente pour l'étape <b>"+ affaire_etape_index.nom +"</b>."
            text += "<br><br>Cadastre: " + str(v_affaire.cadastre)
            text += "<br>Description: " + str(v_affaire.nom)
            text += ("<br><br><br><h4>Historique de l'affaire</h4>\
                <table style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>\
                    <tr>\
                        <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Étape</th>\
                        <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Réalisée par</th>\
                        <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Réalisée le</th>\
                        <th style='border: 1px solid black; border-collapse: collapse; padding: 5px 25px 5px 10px;'>Remarque</th>\
                    </tr>" + lastSteps_html + "</table>") if lastSteps_html != "" else ""
            subject = "Infolica - affaire " + str(v_affaire.id) + (" - URGENT" if v_affaire.urgent else "")
            send_mail(request, mail_list, "", subject, html=text)
        
        return (lastSteps, affaire_etape_index)


    @classmethod
    def sendMailAffaireUrgente(cls, request, model):
        mail_list = []
        operateur_affaire_urgente = request.registry.settings['operateur_affaire_urgente'].split(',')
        for op_id in operateur_affaire_urgente:
            op_mail = request.dbsession.query(Operateur).filter(Operateur.id == op_id).first().mail
            if op_mail is not None:
                mail_list.append(op_mail)
        # Add technicien + creator of affaire
        technicien = request.dbsession.query(Operateur).filter(Operateur.id == model.technicien_id).first()
        if technicien.mail is not None:
            mail_list.append(technicien.mail)

        if len(mail_list) == 0:
            return

        subject = "Infolica - Affaire urgente"
        cadastre = request.dbsession.query(Cadastre).filter(Cadastre.id == model.cadastre_id).first().nom
        affaire_nom = " (" + model.no_access + ")" if model.no_access is not None else ""
        text = "La mention 'URGENTE' a été attribuée à l'affaire <b><a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'affaires/edit', str(model.id)) + "'>" + str(model.id) + affaire_nom + "</a></b>.<br>"
        echeance = "non défini"
        if not model.urgent_echeance is None:
            echeance = datetime.strptime(model.urgent_echeance, '%Y-%m-%d').strftime("%d.%m.%Y")
        text += "Échéance: " + echeance + "<br><br>"
        text += "Merci de traiter cette affaire en priorité."
        text += "<br><br><br>Données de l'affaire:<br> \
                <ul><li>Chef de projet: " + str(technicien.initiales) + "</li>\
                <li>Cadastre: " + str(cadastre) + "</li>\
                <li>Description: " + str(model.nom) + "</li></ul>"
        send_mail(request, mail_list, "", subject, html=text)
        return


    @classmethod
    def sendMailClientHorsCanton(cls, request, client_id, affaire_id):
        affaire_etape_client_hors_canton_id = int(request.registry.settings['affaire_etape_client_hors_canton_id'])
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first()
        affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""
        cl = request.dbsession.query(Client).filter(Client.id == client_id).first()

        # contrôle qu'aucune étape de demande de création du client hors canton n'ait été envoyée
        nb_demandes = request.dbsession.query(
            func.count(AffaireEtape.id)
        ).filter(
            # AffaireEtape.affaire_id == affaire_id,
            AffaireEtape.etape_id == affaire_etape_client_hors_canton_id,
            AffaireEtape.remarque == 'client_id=' + str(cl.id)
        ).scalar()
        if nb_demandes > 0:
            return

        #Contrôle que le client habite hors canton et que son numéros SAP est null
        if cl.no_sap is None and int(cl.npa) not in request.registry.settings['npa_NE']:
            operateur_secretariat = request.registry.settings["operateur_secretariat"].split(",")
            mail_list = request.dbsession.query(Operateur.mail).filter(Operateur.id.in_(operateur_secretariat)).all()
            mail_list = [mail[0] for mail in mail_list]

            html = "<h3>Vérification de client</h3>"
            html += "<p>Un client hors canton et sans numéro SAP a été référencé dans la facturation de l'affaire <b><a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'affaires/edit', str(affaire_id)) + "'>" + str(affaire_id) + affaire_nom + "</a></b>.</p>"
            html += "<ul><li>" + ", ".join([
                cl.entreprise if cl.entreprise is not None else " ".join([
                    cl.titre if cl.titre is not None else "", 
                    cl.prenom if cl.prenom is not None else "", 
                    cl.nom if cl.nom is not None else ""
                ]), 
                cl.adresse if cl.adresse is not None else "", 
                " ".join([
                        cl.npa if cl.npa is not None else "", 
                        cl.localite if cl.localite is not None else ""
                    ])
                ]) + " &#8594; <a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'clients/edit', str(cl.id)) + "'>Lien sur la fiche du client</a>"+ "</li></ul>"
            html += "<p>Merci d'entreprendre les démarches nécessaires pour corriger le client ou pour demander sa création dans SAP.</p>"
            send_mail(request, mail_list, "", "Infolica - Client hors canton à vérifier", html=html)

            affaire_etape = AffaireEtape(
                affaire_id = affaire_id,
                operateur_id = Utils.getOperateurFromUser(request).id,
                etape_id = affaire_etape_client_hors_canton_id,
                datetime = datetime.now(),
                remarque = 'client_id=' + str(cl.id)
            )
            request.dbsession.add(affaire_etape)

        return


    @classmethod
    def sendMailPreavisReponse(cls, request, preavis_id):
        preavis = request.dbsession.query(VAffairesPreavis).filter(VAffairesPreavis.id == preavis_id).first()
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == preavis.affaire_id).first()
        
        affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""
        
        operateur_coordinateur_projets = request.registry.settings["operateur_coordinateur_projets"].split(",")
        mail_list = request.dbsession.query(Operateur.mail).filter(Operateur.id.in_(operateur_coordinateur_projets)).all()
        mail_list = [mail[0] for mail in mail_list]

        html = "<h3>Un nouveau préavis a été saisi</h3>"
        html += "<p>Le préavis du " + preavis.service + " a été saisi pour l'affaire <b><a href='" + os.path.join(request.registry.settings['infolica_url_base'], 'affaires/edit', str(preavis.affaire_id)) + "'>" + str(preavis.affaire_id) + affaire_nom + "</a></b>.<br/>"
        html += "Il peut être consulté dans l'onglet Préavis de l'affaire, en cliquant sur le préavis en question dans le tableau.</p>"
        
        send_mail(request, mail_list, "", "Infolica - Préavis saisi", html=html)
        return


    @classmethod
    def sendMailPreavisDemande(cls, request, preavis_id, service_id, message=None):

        operateurs = request.dbsession.query(Operateur).filter(Operateur.service_id == service_id).all()

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
            
            affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""
            link = str(os.path.join(request.registry.settings['infolica_url_base'], 'preavis/edit', str(preavis_id))).replace('\\', '/')

            subject_suffix = ''

            html = "<p>Bonjour,</p>"
            html += "<p>"
            html += "Une nouvelle demande de préavis est en attente dans la centrale à préavis."
            if affaire.urgent is True:
                subject_suffix = ' - affaire urgente'
                html += "<br>"
                html += "L'affaire porte la mention <b>urgente</b>."
                if affaire.urgent_echeance is not None:
                    html += " Le délai de traitement au SGRF a été fixé au " + datetime.strftime(affaire.urgent_echeance, '%d.%m.%Y')
                html += "<br>"
            html += "<ul>"
            html += "<li>Référence de l'affaire au SGRF: " + str(affaire.id) + affaire_nom + "</li>"
            html += "<li>Cadastre: " + cadastre + "</li>"
            html += "<li>Description: " + affaire.nom + "</li>"
            html += "<li>Lien: <a href='" + link + "'>" + link + "</a></li>"
            if message is not None:
                html += "<li>Remarque: " + message + "</li>"
            html += "</ul>"
            html += "</p>"
            
            send_mail(request, mail_list, "", "Infolica - Demande de préavis" + subject_suffix, html=html, signature="Le service de la géomatique et du registre foncier")
            return

