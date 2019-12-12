from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant

import logging
log = logging.getLogger(__name__)


""" Return all clients"""
@view_config(route_name='clients', request_method='GET', renderer='json')
@view_config(route_name='clients_s', request_method='GET', renderer='json')
def clients_view(request):
    try:
        query = request.dbsession.query(models.Client).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return query


""" Return client by id"""
@view_config(route_name='client_by_id', request_method='GET', renderer='json')
def client_by_id_view(request):
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Client, models.ClientPersonne, models.ClientEntreprise).filter(
            models.Client.id == id).filter(models.Client.id == models.ClientPersonne.id).filter(
            models.Client.id == models.ClientEntreprise).first()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return query


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
        type = None

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

        with transaction.manager:
            model = models.Client(
                adresse = adresse,
                npa = npa,
                localite = localite,
                tel_fixe = tel_fixe,
                mail = mail,
                entree = entree,
                sortie = sortie,
                type = type
            )

            request.dbsession.add(model)
            request.dbsession.flush()
            max_client_id = model.id

            # Read params client entreprise
            if type == settings['type_entreprise']:
                if 'nom' in request.params:
                    model_e = models.ClientEntreprise(
                        id = max_client_id,
                        nom = request.params['nom']
                    )
                    request.dbsession.add(model_e)


            # Read params client personne
            elif type == settings['type_personne']:
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

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Constant.success_save





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
