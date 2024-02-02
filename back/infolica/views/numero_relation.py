# -*- coding: utf-8 -*--
import pyramid.httpexceptions as exc
from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import (AffaireNumero, Numero, NumeroRelation,
                                    VNumerosRelations)
from infolica.scripts.authentication import check_connected
from infolica.scripts.utils import Utils
from pyramid.view import view_config
from sqlalchemy import and_


@view_config(route_name='numeros_relations', request_method='GET', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='GET', renderer='json')
def numeros_relations_view(request):
    """
    Return all numeros_relations
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VNumerosRelations).all()
    return Utils.serialize_many(query)


@view_config(route_name='numeros_relation_by_affaire_id', request_method='GET', renderer='json')
def numeros_relation_by_affaire_id_view(request):
    """
    Return Numeros_relations
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    # filter by conditions
    query = request.dbsession.query(VNumerosRelations).filter(
        VNumerosRelations.affaire_id == affaire_id).all()

    return Utils.serialize_many(query)


# """ Return all numeros_relations based on numero_base_id having project or valid numbers defined on it"""
# @view_config(route_name='numeros_relations_by_numeroBase', request_method='POST', renderer='json')
# @view_config(route_name='numeros_relations_by_numeroBase_s', request_method='POST', renderer='json')
# def numeros_relations_by_numeroBase_view(request):
#     # Check connected
#     if not check_connected(request):
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


@view_config(route_name='numeros_relations', request_method='POST', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='POST', renderer='json')
def numeros_relations_new_view(request, params=None):
    """
    Add new numeros_relations
    """
    if params is None:
        params = request.params

    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # check that relation does not exist yet
    conditions = []
    conditions.append(NumeroRelation.numero_id_base == params['numero_id_base'])
    conditions.append(NumeroRelation.numero_id_associe == params['numero_id_associe'])
    conditions.append(NumeroRelation.relation_type_id == params['relation_type_id'])
    conditions.append(NumeroRelation.affaire_id == params['affaire_id'])

    active_relation = False
    if params['active_relation'] == 'true':
        active_relation = True

    rel = request.dbsession.query(NumeroRelation).filter(*conditions).first()

    if (rel is None and active_relation is False) or (rel is not None and active_relation is True):
        return None

    elif (rel is not None and active_relation is False):
        request.dbsession.delete(rel)
        return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(NumeroRelation.__tablename__))

    else:
        # Get numeros_relations instance
        model = Utils.set_model_record(NumeroRelation(), params)
        request.dbsession.add(model)
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroRelation.__tablename__))


@view_config(route_name='numeros_relations', request_method='PUT', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='PUT', renderer='json')
def numeros_relations_update_view(request):
    """
    Update numeros_relations
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    model = request.dbsession.query(NumeroRelation)

    # get instance
    if "id" in request.params:
        numrel_id = request.params["id"]
        model = model.filter(NumeroRelation.id == numrel_id)
    else:
        num_base_id = request.params["numero_id_base"]
        num_associe_id = request.params["numero_id_associe"]
        affaire_old_id = request.params["affaire_old_id"]

        model = model.filter(and_(
            NumeroRelation.numero_id_base == num_base_id,
            NumeroRelation.numero_id_associe == num_associe_id,
            NumeroRelation.affaire_id == affaire_old_id,
        ))

    model = model.first()

    # update instance
    if model != None and "affaire_new_id" in request.params:
        model.affaire_id = request.params["affaire_new_id"] if "affaire_new_id" in request.params else None

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroRelation.__tablename__))


@view_config(route_name='numeros_relations', request_method='DELETE', renderer='json')
@view_config(route_name='numeros_relations_s', request_method='DELETE', renderer='json')
def numeros_relations_delete_view(request):
    """
    Delete numeros_relations
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    model = None
    numero_relation_id = None
    if "numero_relation_id" in request.params:
        numero_relation_id = request.params["numero_relation_id"]
        model = request.dbsession.query(NumeroRelation).filter(NumeroRelation.id == numero_relation_id).first()
    elif "numero_base_id" in request.params and "affaire_id" in request.params:
        numero_base_id = int(request.params["numero_base_id"])
        affaire_id = int(request.params["affaire_id"])
        numero_relation_id = "numero_base_id=" + request.params["numero_base_id"] + " & affaire_id=" + request.params["affaire_id"]
        model = request.dbsession.query(NumeroRelation).filter(and_(
            NumeroRelation.numero_id_base == numero_base_id,
            NumeroRelation.affaire_id == affaire_id
        )).first()
    else:
        raise CustomError.INCOMPLETE_REQUEST

    if not model:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(NumeroRelation.__tablename__, numero_relation_id))

    request.dbsession.delete(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(NumeroRelation.__tablename__))

###########################################################
# CONSTITUTION DDP
###########################################################


@view_config(route_name="new_ddp", request_method="POST", renderer="json")
def numero_differe_view(request):
    """
    Post new ddp
    """
    # Check authorization
    if not Utils.has_permission(
        request, request.registry.settings["affaire_numero_edition"]
    ):
        raise exc.HTTPForbidden()

    numero_type_ddp_id = request.registry.settings["numero_ddp_id"]
    numero_relation_type_ddp_id = request.registry.settings["numero_relation_ddp_id"]
    affaire_numero_type_ancien_id = request.registry.settings[
        "affaire_numero_type_ancien_id"
    ]

    affaire_id = (
        request.params["affaire_id"] if "affaire_id" in request.params else None
    )
    ddp_id = request.params["ddp"] if "ddp" in request.params else None
    base_id = request.params["base"] if "base" in request.params else None

    if ddp_id is not None and base_id is not None:
        # update type of ddp
        ddp = request.dbsession.query(Numero).get(ddp_id)
        ddp.type_id = numero_type_ddp_id

        # create / update numero_relation
        num_rel = (
            request.dbsession.query(NumeroRelation)
            .filter(
                NumeroRelation.numero_id_base == base_id,
                NumeroRelation.numero_id_associe == ddp_id,
                NumeroRelation.affaire_id == affaire_id,
            )
            .first()
        )

        if num_rel is not None:
            num_rel.relation_type_id = numero_relation_type_ddp_id
        else:
            num_rel = NumeroRelation()
            num_rel.affaire_id = affaire_id
            num_rel.numero_id_base = base_id
            num_rel.numero_id_associe = ddp_id
            num_rel.relation_type_id = numero_relation_type_ddp_id
            request.dbsession.add(num_rel)

        # create / update affaire_numero base
        aff_num_base = (
            request.dbsession.query(AffaireNumero)
            .filter(
                AffaireNumero.affaire_id == affaire_id,
                AffaireNumero.numero_id == base_id,
            )
            .first()
        )

        if aff_num_base is not None:
            aff_num_base.type_id = affaire_numero_type_ancien_id
            aff_num_base.actif = True
        else:
            aff_num_base = AffaireNumero()
            aff_num_base.affaire_id = affaire_id
            aff_num_base.numero_id = base_id
            aff_num_base.type_id = affaire_numero_type_ancien_id
            aff_num_base.actif = True
            request.dbsession.add(aff_num_base)

    return Utils.get_data_save_response(
        Constant.SUCCESS_SAVE.format(NumeroRelation.__tablename__)
    )
