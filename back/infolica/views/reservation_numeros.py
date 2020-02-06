from copy import copy
from pyramid.view import view_config
from pyramid.response import Response
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from sqlalchemy import and_, desc

from sqlalchemy.exc import DBAPIError
from ..exceptions.custom_error import CustomError

from .. import models
from ..views.numero import numeros_new_view, affaire_numero_new_view, numeros_etat_histo_new_view

import logging
log = logging.getLogger(__name__)


""" Return all numeros in affaire"""
@view_config(route_name='reservation_numeros', request_method='GET', renderer='json')
@view_config(route_name='reservation_numeros_s', request_method='GET', renderer='json')
def reservation_numeros_view(request):
    # Get affaire_id
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None

    try:
        query = request.dbsession.query(models.VNumeros).filter(and_(
            models.AffaireNumero.affaire_id == affaire_id, models.VNumeros.id == models.AffaireNumero.numero_id)).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new numeros in affaire"""
@view_config(route_name='reservation_numeros', request_method='POST', renderer='json')
@view_config(route_name='reservation_numeros_s', request_method='POST', renderer='json')
def reservation_numeros_new_view(request):
    # Get affaire_id
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    cadastre_id = request.params['cadastre_id'] if 'cadastre_id' in request.params else None
    plan_id = request.params['plan_id'] if 'plan_id' in request.params else None

    # Get first available number (BF, DDP, PPE, PCOP)
    ln = Utils.last_number(request, cadastre_id, [1, 2, 3, 4])

    c = 0
    # Biens-fonds
    try:
        if 'bf' in request.params:
            for i in range(int(request.params['bf'])):
                c += 1
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=1, etat_id=1, numero=ln + c)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)
                # enregistrer l'historique de l'état
                params = Utils._params(numero_id=numero_id, numero_etat_id=1)
                numeros_etat_histo_new_view(request, params)

        if 'ddp' in request.params:
            for i in range(int(request.params['ddp'])):
                c += 1
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=2, etat_id=1, numero=ln + c)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)
                # enregistrer l'historique de l'état
                params = Utils._params(numero_id=numero_id, numero_etat_id=1)
                numeros_etat_histo_new_view(request, params)

        if 'ppe' in request.params:
            unite_start_idx = Utils.get_index_from_unite(
                request.params["ppe_unite"]) if "ppe_unite" in request.params else 0
            for i in range(int(request.params['ppe'])):
                c += 1
                # enregistrer un nouveau numéro
                suffixe = Utils.get_unite_from_index(unite_start_idx + i)
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=3, etat_id=1, numero=ln + c, suffixe=suffixe)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)
                # enregistrer l'historique de l'état
                params = Utils._params(numero_id=numero_id, numero_etat_id=1)
                numeros_etat_histo_new_view(request, params)

        if 'pcop' in request.params:
            for i in range(int(request.params['pcop'])):
                c += 1
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=4, etat_id=1, numero=ln + c, suffixe="part")
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)
                # enregistrer l'historique de l'état
                params = Utils._params(numero_id=numero_id, numero_etat_id=1)
                numeros_etat_histo_new_view(request, params)

        if 'pfp3' in request.params:
            ln = Utils.last_number(request, cadastre_id, [5])
            for i in range(int(request.params['pfp3'])):
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=5, etat_id=2, numero=ln + i+1)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)

        if 'bat' in request.params:
            ln = Utils.last_number(request, cadastre_id, [6])
            for i in range(int(request.params['bat'])):
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=6, etat_id=2, numero=ln + i+1)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)

        if 'pcs' in request.params:
            ln = Utils.last_number(request, cadastre_id, [7])
            for i in range(int(request.params['pcs'])):
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=7, etat_id=2, numero=ln + i+1)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)

        if 'paux' in request.params:
            ln = Utils.last_number(request, cadastre_id, [8], plan_id=plan_id)
            for i in range(int(request.params['paux'])):
                # enregistrer un nouveau numéro
                params = Utils._params(
                    cadastre_id=cadastre_id, type_id=8, etat_id=2, numero=ln + i+1, plan_id=plan_id)
                numero_id = numeros_new_view(request, params)
                # enregistrer le lien affaire-numéro
                params = Utils._params(
                    affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
                affaire_numero_new_view(request, params)

        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
