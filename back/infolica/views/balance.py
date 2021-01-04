# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.models import Affaire, GeosBalance
from infolica.scripts.utils import Utils
from infolica.scripts.mailer import send_mail

import os
import json
from docx.api import Document


@view_config(route_name='balance_generate_table', request_method='GET', renderer='json')
def balance_generate_table_view(request):
    """
    Generate table balance 
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    send_mail(request, [request.registry.settings["infolica_balance_mail"]], "Génération Balance Infolica\nMail généré automatiquement", "Infolica-Balance")
    return "ok"
    

@view_config(route_name='balance_mutation_names', request_method='GET', renderer='json')
def balance_mutation_names_view(request):
    """
    Get balance by mutation names
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(GeosBalance.mutation).group_by(GeosBalance.mutation).all()

    query = [i[0] for i in query]
    return json.dumps(query)


@view_config(route_name='balance_by_affaire_id', request_method='GET', renderer='json')
def balance_view(request):
    """
    Return balance ef affaire from table GEOS
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()
    
    mutation_name = request.params["mutation_name"] if "mutation_name" in request.params else None
    
    if not mutation_name:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(GeosBalance.__tablename__, mutation_name))
