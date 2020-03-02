from datetime import time, date, datetime
from sqlalchemy import func, and_, desc
from .. import models


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

