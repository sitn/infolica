from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy import func, and_
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import os
from datetime import datetime

import logging
log = logging.getLogger(__name__)


###########################################################
# ETAPES AFFAIRE
###########################################################

""" GET etapes index"""
@view_config(route_name='etapes_index', request_method='GET', renderer='json')
@view_config(route_name='etapes_index_s', request_method='GET', renderer='json')
def etapes_index_view(request):
    try:
        records = request.dbsession.query(models.AffaireEtapeIndex).all()
        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" GET etapes affaire"""
@view_config(route_name='affaire_etapes_by_affaire_id', request_method='GET', renderer='json')
def affaires_etapes_view(request):
    affaire_id = request.matchdict['id']

    try:
        records = request.dbsession.query(models.VEtapesAffaires)\
            .filter(models.VEtapesAffaires.affaire_id == affaire_id).all()

        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" POST remarque affaire"""
@view_config(route_name='etapes', request_method='POST', renderer='json')
@view_config(route_name='etapes_s', request_method='POST', renderer='json')
def etapes_new_view(request):

    model = models.AffaireEtape()
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.AffaireEtape.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" DELETE remarque affaire"""
@view_config(route_name='etapes_by_id', request_method='DELETE', renderer='json')
def etapes_delete_view(request):
    affaire_etape_id = request.matchdict['id']

    record = request.dbsession.query(models.AffaireEtape).filter(
        models.AffaireEtape.id == affaire_etape_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.AffaireEtape.__tablename__, affaire_etape_id))

    try:
        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.AffaireEtape.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

