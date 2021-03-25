# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy import and_

from infolica.exceptions.custom_error import CustomError
from infolica.models.models import Affaire, GeosBalance, Numero, NumeroEtatHisto, AffaireNumero
from infolica.scripts.utils import Utils
from infolica.scripts.mailer import send_mail

import os
import json
from docx.api import Document
from datetime import datetime


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
    
    affaire_id = request.params['affaire_id']
    oldBF = json.loads(request.params['oldBF'])

    # Control existance of each oldBF
    numero_obj = []
    for bf in oldBF:
        bf_cadastre_id, bf_numero = bf.split("_")
        numero = request.dbsession.query(Numero).filter(and_(
            Numero.cadastre_id == bf_cadastre_id,
            Numero.numero == bf_numero
        )).first()

        # Create number if it doesn't exist
        if not numero:
            numero = Numero(
                cadastre_id = bf_cadastre_id,
                type_id = request.registry.settings['numero_bf_id'],
                numero = bf_numero,
                etat_id = request.registry.settings['numero_vigueur_id']
            )
            
            request.dbsession.flush()

        # Add numero to array of Numeros created
        numero_obj.append(numero)
        
        # Add numero_affaire link
        affnum_exists = request.dbsession.query(AffaireNumero).filter(and_(
            AffaireNumero.numero_id == numero.id,
            AffaireNumero.affaire_id == affaire_id
        )).first()
        toto
        affNum = AffaireNumero(
            affaire_id = affaire_id,
            numero_id = numero.id,
            type_id = request.registry.settings['numero_bf_id'],
            actif = True
        )
        request.dbsession.add(affNum)

        # Add numero_etat_histo link
        numEtatHisto = NumeroEtatHisto(
            numero_id = numero.id,
            numero_etat_id = request.registry.settings['numero_vigueur_id'],
            date = datetime.now().date()
        )
        request.dbsession.add(numEtatHisto)

    return Utils.serialize_many(numero_obj)



@view_config(route_name='balance_from_file_by_affaire_id', request_method='GET', renderer='json')
def balance_from_file_view(request):
    """
    Return balance
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params["affaire_id"] if 'affaire_id' in request.params else None
    affaires_directory = request.registry.settings['affaires_directory']
    balance_file_rel_path = request.registry.settings['balance_file_rel_path'].encode("latin1").decode()
    balance_filename_prefix = request.registry.settings['balance_filename_prefix']

    # Get affaire path and search file
    query = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first()
    path = os.path.normcase(os.path.join(affaires_directory, query.chemin, balance_file_rel_path))

    fileExists = False
    for filename in os.listdir(path):
        if filename.startswith(balance_filename_prefix) and (filename.endswith(".doc") or filename.endswith(".docx")):
            fileExists = True
            break
    
    if not fileExists:
        raise CustomError(CustomError.FILE_NOT_FOUND.format('Des_XXX.docx'))
    
    input_file = os.path.join(path, filename)
    
    # Open balance file and get table of balance
    doc = Document(input_file)
    table = None
    for table in doc.tables:
        if "ancien" in table.rows[0].cells[0].text:
            break
    
    lastBF = []
    balance = []
    for i, row in enumerate(table.rows[1:]):

        text = list(cell.text for cell in row.cells)
        
        if i == 0:
            lastBF = text
            continue
        
        for j, text_i in enumerate(text):
            if j >= 2 and text_i.isnumeric() and not text[0] == "":
                balance.append({
                        "new": int(lastBF[j]) if lastBF[j].isnumeric() else lastBF[j],
                        "old": int(text[0]) if text[0].isnumeric() else text[0]
                    })
    
    return json.dumps(balance)


