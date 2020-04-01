from datetime import time, date, datetime
from sqlalchemy import func, and_, desc
from .. import models
from ..scripts.ldap_query import LDAPQuery


unite_ppe_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class Utils():

    """ Serialize one query item"""
    @classmethod
    def serialize_one(cls, _query):
        d = _query.__dict__
        item = {}
        for n in d.keys():
            if n != '_sa_instance_state':
                if isinstance(d[n], (datetime, date)):
                    item[n] = d[n].isoformat()
                else:
                    item[n] = d[n]

        return item

    """ Serialize many query items"""
    @classmethod
    def serialize_many(cls, _query):
        master = []
        item = {}
        x = 0
        for u in _query:
            d = u.__dict__
            item = {}
            for n in d.keys():
                if n != '_sa_instance_state':
                    if isinstance(d[n], (datetime, date)):
                        item[n] = d[n].isoformat()
                    else:
                        item[n] = d[n]
            master.append(item)
        return master

    """ Return model record parameters """
    @classmethod
    def get_model_record_attributes(cls, record):
        return [a for a in dir(record) if not (a == 'id' or a.startswith('_'))] if record else []

    """ Set model record"""
    @classmethod
    def set_model_record(cls, record, params):
        atts = cls.get_model_record_attributes(record)

        for att in atts:
            val = params[att] if att in params else None

            #Chek boolean
            if val == 'true':
                val = True
            elif val == 'false':
                val = False

            setattr(record, att, val)

        return record

    """ Get data save response"""
    @classmethod
    def get_data_save_response(cls, message):
        return {'message': message}

    """ Get search conditions """
    @classmethod
    def get_search_conditions(cls, model, params):
        conditions = list()

        for param in params:
            if params[param].isdigit():
                tmp = int(params[param])
                conditions.append(getattr(model, param) == tmp)
            else:
                conditions.append(func.lower(getattr(model, param)).like(
                    '%' + func.lower(params[param].replace('"','')) + '%'))
        return conditions


    """ Get number_record with the highest number in cadastre and type to continue the numerotation """
    @classmethod
    def last_number(cls, request, cadastre_id, type_id, plan_id=None, affaire_id=None):
        if not isinstance(type_id, list):
            type_id = [type_id]
        # Filter by type and cadastre
        query = request.dbsession.query(models.Numero).filter(and_(models.Numero.type_id.in_(type_id), models.Numero.cadastre_id==cadastre_id))
        # If plan_id is specified, also filter by plan
        if plan_id:
            query = query.filter(models.Numero.plan_id==plan_id)
        if affaire_id:
            query = query.filter(and_(models.AffaireNumero.affaire_id==affaire_id, models.AffaireNumero.numero_id==models.Numero.id))
        result = query.order_by(desc(models.Numero.numero)).limit(1).first()
        numero = result.numero if result else 0
        return numero


    """ Function that creates dictionnary with specified keys and values """
    @classmethod
    def _params(cls, **kwargs):
        params = dict()
        for key, value in kwargs.items():
            params[key] = value
        return params


    """ Get PPE unite from index """
    @classmethod
    def get_unite_from_index(cls, idx):
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

    """ Get index from PPE unite """
    @classmethod
    def get_index_from_unite(cls, unite):
        n = len(unite_ppe_list)
        idx = 0
        c = 0
        for i, unite_i in enumerate(reversed(list(unite))):
            idx = idx + (unite_ppe_list.index(unite_i) + c) * n**i
            c = 1
        return idx

    """ Return fonctions roles by role id"""

    @classmethod
    def get_fonctions_roles_by_id(cls, request, role_id):
        results = []
        try:
            query = request.dbsession.query(models.Fonction, models.Role, models.FonctionRole).filter(
                models.Role.id == role_id).filter(models.Role.id == models.FonctionRole.role_id).filter(
                models.Fonction.id == models.FonctionRole.fonction_id).all()

            for f, r, fr in query:
                one_item = {}
                one_item["id"] = f.id
                one_item["nom"] = f.nom

                results.append(one_item)

            return results

        except Exception as e:
            raise e

    @classmethod
    def get_fonctions_roles_by_name(cls, request, role_name):
        results = []
        try:
            query = request.dbsession.query(models.Fonction, models.Role, models.FonctionRole).filter(
                models.Role.nom == role_name).filter(models.Role.id == models.FonctionRole.role_id).filter(
                models.Fonction.id == models.FonctionRole.fonction_id).all()

            for f, r, fr in query:
                one_item = {}
                one_item["id"] = f.id
                one_item["nom"] = f.nom

                results.append(one_item)

            return results

        except Exception as e:
            raise e

    @classmethod
    def has_permission(cls, request, fonction_name):

        try:
            if not cls.check_connected(request):
               return False

            user_dn = request.authenticated_userid

            if not user_dn:
                return False

            role_name = LDAPQuery.get_user_group_by_dn(request, user_dn)

            fonctions = cls.get_fonctions_roles_by_name(request, role_name)
            fonctions_names = [x for x in fonctions if x["nom"] == fonction_name]
            return len(fonctions_names) > 0

        except Exception as e:
            raise e

    @classmethod
    def check_connected(cls, request):
        try:
            auth_tkt = request.cookies.get('auth_tkt', default=None)

            if not auth_tkt:
                return False

            return True

        except Exception as e:
            raise e


    @classmethod
    def get_role_id_by_name(cls, request, role_name):
        try:
            query = request.dbsession.query(models.Role).filter(
                models.Role.nom == role_name).first()

            if query:
                return query.id

        except Exception as e:
            raise e

        return None