# -*- coding: utf-8 -*--
from datetime import date, datetime
from sqlalchemy import func, and_, desc
from sqlalchemy import String
from sqlalchemy.sql.expression import cast
from infolica.models.models import Affaire
from infolica.models.models import Numero, AffaireNumero, Client
from infolica.models.models import Role, ReservationNumerosMO, Cadastre, Operateur
from infolica.scripts.mailer import send_mail

from infolica.scripts.authentication import get_user_functions, check_connected

from shutil import copytree, ignore_patterns
import json
import os
import time

unite_ppe_list = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z'
]


class Utils(object):

    @classmethod
    def serialize_one(cls, _query):
        """
        Serialize one query item
        """
        if _query is None:
            return None

        d = _query.__dict__
        item = {}
        for n in d.keys():
            if n != '_sa_instance_state' and n != 'geom':
                if isinstance(d[n], (datetime, date)):
                    item[n] = d[n].isoformat()
                else:
                    item[n] = d[n]

        return item

    @classmethod
    def serialize_many(cls, _query):
        """
        Serialize many query items
        """
        if _query is None:
            return None

        master = []
        for u in _query:
            d = u.__dict__
            item = {}
            for n in d.keys():
                if n != '_sa_instance_state' and n != 'geom':
                    if isinstance(d[n], (datetime, date)):
                        item[n] = d[n].isoformat()
                    else:
                        item[n] = d[n]
            master.append(item)
        return master

    @classmethod
    def get_model_record_attributes(cls, record):
        """
        Return model record parameters
        """
        return [a for a in dir(record) if not (a == 'id' or a.startswith('_'))] if record else []

    @classmethod
    def set_model_record(cls, record, params):
        """
        Set model record
        """
        atts = cls.get_model_record_attributes(record)

        for att in atts:
            if att != 'affaire_doc_file':
                val = params[att] if att in params else getattr(record, att)

                # Check boolean
                if val == 'true':
                    val = True
                if val == 'false':
                    val = False
                if val == "null" or val == "":
                    val = None

                setattr(record, att, val)

        return record

    @classmethod
    def get_data_save_response(cls, message):
        """
        Get data save response
        """
        return {'message': message}

    @classmethod
    def get_search_conditions(cls, model, params):
        """
        Get search conditions
        """
        conditions = list()

        for param in params:
            if param == 'matDiff':
                continue
            if param.startswith('_'):
                # pour les conditions NOT IN, p. ex. référencement numéros à affaire
                param = param[1:]
                conditions.append(~getattr(model, param).in_(json.loads(params["_"+param])))
            elif param.startswith('%'):
                # pour les conditions numérique qui contiennent un sous ensemble (p.ex. 101 est contenu dans 2101)
                param = param[1:]
                conditions.append(cast(getattr(model, param), String).like("%" + params["%"+param] + "%"))
            else:
                if params[param].isdigit() and not param == 'npa' and not param == 'no_access':
                    tmp = int(params[param])
                    conditions.append(getattr(model, param) == tmp)
                else:
                    conditions.append(func.lower(getattr(model, param)).like(
                        '%' + func.lower(params[param].replace('"', '')) + '%'))
        return conditions

    @classmethod
    def last_number(cls, request, cadastre_id, type_id, plan_id=None, affaire_id=None):
        """
        Get number_record with the highest number in cadastre and type
        to continue the numerotation
        """
        if not isinstance(type_id, list):
            type_id = [type_id]
        # Filter by type and cadastre
        query = request.dbsession.query(Numero).filter(
            and_(Numero.type_id.in_(type_id), Numero.cadastre_id == cadastre_id)
        )
        # If plan_id is specified, also filter by plan
        if plan_id:
            query = query.filter(Numero.plan_id == plan_id)
        if affaire_id:
            query = query.filter(
                and_(AffaireNumero.affaire_id == affaire_id, AffaireNumero.numero_id == Numero.id)
            )
        result = query.order_by(desc(Numero.numero)).limit(1).first()
        numero = result.numero if result else 0
        return numero

    @classmethod
    def last_number_mo(cls, request, cadastre_id, type_id, plan_id=None):
        """
        Return last number MO taking into account twin cadastres
        """
        query = request.dbsession.query(func.max(ReservationNumerosMO.numero_a)).filter(and_(
            ReservationNumerosMO.cadastre_id == cadastre_id,
            ReservationNumerosMO.type_id == type_id
        ))

        if plan_id:
            query = query.filter(ReservationNumerosMO.plan_id == plan_id)

        return 0 if query.first()[0] is None else query.first()[0]

    @classmethod
    def _params(cls, **kwargs):
        """
        Function that creates dictionnary with specified keys and values
        """
        params = dict()
        for key, value in kwargs.items():
            params[key] = value
        return params

    @classmethod
    def get_unite_from_index(cls, idx):
        """
        Get PPE unite from index
        """
        if idx == 0:
            unite = "A"
        else:
            n = len(unite_ppe_list)
            unite = ""
            c = 0
            while idx: 
                idx, idx_ = divmod(idx-c, n)
                unite = unite_ppe_list[idx_] + unite
                c = 1
        return unite

    @classmethod
    def get_index_from_unite(cls, unite):
        """
        Get index from PPE unite
        """
        n = len(unite_ppe_list)
        idx = 0
        c = 0
        for i, unite_i in enumerate(reversed(list(unite))):
            idx = idx + (unite_ppe_list.index(unite_i) + c) * n**i
            c = 1
        return idx

    @classmethod
    def get_fonctions_roles_by_id(cls, request, role_id):
        """
        Return fonctions roles by role id
        """
        results = []

        role = request.dbsession.query(Role).get(role_id)

        functions = role.fonctions

        for function in functions:
             results.append({
                'id': function.id,
                'nom': function.nom
            })

        return results

    @classmethod
    def has_permission(cls, request, fonction_name):
        if not check_connected(request):
            return False
        
        user_functions = get_user_functions(request)

        if fonction_name in user_functions['fonctions']:
            return True

        return False

    @classmethod
    def get_role_id_by_name(cls, request, role_name):
        query = request.dbsession.query(Role).filter(
            Role.nom == role_name).first()

        if query:
            return query.id

        return None

    @classmethod
    def create_affaire_folder(cls, request, affaire_folder):
        if not os.path.isdir(affaire_folder):
            copytree(request.registry.settings['affaireTemplateDir'], affaire_folder, ignore=ignore_patterns('Thumbs.db'))
            settime = time.time()
            os.utime(affaire_folder, times=(settime, settime))
    
    @classmethod
    def addNewRecord(cls, request, Model, params=None):
        """
        Create a new record in table Model. This is a general case, with no supplementary condition.
        Returns id of the new record.
        Uses params if set, request.params otherwise.
        """
        if params is None:
            params = request.params
        
        record = Model()
        record = cls.set_model_record(record, params)
        request.dbsession.add(record)
        request.dbsession.flush()
        return record


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
        if cl.no_sap is not None and int(cl.npa) not in request.registry.settings['npa_NE']:
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
