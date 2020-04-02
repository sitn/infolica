from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.httpexceptions import HTTPForbidden

from ..scripts.utils import Utils
from ..models import Constant
import transaction
from sqlalchemy import and_, desc

import json

from sqlalchemy.exc import DBAPIError
from ..exceptions.custom_error import CustomError

from .. import models
from ..views.numero import affaire_numero_new_view, numeros_etat_histo_new_view

import logging
log = logging.getLogger(__name__)


""" Add numéro muté in affaire"""
@view_config(route_name='reference_numeros', request_method='POST', renderer='json')
@view_config(route_name='reference_numeros_s', request_method='POST', renderer='json')
def reference_numeros_new_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise HTTPForbidden()

        # Get affaire_id
        affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
        numeros_liste = json.loads(
            request.params['numeros_liste']) if 'numeros_liste' in request.params else None

        for numero_i in numeros_liste:
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_i['numero_id'], modifie=False, type_id=1)
            affaire_numero_new_view(request, params)

        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Delete numéro muté in affaire"""
@view_config(route_name='reference_numeros', request_method='DELETE', renderer='json')
@view_config(route_name='reference_numeros_s', request_method='DELETE', renderer='json')
def reference_numeros_delete_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise HTTPForbidden()

        # Get affaire_id and numero_id
        affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
        numero_id = request.params['numero_id'] if 'numero_id' in request.params else None

        # supprimer le lien affaire-numéro
        affNum = request.dbsession.query(models.AffaireNumero).filter(and_(
            models.AffaireNumero.affaire_id == affaire_id, models.AffaireNumero.numero_id == numero_id)).first()

        with transaction.manager:
            request.dbsession.delete(affNum)
            transaction.commit()

        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
