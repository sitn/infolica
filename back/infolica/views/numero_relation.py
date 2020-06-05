from datetime import datetime
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils
from sqlalchemy import and_
import json

""" Return all numeros_relations"""
@view_config(route_name='numeros_relations', request_method='GET', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='GET', renderer='json')
def numeros_relations_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(models.VNumerosRelations).all()
    return Utils.serialize_many(query)


# """ Return all numeros_relations based on numero_base_id having project or valid numbers defined on it"""
# @view_config(route_name='numeros_relations_by_numeroBase', request_method='POST', renderer='json')
# @view_config(route_name='numeros_relations_by_numeroBase_s', request_method='POST', renderer='json')
# def numeros_relations_by_numeroBase_view(request):
#     # Check connected
#     if not Utils.check_connected(request):
#         raise exc.HTTPForbidden()

#     # Récupérer les indices des états projet et vigueur de la config
#     settings = request.registry.settings
#     numero_etat_projet_id = int(settings['numero_projet_id'])
#     numero_etat_vigueur_id = int(settings['numero_vigueur_id'])

#     # Récupérer la liste des numéros de base de l'affaire
#     numeros_base_id_list = request.params['numeros_base_id_list'] if 'numeros_base_id_list' in request.params else None
#     numeros_base_id_list = json.loads(numeros_base_id_list)

#     query = request.dbsession.query(models.VNumerosRelations).filter(
#         and_(
#             models.VNumerosRelations.numero_base_id.in_(numeros_base_id_list),
#             models.VNumerosRelations.numero_associe_etat_id.in_([numero_etat_projet_id, numero_etat_vigueur_id])
#         )).all()
#     return Utils.serialize_many(query)


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


