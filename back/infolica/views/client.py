from pyramid.view import view_config
from pyramid.response import Response

from pyramid.view import exception_view_config

from pyramid.httpexceptions import (
    HTTPOk,
    HTTPException,
    HTTPBadRequest
)

from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

from copy import copy
from pprint import pprint

import logging
log = logging.getLogger(__name__)


def getBodyClient(params, model=None):
    # Create instance
    if model is None:
        model = models.Client()
    # Get form params
    model.id = int(params['id']) if 'id' in params else None
    model.entreprise = params['entreprise'] if 'entreprise' in params else None
    model.titre = params['titre'] if 'titre' in params else None
    model.nom = params['nom'] if 'nom' in params else None
    model.prenom = params['prenom'] if 'prenom' in params else None
    model.represente_par = params['represente_par'] if 'represente_par' in params else None
    model.adresse = params['adresse'] if 'adresse' in params else None
    model.npa = params['npa'] if 'npa' in params else None
    model.localite = params['localite'] if 'localite' in params else None
    model.case_postale = params['case_postale'] if 'case_postale' in params else None
    model.tel_fixe = params['tel_fixe'] if 'tel_fixe' in params else None
    model.fax = params['fax'] if 'fax' in params else None
    model.tel_portable = params['tel_portable'] if 'tel_portable' in params else None
    model.mail = params['mail'] if 'mail' in params else None
    model.entree = params['entree'] if 'entree' in params else None
    model.sortie = params['sortie'] if 'sortie' in params else None
    model.no_sap = params['no_sap'] if 'no_sap' in params else None
    model.no_bdp_bdee = params['no_bdp_bdee'] if 'no_bdp_bdee' in params else None
    model.type_client = int(params['type_client']) if 'type_client' in params else None
    return model

# def getBodyClient(post, model=None):
#     # Create instance
#     if model is None:
#         model = models.Client
#     # Get form params
#     model.entreprise = post.get('entreprise') if 'entreprise' in post else None
#     model.titre = post.get('titre') if 'titre' in post else None
#     model.nom = post.get('nom') if 'nom' in post else None
#     model.prenom = post.get('prenom') if 'prenom' in post else None
#     model.represente_par = post.get('represente_par') if 'represente_par' in post else None
#     model.adresse = post.get('adresse') if 'adresse' in post else None
#     model.npa = post.get('npa') if 'npa' in post else None
#     model.localite = post.get('localite') if 'localite' in post else None
#     model.case_postale = post.get('case_postale') if 'case_postale' in post else None
#     model.tel_fixe = post.get('tel_fixe') if 'tel_fixe' in post else None
#     model.fax = post.get('fax') if 'fax' in post else None
#     model.tel_portable = post.get('tel_portable') if 'tel_portable' in post else None
#     model.mail = post.get('mail') if 'mail' in post else None
#     model.entree = post.get('entree') if 'entree' in post else None
#     model.sortie = post.get('sortie') if 'sortie' in post else None
#     model.no_sap = post.get('no_sap') if 'no_sap' in post else None
#     model.no_bdp_bdee = post.get('no_bdp_bdee') if 'no_bdp_bdee' in post else None
#     model.type_client = int(post.get('type_client')) if 'type_client' in post else None
#     return model


""" Return all types clients"""
@view_config(route_name='types_clients', request_method='GET', renderer='json')
@view_config(route_name='types_clients_s', request_method='GET', renderer='json')
def types_clients_view(request):
    try:
        query = request.dbsession.query(models.ClientType).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return all clients"""
@view_config(route_name='clients', request_method='GET', renderer='json')
@view_config(route_name='clients_s', request_method='GET', renderer='json')
def clients_personnes_view(request):
    result = []
    try:
        query = request.dbsession.query(models.Client).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return client by id"""
@view_config(route_name='client_by_id', request_method='GET', renderer='json')
def client_personne_by_id_view(request):
    merged = None
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Client).filter(models.Client.id == id).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_one(query)


""" Add new client"""
@view_config(route_name='clients', request_method='POST', renderer='json')
@view_config(route_name='clients_s', request_method='POST', renderer='json')
def clients_new_view(request):
    # Get client instance
    model = Utils.set_model_record(models.Client(), request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            request.dbsession.flush()
            print("model.id = ", model.id)
            transaction.commit()
            return HTTPOk("POST Client OK")

    except Exception as e:
        print(e)
        raise e
    

""" Update client"""
@view_config(route_name='clients', request_method='PUT', renderer='json')
@view_config(route_name='clients_s', request_method='PUT', renderer='json')
def clients_update_view(request):
    # Get client_id
    id_client = int(request.params['id']) if 'id' in request.params else None

    query = request.dbsession.query(models.Client).filter(
            models.Client.id == id_client)
    
    lastmodel = query.first()
    model = copy(lastmodel)

    # If result is empty
    if not lastmodel:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Client.__tablename__, id_client))
    
    # Read params client
    model = Utils.set_model_record(model, request.params)

    # If no change
    if model == lastmodel:
        print("Models are identical")
        raise CustomError(CustomError.UPDATE_NO_CHANGE_RECORDED.format(id_client, models.Client.__tablename__))
    lastmodel = None

    try:
        with transaction.manager:
            model = Utils.serialize_one(model)
            pprint(model)
            query.update(model)
            transaction.commit()
            return HTTPOk("PULL Client OK")
        
    except Exception as e:
        print(e)
        raise e


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
