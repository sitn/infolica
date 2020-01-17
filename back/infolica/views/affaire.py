from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

""" Return all affaires"""
@view_config(route_name='affaires', request_method='GET', renderer='json')
@view_config(route_name='affaires_s', request_method='GET', renderer='json')
def affaires_view(request):
    try:
        query = request.dbsession.query(models.Affaire).all()
        return Utils.serialize_many(query)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



""" Return affaires by id"""
@view_config(route_name='affaire_by_id', request_method='GET', renderer='json')
def affaire_by_id_view(request):
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Affaire)
        one = query.filter(models.Affaire.id == id).first()
        return Utils.serialize_one(one)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


""" Search affaires"""
@view_config(route_name='recherche_affaires', request_method='GET', renderer='json')
@view_config(route_name='recherche_affaires_s', request_method='GET', renderer='json')
def affaires_search_view(request):
    try:
        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(models.Affaire, request.params)
        query = request.dbsession.query(models.Affaire).filter(*conditions).all()[:search_limit]
        return Utils.serialize_many(query)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

""" Return all types affaires"""
@view_config(route_name='types_affaires', request_method='GET', renderer='json')
@view_config(route_name='types_affaires_s', request_method='GET', renderer='json')
def types_affaires_view(request):
    try:
        query = request.dbsession.query(models.AffaireType).all()
        return Utils.serialize_many(query)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



""" Add new affaire"""
@view_config(route_name='affaires', request_method='POST', renderer='json')
def affaires_new_view(request):
    try:

        model = models.Affaire()
        model = Utils.set_model_record(model, request.params)

        with transaction.manager:
            request.dbsession.add(model)

            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))

""" Update affaire"""
@view_config(route_name='affaires', request_method='PUT', renderer='json')
@view_config(route_name='affaires_s', request_method='PUT', renderer='json')
def affaires_update_view(request):
    try:

        # id_affaire
        id_affaire = None

        if 'id_affaire' in request.params:
            id_affaire = request.params['id_affaire']

        # Get the affaire
        affaire_record = request.dbsession.query(models.Affaire).filter(
            models.Affaire.id == id_affaire).first()

        if not affaire_record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))

        affaire_record = Utils.set_model_record(affaire_record, request.params)

        with transaction.manager:

            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))


""" Delete affaire"""
@view_config(route_name='affaire_by_id', request_method='DELETE', renderer='json')
def affaires_delete_view(request):
    try:
        id = request.matchdict['id']

        query = request.dbsession.query(models.Affaire)
        affaire = query.filter(models.Affaire.id == id).first()

        if not affaire:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id))

        with transaction.manager:
            request.dbsession.delete(affaire)
            # Commit transaction
            transaction.commit()

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Affaire.__tablename__))


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
