# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy import and_

from infolica.exceptions.custom_error import CustomError
from infolica.models.models import Affaire, GeosBalance, Numero
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

    query = request.dbsession.query(GeosBalance).filter(GeosBalance.mutation == mutation_name).all()

    return Utils.serialize_many(query)


@view_config(route_name='balance_check_existing_oldBF', request_method='POST', renderer='json')
def balance_check_existing_oldBF_new_view(request):
    """
    Check if oldBF already exist in DB and create it otherwise
    """
    # Check connected
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()
    
    oldBF = json.loads(request.params['oldBF'])

    # Control existance of each oldBF
    numero_obj = []
    for bf in oldBF:
        bf_cadastre_id, bf_numero = bf.split("_")
        query = request.dbsession.query(Numero).filter(and_(
            Numero.cadastre_id == bf_cadastre_id,
            Numero.numero == bf_numero
        )).first()

        # Create number if it doesn't exist
        if not query:
            numero = Numero(
                cadastre_id = bf_cadastre_id,
                type_id = request.registry.settings['numero_bf_id'],
                numero = bf_numero,
                etat_id = request.registry.settings['numero_vigueur_id']
            )
            
            request.dbsession.flush()
            numero_obj.append(numero)

        else:
            numero_obj.append(query)

    return Utils.serialize_many(numero_obj)
