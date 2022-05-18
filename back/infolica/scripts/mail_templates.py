# -*- coding: utf-8 -*--
from datetime import datetime
from infolica.models.models import Affaire, Cadastre, Client
from infolica.models.models import Operateur
from infolica.models.models import VAffairesPreavis
from infolica.scripts.mailer import send_mail


import os


class MailTemplates(object):

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
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first()
        affaire_nom = " (" + affaire.no_access + ")" if affaire.no_access is not None else ""
        cl = request.dbsession.query(Client).filter(Client.id == client_id).first()
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
        


