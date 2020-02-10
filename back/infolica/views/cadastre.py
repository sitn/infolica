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
# PREAVIS AFFAIRE
###########################################################

""" GET cadastre"""
@view_config(route_name='cadastres', request_method='GET', renderer='json')
@view_config(route_name='cadastres_s', request_method='GET', renderer='json')
def cadastre_view(request):
    try:
        records = request.dbsession.query(models.Cadastre).all()
        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

