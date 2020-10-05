# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import VReservationNumerosMO, Plan, Affaire
from infolica.scripts.utils import Utils

from sqlalchemy import or_

import os
import json
from datetime import datetime



@view_config(route_name='reservation_numeros_mo_by_affaire_id', request_method='GET', renderer='json')
def reservation_numeros_mo_by_affaire_id_view(request):
    """
    Return all reservations_numeros_mo by affaire_id
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']
    query = request.dbsession.query(VReservationNumerosMO).filter(VReservationNumerosMO.affaire_id == affaire_id).all()
    return Utils.serialize_many(query)
