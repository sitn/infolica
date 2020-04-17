from datetime import datetime
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

""" Return all numeros_relations"""
@view_config(route_name='numeros_relations', request_method='GET', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='GET', renderer='json')
def numeros_relations_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(models.VNumerosRelations).all()
    return Utils.serialize_many(query)


""" Add new numeros_relations"""
@view_config(route_name='numeros_relations', request_method='POST', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='POST', renderer='json')
def numeros_relations_new_view(request, params=None):
    if params is None:
        params = request.params

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # Get numeros_relations instance
    model = Utils.set_model_record(models.NumeroRelation(), params)

    with transaction.manager:
        request.dbsession.add(model)
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.NumeroRelation.__tablename__))


# """ Update operateur"""
# @view_config(route_name='operateurs', request_method='PUT', renderer='json')
# @view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
# def operateurs_update_view(request):
#     # Check authorization
#     if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
#         raise exc.HTTPForbidden()

#     # Get numero_relation_id
#     id_operateur = request.params['id'] if 'id' in request.params else None

#     model = request.dbsession.query(models.Operateur).filter(
#         models.Operateur.id == id_operateur).first()

#     # If result is empty
#     if not model:
#         raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
#             models.Operateur.__tablename__, id_operateur))

#     # Read params operateur
#     model = Utils.set_model_record(model, request.params)

#     with transaction.manager:

#         transaction.commit()
#         return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Operateur.__tablename__))

# """ Delete operateur"""
# @view_config(route_name='operateurs', request_method='DELETE', renderer='json')
# @view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
# def operateurs_delete_view(request):
#     # Check authorization
#     if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
#         raise exc.HTTPForbidden()

#     # Get operateur_id
#     id_operateur = request.params['id'] if 'id' in request.params else None

#     model = request.dbsession.query(models.Operateur).filter(
#         models.Operateur.id == id_operateur).first()

#     # If result is empty
#     if not model:
#         raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
#             models.Operateur.__tablename__, id_operateur))

#     model.sortie = datetime.utcnow()

#     with transaction.manager:
#         transaction.commit()
#         return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Operateur.__tablename__))

