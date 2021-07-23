# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import EmolumentFacture, VEmolumentsFactures, TableauEmoluments
from infolica.models.models import EmolumentAffaire, Emolument
from infolica.scripts.utils import Utils

import json

###########################################################
# EMOLUMENTS
###########################################################


@view_config(route_name='emoluments', request_method='GET', renderer='json')
def emoluments_view(request):
    """
    Return all emoluments available
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(TableauEmoluments).all()
    return Utils.serialize_many(query)


@view_config(route_name='facture_emoluments_by_facture_id', request_method='GET', renderer='json')
def facture_emoluments_view(request):
    """
    Return all emoluments in facture
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    facture_id = request.matchdict["id"]

    query = request.dbsession.query(VEmolumentsFactures).filter(
        VEmolumentsFactures.facture_id == facture_id
    ).all()
    return Utils.serialize_many(query)


@view_config(route_name='emolument_facture', request_method='POST', renderer='json')
@view_config(route_name='emolument_facture_s', request_method='POST', renderer='json')
def emolument_facture_new_view(request):
    """
    Add new emolument_facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    record = EmolumentFacture()
    record = Utils.set_model_record(record, request.params)

    request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentFacture.__tablename__))


@view_config(route_name='emolument_facture', request_method='PUT', renderer='json')
@view_config(route_name='emolument_facture_s', request_method='PUT', renderer='json')
def emolument_facture_update_view(request):
    """
    Update emolument_facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    emolument_facture_id = request.params['id'] if 'id' in request.params else None

    # Get the facture
    record = request.dbsession.query(EmolumentFacture).filter(
        EmolumentFacture.id == emolument_facture_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(EmolumentFacture.__tablename__, emolument_facture_id))

    record = Utils.set_model_record(record, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentFacture.__tablename__))


@view_config(route_name='emolument_facture_by_id', request_method='DELETE', renderer='json')
def emolument_facture_delete_view(request):
    """
    Delete emolument_facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']

    record = request.dbsession.query(EmolumentFacture).filter(
        EmolumentFacture.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(EmolumentFacture.__tablename__, id))

    request.dbsession.delete(record)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(EmolumentFacture.__tablename__))

###############################################################################################################

@view_config(route_name='emolument_affaire', request_method='POST', renderer='json')
def emolument_affaire_new_view(request):
    """
    Add new emolument_affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    params = request.params
    data = json.loads(params["data"])

    record = EmolumentAffaire()
    record = Utils.set_model_record(record, data)

    request.dbsession.add(record)
    request.dbsession.flush()

    return {"emolument_affaire_id": record.id}


@view_config(route_name='emolument', request_method='POST', renderer='json')
def emolument_new_view(request):
    """
    Add new emolument
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    params = request.params
    data = json.loads(params['data'])
    emolument_affaire_id = params['emolument_affaire_id']

    for batiment_i in data:
        for emolument_i in batiment_i:
            if float(batiment_i[emolument_i]['montant']) > 0 and float(batiment_i[emolument_i]['nombre']) > 0:
                params = Utils._params(
                    emolument_affaire_id=int(emolument_affaire_id),
                    tableau_emolument_id=int(batiment_i[emolument_i]['tableau_emolument_id']),
                    position=batiment_i[emolument_i]['nom'],
                    prix_unitaire=float(batiment_i[emolument_i]['prix_unitaire']),
                    nombre=int(batiment_i[emolument_i]['nombre']),
                    batiment=int(batiment_i[emolument_i]['batiment']),
                    batiment_f=float(batiment_i[emolument_i]['batiment_f']),
                    montant=float(batiment_i[emolument_i]['montant'])
                )

                record = Emolument()
                record = Utils.set_model_record(record, params)

                request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Emolument.__tablename__))

