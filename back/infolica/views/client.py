from pyramid.view import view_config
from pyramid.response import Response

from pyramid.view import exception_view_config

from pyramid.httpexceptions import (
    HTTPException,
    HTTPBadRequest
)

from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils


import logging
log = logging.getLogger(__name__)


""" Return all types clients"""
@view_config(route_name='types_clients', request_method='GET', renderer='json')
@view_config(route_name='types_clients_s', request_method='GET', renderer='json')
def types_clients_view(request):
    try:
        query = request.dbsession.query(models.ClientType).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)

""" Return all clients personnes"""
@view_config(route_name='clients_personnes', request_method='GET', renderer='json')
@view_config(route_name='clients_personnes_s', request_method='GET', renderer='json')
def clients_personnes_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Client, models.ClientPersonne).filter(models.Client.id == models.ClientPersonne.id).all()

        if query:
            for c, cp in query:
                merged = dict()
                merged.update(Utils.serialize_one(c))
                merged.update(Utils.serialize_one(cp))
                result.append(merged)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return result#Utils.serialize_many(result)


""" Return client personne by id"""
@view_config(route_name='client_personne_by_id', request_method='GET', renderer='json')
def client_personne_by_id_view(request):
    merged = None
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Client, models.ClientPersonne).filter(models.Client.id == models.ClientPersonne.id).first()

        if query:
            merged = dict()
            merged.update(Utils.serialize_one(query[0]))
            merged.update(Utils.serialize_one(query[1]))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return merged

""" Return all clients entreprise"""
@view_config(route_name='clients_entreprises', request_method='GET', renderer='json')
@view_config(route_name='clients_entreprises_s', request_method='GET', renderer='json')
def clients_entreprises_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Client, models.ClientEntreprise).filter(models.Client.id == models.ClientEntreprise.id).all()

        if query:
            for c, ce in query:
                merged = dict()
                merged.update(Utils.serialize_one(c))
                merged.update(Utils.serialize_one(ce))
                result.append(merged)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return result#Utils.serialize_many(result)


""" Return client entreprise by id"""
@view_config(route_name='client_entreprise_by_id', request_method='GET', renderer='json')
def client_entreprise_by_id_view(request):
    merged = None
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Client, models.ClientEntreprise).filter(models.Client.id == models.ClientEntreprise.id).first()

        if query:
            merged = dict()
            merged.update(Utils.serialize_one(query[0]))
            merged.update(Utils.serialize_one(query[1]))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return merged


""" Add new client"""
@view_config(route_name='clients', request_method='POST', renderer='json')
@view_config(route_name='clients_s', request_method='POST', renderer='json')
def clients_new_view(request):
    try:
        settings = request.registry.settings

        # Read params client
        adresse = None
        npa = None
        localite = None
        tel_fixe = None
        mail = None
        entree = None
        sortie = None
        type_client = None

        if 'adresse' in request.params:
            adresse = request.params['adresse']

        if 'npa' in request.params:
            npa = request.params['npa']

        if 'localite' in request.params:
            localite = request.params['localite']

        if 'tel_fixe' in request.params:
            tel_fixe = request.params['tel_fixe']

        if 'mail' in request.params:
            mail = request.params['mail']

        if 'entree' in request.params:
            entree = request.params['entree']

        if 'sortie' in request.params:
            sortie = request.params['sortie']

        if 'type_client' in request.params:
            type_client = request.params['type_client']

        with transaction.manager:

            model = models.Client(
                adresse=adresse,
                npa = npa,
                localite = localite,
                tel_fixe = tel_fixe,
                mail = mail,
                entree = entree,
                sortie = sortie,
                type_client = int(type_client)
            )

            request.dbsession.add(model)
            request.dbsession.flush()
            max_client_id = model.id

            # Read params client entreprise
            if int(type_client) == int(settings['type_entreprise']):
                if 'nom' in request.params:
                    model_e = models.ClientEntreprise(
                        id = max_client_id,
                        nom = request.params['nom']
                    )
                    request.dbsession.add(model_e)


            # Read params client personne
            elif int(type_client) == int(settings['type_personne']):
                titre = None
                nom = None
                prenom = None
                tel_portable = None

                if 'titre' in request.params:
                    titre = request.params['titre']

                if 'nom' in request.params:
                    nom = request.params['nom']

                if 'prenom' in request.params:
                    prenom = request.params['prenom']

                if 'tel_portable' in request.params:
                    tel_portable = request.params['tel_portable']

                model_p = models.ClientPersonne(
                    id = max_client_id,
                    titre = titre,
                    nom = nom,
                    prenom = prenom,
                    tel_portable = tel_portable
                )
                request.dbsession.add(model_p)

            # Commit transaction
            transaction.commit()

    except Exception as e:
        raise e
    return Constant.SUCCESS_SAVE


""" Update client"""
@view_config(route_name='clients', request_method='PUT', renderer='json')
@view_config(route_name='clients_s', request_method='PUT', renderer='json')
def clients_update_view(request):
    try:
        settings = request.registry.settings
        client_record = None

        # Read params client
        id_client = None
        adresse = None
        npa = None
        localite = None
        tel_fixe = None
        mail = None
        entree = None
        sortie = None
        type = None

        if 'id_client' in request.params:
            id_client = request.params['id_client']

        if 'adresse' in request.params:
            adresse = request.params['adresse']

        if 'npa' in request.params:
            npa = request.params['npa']

        if 'localite' in request.params:
            localite = request.params['localite']

        if 'tel_fixe' in request.params:
            tel_fixe = request.params['tel_fixe']

        if 'mail' in request.params:
            mail = request.params['mail']

        if 'entree' in request.params:
            entree = request.params['entree']

        if 'sortie' in request.params:
            sortie = request.params['sortie']

        if 'type' in request.params:
            type = request.params['type']

        # Get the client
        client_record = request.dbsession.query(models.Client).filter(
                models.Client.id == id_client).first()

        if not client_record:
            raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Perturbation.__tablename__, id_client))

        with transaction.manager:

            client_record.adresse = adresse
            client_record.npa = npa
            client_record.localite = localite
            client_record.tel_fixe = tel_fixe
            client_record.mail = mail
            client_record.entree = entree
            client_record.sortie = sortie
            client_record.type = type


            # Read params client entreprise
            if type == settings['type_entreprise']:
                if 'nom' in request.params:
                    entreprise_record = request.dbsession.query(models.ClientEntreprise).filter(
                        models.ClientEntreprise.id == id_client).first()
                    if entreprise_record:
                        entreprise_record.nom = request.params['nom']

            # Read params client personne
            elif type == settings['type_personne']:

                personne_record = request.dbsession.query(models.ClientPersonne).filter(
                    models.ClientPersonne.id == id_client).first()

                if personne_record:

                    titre = None
                    nom = None
                    prenom = None
                    tel_portable = None

                    if 'titre' in request.params:
                        titre = request.params['titre']

                    if 'nom' in request.params:
                        nom = request.params['nom']

                    if 'prenom' in request.params:
                        prenom = request.params['prenom']

                    if 'tel_portable' in request.params:
                        tel_portable = request.params['tel_portable']

                    personne_record.titre = titre
                    personne_record.nom = nom
                    personne_record.prenom = prenom
                    personne_record.tel_portable = tel_portable

            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Constant.SUCCESS_SAVE



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
