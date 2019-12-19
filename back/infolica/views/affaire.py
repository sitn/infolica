from pyramid.view import view_config
from pyramid.response import Response

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
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Return affaires by id"""
@view_config(route_name='affaire_by_id', request_method='GET', renderer='json')
def affaire_by_id_view(request):
    try:
        id = request.matchdict['id']
        query = request.dbsession.query(models.Affaire)
        one = query.filter(models.Affaire.id == id).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_one(one)


""" Return all types affaires"""
@view_config(route_name='types_affaires', request_method='GET', renderer='json')
@view_config(route_name='types_affaires_s', request_method='GET', renderer='json')
def types_affaires_view(request):
    try:
        query = request.dbsession.query(models.AffaireType).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return Utils.serialize_many(query)


""" Add new affaire"""
@view_config(route_name='affaires', request_method='POST', renderer='json')
def affaires_new_view(request):
    try:
        settings = request.registry.settings

        # Read params affaire
        responsable_id = None
        technicien_id = None
        type_id = None
        cadastre_id = None
        information = None
        date_ouverture = None
        date_cloture = None
        localisation_E = None
        localisation_N = None

        if 'responsable_id' in request.params:
            responsable_id = request.params['responsable_id']

        if 'technicien_id' in request.params:
            technicien_id = request.params['technicien_id']

        if 'cadastre_id' in request.params:
            cadastre_id = request.params['cadastre_id']

        if 'information' in request.params:
            information = request.params['information']

        if 'date_ouverture' in request.params:
            date_ouverture = request.params['date_ouverture']

        if 'date_cloture' in request.params:
            date_cloture = request.params['date_cloture']

        if 'localisation_E' in request.params:
            localisation_E = request.params['localisation_E']

        if 'localisation_N' in request.params:
            localisation_N = request.params['localisation_N']

        with transaction.manager:
            model = models.Affaire(
                responsable_id = responsable_id,
                technicien_id = technicien_id,
                type_id = type_id,
                cadastre_id = cadastre_id,
                information = information,
                date_ouverture = date_ouverture,
                date_cloture = date_cloture,
                localisation_E = localisation_E,
                localisation_N = localisation_N
            )

            request.dbsession.add(model)

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
