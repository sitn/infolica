from pyramid.view import view_config
from pyramid.response import Response
from ..scripts.utils import Utils
from ..models import Constant
import transaction

from sqlalchemy.exc import DBAPIError
from ..exceptions.custom_error import CustomError

from .. import models

import logging
log = logging.getLogger(__name__)


""" Return all numeros"""
@view_config(route_name='numeros', request_method='GET', renderer='json')
@view_config(route_name='numeros_s', request_method='GET', renderer='json')
def numeros_view(request):
    try:
        query = request.dbsession.query(models.VNumeros).all()
        return Utils.serialize_many(query)
    
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Return numeros by id"""
@view_config(route_name='numero_by_id', request_method='GET', renderer='json')
def numeros_by_id_view(request):
    try:
        # Get controle mutation id    
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.VNumeros).filter(models.VNumeros.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)
    

""" Add new numeros"""
@view_config(route_name='numeros', request_method='POST', renderer='json')
@view_config(route_name='numeros_s', request_method='POST', renderer='json')
def numeros_new_view(request, params=None):
    if not params: params=request.params
    
    #nouveau numero
    record = models.Numero()
    record = Utils.set_model_record(record, params)
    
    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))
            return record.id

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update numeros"""
@view_config(route_name='numeros', request_method='PUT', renderer='json')
@view_config(route_name='numeros_s', request_method='PUT', renderer='json')
def numeros_update_view(request):

    # Get numero id
    id = request.params['id'] if 'id' in request.params else None

    # Get numero record
    record = request.dbsession.query(models.Numero).filter(
        models.Numero.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Numero.__tablename__, id))

    last_record_etat_id = record.etat_id
    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            
            if 'etat_id' in request.params:
                if request.params['etat_id'] != last_record_etat_id:
                    params = Utils._params(numero_id=record.id, numero_etat_id=request.params['etat_id'])
                    numeros_etat_histo_new_view(request, params)
                                
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# NUMERO ETAT HISTO
###########################################################

""" Add new numero_etat_histo """
@view_config(route_name='numeros_etat_histo', request_method='POST', renderer='json')
@view_config(route_name='numeros_etat_histo_s', request_method='POST', renderer='json')
def numeros_etat_histo_new_view(request, params=None):
    if not params: params=request.params
    
    #nouveau numero
    record = models.NumeroEtatHisto()
    record = Utils.set_model_record(record, params)
    
    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.NumeroEtatHisto.__tablename__))
            return record.id

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# AFFAIRE-NUMERO
###########################################################

""" Return all numeros in affaire"""
@view_config(route_name='affaire_numeros_by_affaire_id', request_method='GET', renderer='json')
def affaire_numeros_view(request):
    affaire_id = request.matchdict["id"]
    try:
        records = request.dbsession.query(models.VNumerosAffaires).filter(models.VNumerosAffaires.affaire_id==affaire_id).all()
        return Utils.serialize_many(records)
    
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new affaire-numero """
@view_config(route_name='affaire_numeros', request_method='POST', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='POST', renderer='json')
def affaire_numero_new_view(request, params=None):
    if not params: params=request.params
    #nouveau affaire_numero
    record = models.AffaireNumero()
    record = Utils.set_model_record(record, params)
    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# NUMERO- AFFAIRE
###########################################################

""" Return all affaires touching one numero """
@view_config(route_name='numero_affaires_by_numero_id', request_method='GET', renderer='json')
def numeros_affaire_view(request):
    numero_id = request.matchdict['id']

    query = request.dbsession.query(models.VNumerosAffaires).filter(models.VNumerosAffaires.numero_id==numero_id).all()

    if not query:
        raise CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.VNumerosAffaires.__tablename__, numero_id)

    try:
        return Utils.serialize_many(query)
    
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)








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

