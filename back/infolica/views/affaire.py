from pyramid.view import view_config
from pyramid.response import Response
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
# AFFAIRE
###########################################################

""" Return all affaires"""
@view_config(route_name='affaires', request_method='GET', renderer='json')
@view_config(route_name='affaires_s', request_method='GET', renderer='json')
def affaires_view(request):
    try:
        query = request.dbsession.query(models.VAffaire).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        print(e)
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)



""" Return affaires by id"""
@view_config(route_name='affaire_by_id', request_method='GET', renderer='json')
def affaire_by_id_view(request):
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.VAffaire)
        one = query.filter(models.VAffaire.id == id).first()
        return Utils.serialize_one(one)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Search affaires"""
@view_config(route_name='recherche_affaires', request_method='GET', renderer='json')
@view_config(route_name='recherche_affaires_s', request_method='GET', renderer='json')
def affaires_search_view(request):
    try:
        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(models.VAffaire, request.params)
        query = request.dbsession.query(models.VAffaire).filter(*conditions).all()[:search_limit]
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)

""" Return all types affaires"""
@view_config(route_name='types_affaires', request_method='GET', renderer='json')
@view_config(route_name='types_affaires_s', request_method='GET', renderer='json')
def types_affaires_view(request):
    try:
        query = request.dbsession.query(models.AffaireType).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)



""" Add new affaire"""
@view_config(route_name='affaires', request_method='POST', renderer='json')
def affaires_new_view(request):

    model = models.Affaire()
    model = Utils.set_model_record(model, request.params)
    
    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update affaire"""
@view_config(route_name='affaires', request_method='PUT', renderer='json')
@view_config(route_name='affaires_s', request_method='PUT', renderer='json')
def affaires_update_view(request):
    # id_affaire
    id_affaire = request.params['id_affaire'] if 'id_affaire' in request.params else None

    # Get the affaire
    record = request.dbsession.query(models.Affaire).filter(
        models.Affaire.id == id_affaire).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))

    record = Utils.set_model_record(record, request.params)
    
    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


# """ Delete affaire"""
# @view_config(route_name='affaire_by_id', request_method='DELETE', renderer='json')
# def affaires_delete_view(request):
#     # id_affaire
#     id_affaire = request.params['id_affaire'] if 'id_affaire' in request.params else None

#     # Get the affaire
#     record = request.dbsession.query(models.Affaire).filter(
#         models.Affaire.id == id_affaire).first()

#     if not record:
#         raise CustomError(
#             CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))
    
#     try:
#         with transaction.manager:
#             request.dbsession.delete(record)
#             # Commit transaction
#             transaction.commit()
#             return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Affaire.__tablename__))

#     except DBAPIError as e:
#         log.error(e)
#         return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# REMARQUES AFFAIRE
###########################################################

""" GET remarque affaire"""
@view_config(route_name='affaires_remarques_by_affaire_id', request_method='GET', renderer='json')
def affaires_remarques_view(request):
    affaire_id = request.matchdict['id']

    try:
        records = request.dbsession.query(models.RemarqueAffaire, models.Operateur)\
            .filter(models.RemarqueAffaire.affaire_id==affaire_id)\
            .filter(models.RemarqueAffaire.operateur_id==models.Operateur.id).all()

        ra_json = list()
        for ra, op in records:
            ra_json.append(Utils._params(nom=op.nom, prenom=op.prenom, remarque=ra.remarque, date=ra.date.isoformat()))

        return ra_json

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" POST remarque affaire"""
@view_config(route_name='affaires_remarques', request_method='POST', renderer='json')
@view_config(route_name='affaires_remarques_s', request_method='POST', renderer='json')
def affaires_remarques_new_view(request):

    model = models.RemarqueAffaire()
    model = Utils.set_model_record(model, request.params)
    
    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.RemarqueAffaire.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# ETAPES AFFAIRE
###########################################################

""" GET etapes affaire"""
@view_config(route_name='affaires_etapes_by_affaire_id', request_method='GET', renderer='json')
def affaires_etapes_view(request):
    affaire_id = request.matchdict['id'] 

    try:
        records = request.dbsession.query(models.VEtapesAffaires)\
            .filter(models.VEtapesAffaires.affaire_id==affaire_id).all()

        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" POST remarque affaire"""
@view_config(route_name='affaires_etapes', request_method='POST', renderer='json')
@view_config(route_name='affaires_etapes_s', request_method='POST', renderer='json')
def affaires_etapes_new_view(request):

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
        return Response(db_err_msg, content_type='text/plain', status=500)


""" DELETE remarque affaire"""
@view_config(route_name='affaires_etapes_by_affaire_id', request_method='DELETE', renderer='json')
def affaires_etapes_delete_view(request):
    affaire_etape_id = request.matchdict['id']

    record = request.dbsession.query(models.AffaireEtape).filter(models.AffaireEtape.id==affaire_etape_id).first()
    
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
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# PREAVIS AFFAIRE
###########################################################

""" GET preavis affaire"""
@view_config(route_name='affaires_preavis_by_affaire_id', request_method='GET', renderer='json')
def affaires_preavis_view(request):
    affaire_id = request.matchdict['id']

    try:
        records = request.dbsession.query(models.VAffairesPreavis)\
            .filter(models.VAffairesPreavis.affaire_id==affaire_id).all()

        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" POST preavis affaire"""
@view_config(route_name='affaires_preavis', request_method='POST', renderer='json')
@view_config(route_name='affaires_preavis_s', request_method='POST', renderer='json')
def affaires_preavis_new_view(request):

    model = models.Preavis()
    model = Utils.set_model_record(model, request.params)
    
    try:
        with transaction.manager:
            request.dbsession.add(model)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" UPDATE preavis affaire"""
@view_config(route_name='affaires_preavis', request_method='PUT', renderer='json')
@view_config(route_name='affaires_preavis_s', request_method='PUT', renderer='json')
def affaires_preavis_update_view(request):
    preavis_id = request.params['id'] if 'id' in request.params else None
    print(preavis_id)
    record = request.dbsession.query(models.Preavis).filter(models.Preavis.id==preavis_id).first()
    print ("toto")
    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

    record = Utils.set_model_record(record, request.params)
    
    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" DELETE preavis affaire"""
@view_config(route_name='affaires_preavis_by_affaire_id', request_method='DELETE', renderer='json')
def affaires_preavis_delete_view(request):
    preavis_id = request.matchdict['id']

    record = request.dbsession.query(models.Preavis).filter(models.Preavis.id==preavis_id).first()
    
    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Preavis.__tablename__, preavis_id))

    try:
        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Preavis.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# DOCUMENTS (LISTE) AFFAIRE
###########################################################

""" GET documents affaire"""
@view_config(route_name='affaires_documents_by_affaire_id', request_method='GET', renderer='json')
def affaires_documents_view(request):
    affaire_id = request.matchdict['id']
    
    doc_path = os.path.join(Constant.AFFAIRE_DIRECTORY, affaire_id)
    documents = list()
    for root, dirs, files in os.walk(doc_path):
        for file_i in files:
            file_path = os.path.join(root, file_i)
            documents.append(Utils._params(nom=file_i, dossier=os.path.relpath(root, doc_path), chemin=file_path, creation=datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d.%m.%Y")))


    return documents







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
