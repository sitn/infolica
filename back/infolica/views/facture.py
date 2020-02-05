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


###########################################################
# FACTURE
###########################################################

""" Return all factures"""
@view_config(route_name='factures', request_method='GET', renderer='json')
@view_config(route_name='factures_s', request_method='GET', renderer='json')
def factures_view(request):
    try:
        query = request.dbsession.query(models.Facture).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Return all factures in affaire"""
@view_config(route_name='affaires_factures_by_affaire_id', request_method='GET', renderer='json')
def affaires_factures_view(request):
    affaire_id = request.matchdict["id"]

    try:
        query = request.dbsession.query(models.Facture)\
            .filter(models.Facture.affaire_id == affaire_id).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new facture"""
@view_config(route_name='factures', request_method='POST', renderer='json')
@view_config(route_name='factures_s', request_method='POST', renderer='json')
def factures_new_view(request):
    model = models.Facture()
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Facture.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update facture"""
@view_config(route_name='factures', request_method='PUT', renderer='json')
@view_config(route_name='factures_s', request_method='PUT', renderer='json')
def factures_update_view(request):
    # id_facture
    id_facture = None

    if 'id_facture' in request.params:
        id_facture = request.params['id_facture']

    # Get the facture
    facture_record = request.dbsession.query(models.Facture).filter(
        models.Facture.id == id_facture).first()

    if not facture_record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id_facture))

    facture_record = Utils.set_model_record(facture_record, request.params)

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Facture.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Delete facture"""
@view_config(route_name='facture_by_id', request_method='DELETE', renderer='json')
def factures_delete_view(request):

    id = request.matchdict['id']

    query = request.dbsession.query(models.Facture)
    facture = query.filter(models.Facture.id == id).first()

    if not facture:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id))
    try:
        with transaction.manager:
            request.dbsession.delete(facture)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Facture.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


###########################################################
# EMOLUMENTS
###########################################################

""" Return all emoluments in facture"""
@view_config(route_name='facture_emoluments_by_facture_id', request_method='GET', renderer='json')
def facture_emoluments_view(request):
    facture_id = request.matchdict["id"]

    try:
        query = request.dbsession.query(models.VEmolumentsFactures)\
            .filter(models.VEmolumentsFactures.facture_id == facture_id).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new emolument_facture"""
@view_config(route_name='emolument_facture', request_method='POST', renderer='json')
@view_config(route_name='emolument_facture_s', request_method='POST', renderer='json')
def emolument_facture_new_view(request):

    record = models.EmolumentFacture()
    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(record)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.EmolumentFacture.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Update emolument_facture"""
@view_config(route_name='emolument_facture', request_method='PUT', renderer='json')
@view_config(route_name='emolument_facture_s', request_method='PUT', renderer='json')
def emolument_facture_update_view(request):
    emolument_facture_id = request.params['id'] if 'id' in request.params else None

    # Get the facture
    record = request.dbsession.query(models.EmolumentFacture).filter(
        models.EmolumentFacture.id == emolument_facture_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.EmolumentFacture.__tablename__, emolument_facture_id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.EmolumentFacture.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Delete emolument_facture"""
@view_config(route_name='emolument_facture_by_id', request_method='DELETE', renderer='json')
def emolument_facture_delete_view(request):
    try:
        id = request.matchdict['id']

        record = request.dbsession.query(models.EmolumentFacture).filter(
            models.EmolumentFacture.id == id).first()

        if not record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.EmolumentFacture.__tablename__, id))

        with transaction.manager:
            request.dbsession.delete(record)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.EmolumentFacture.__tablename__))

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
