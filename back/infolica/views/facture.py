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



""" Return all types factures"""
@view_config(route_name='types_factures', request_method='GET', renderer='json')
@view_config(route_name='types_factures_s', request_method='GET', renderer='json')
def factures_types_view(request):
    try:
        query = request.dbsession.query(models.FactureType).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(str(e), exc_info=True)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Return all factures"""
@view_config(route_name='factures', request_method='GET', renderer='json')
@view_config(route_name='factures_s', request_method='GET', renderer='json')
def factures_view(request):
    try:
        query = request.dbsession.query(models.Facture).all()
        return Utils.serialize_many(query)
    except DBAPIError as e:
        log.error(str(e), exc_info=True)
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Add new facture"""
@view_config(route_name='factures', request_method='POST', renderer='json')
@view_config(route_name='factures_s', request_method='POST', renderer='json')
def factures_new_view(request):
    try:
        settings = request.registry.settings

        # Read params affaire
        affaire_id = None
        sap = None
        client_id = None
        montant_mo = None
        montant_rf = None
        montant_mat_diff = None
        tva = None
        total = None
        date = None
        type_facture = None

        if 'affaire_id' in request.params:
            affaire_id = request.params['affaire_id']

        if 'sap' in request.params:
            sap = request.params['sap']

        if 'client_id' in request.params:
            client_id = request.params['client_id']

        if 'montant_mo' in request.params:
            montant_mo = request.params['montant_mo']

        if 'montant_rf' in request.params:
            montant_rf = request.params['montant_rf']

        if 'montant_mat_diff' in request.params:
            montant_mat_diff = request.params['montant_mat_diff']

        if 'tva' in request.params:
            tva = request.params['tva']

        if 'total' in request.params:
            total = request.params['total']

        if 'date' in request.params:
            date = request.params['date']

        if 'type_facture' in request.params:
            type_facture = request.params['type_facture']


        with transaction.manager:
            model = models.Facture(
                affaire_id= affaire_id,
                sap = sap,
                client_id = client_id,
                montant_mo = montant_mo,
                montant_rf = montant_rf,
                montant_mat_diff = montant_mat_diff,
                tva = tva,
                total = total,
                date = date,
                type_facture = type_facture
            )

            request.dbsession.add(model)

            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Constant.SUCCESS_SAVE


""" Update facture"""
@view_config(route_name='factures', request_method='PUT', renderer='json')
@view_config(route_name='factures_s', request_method='POST', renderer='json')
def factures_update_view(request):
    try:
        settings = request.registry.settings

        # Read params affaire
        id_facture = None
        sap = None
        client_id = None
        montant_mo = None
        montant_rf = None
        montant_mat_diff = None
        tva = None
        total = None
        date = None
        type_facture = None

        if 'id_facture' in request.params:
            id_facture = request.params['id_facture']

        if 'affaire_id' in request.params:
            affaire_id = request.params['affaire_id']

        if 'sap' in request.params:
            sap = request.params['sap']

        if 'client_id' in request.params:
            client_id = request.params['client_id']

        if 'montant_mo' in request.params:
            montant_mo = request.params['montant_mo']

        if 'montant_rf' in request.params:
            montant_rf = request.params['montant_rf']

        if 'montant_mat_diff' in request.params:
            montant_mat_diff = request.params['montant_mat_diff']

        if 'tva' in request.params:
            tva = request.params['tva']

        if 'total' in request.params:
            total = request.params['total']

        if 'date' in request.params:
            date = request.params['date']

        if 'type_facture' in request.params:
            type_facture = request.params['type_facture']

        # Get the facture
        facture_record = request.dbsession.query(models.Facture).filter(
            models.Client.id == id_facture).first()

        if not facture_record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id_facture))

        with transaction.manager:

            facture_record.affaire_id= affaire_id
            facture_record.sap = sap
            facture_record.client_id = client_id
            facture_record.montant_mo = montant_mo
            facture_record.montant_rf = montant_rf
            facture_record.montant_mat_diff = montant_mat_diff
            facture_record.tva = tva
            facture_record.total = total
            facture_record.date = date
            facture_record.type_facture = type_facture

            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Constant.SUCCESS_SAVE


""" Delete facture"""
@view_config(route_name='facture_by_id', request_method='DELETE', renderer='json')
def factures_update_view(request):
    try:
        id = request.matchdict['id']

        query = request.dbsession.query(models.Facture)
        facture = query.filter(models.Facture.id == id).first()

        if not facture:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Facture.__tablename__, id))

        with transaction.manager:
            request.dbsession.delete(facture)
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

