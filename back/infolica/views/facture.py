# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireEtape
from infolica.models.models import EmolumentAffaire, EmolumentAffaireRepartition
from infolica.models.models import Facture, FactureType, VFactures
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
import json

###########################################################
# FACTURE
###########################################################


@view_config(route_name='factures', request_method='GET', renderer='json')
@view_config(route_name='factures_s', request_method='GET', renderer='json')
def factures_view(request):
    """
    Return all factures
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VFactures).all()
    return Utils.serialize_many(query)


@view_config(route_name='facture_type', request_method='GET', renderer='json')
def facture_type_view(request):
    """
    Return all facture types
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(FactureType).all()
    return Utils.serialize_many(query)


@view_config(route_name='affaires_factures_by_affaire_id', request_method='GET', renderer='json')
def affaires_factures_view(request):
    """
    Return all factures in affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict["id"]

    query = request.dbsession.query(VFactures).filter(
        VFactures.affaire_id == affaire_id
    ).all()
    return Utils.serialize_many(query)


@view_config(route_name='factures', request_method='POST', renderer='json')
@view_config(route_name='factures_s', request_method='POST', renderer='json')
def factures_new_view(request):
    """
    Add new facture
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    params = {}
    for key in request.params:
        if key == "numeros":
            params[key] = json.loads(request.params[key])
        else: 
            params[key] = request.params[key]

    Utils.addNewRecord(request, Facture, params)

     # send mail if client is new and outside canton NE
    if 'client_id' in request.params:
        client_id = request.params['client_id']
        affaire_id = request.params['affaire_id']
        nb_etape_traitement = request.dbsession.query(AffaireEtape).filter(
            AffaireEtape.affaire_id == affaire_id
        ).filter(
            AffaireEtape.etape_id == request.registry.settings['affaire_etape_traitement_id']
        ).count()
        if nb_etape_traitement >= 1:
            Utils.sendMailClientHorsCanton(request, client_id, affaire_id)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Facture.__tablename__))


@view_config(route_name='factures', request_method='PUT', renderer='json')
@view_config(route_name='factures_s', request_method='PUT', renderer='json')
def factures_update_view(request):
    """
    Update facture
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    # id_facture
    id_facture = None

    if 'id' in request.params:
        id_facture = request.params['id']

    # Get the facture
    facture_record = request.dbsession.query(Facture).filter(
        Facture.id == id_facture).first()

    facture_client_id_old = int(facture_record.client_id)
    facture_client_id_new = int(request.params['client_id']) if 'client_id' in request.params else None

    params = {}
    for key in request.params:
        if key == "numeros":
            params[key] = json.loads(request.params[key])
        else: 
            params[key] = request.params[key]

    if not facture_record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Facture.__tablename__, id_facture))

    facture_record = Utils.set_model_record(facture_record, params)

    # send mail if client is new and outside canton NE
    nb_etape_traitement = request.dbsession.query(AffaireEtape).filter(
        AffaireEtape.affaire_id == facture_record.affaire_id
    ).filter(
        AffaireEtape.etape_id == request.registry.settings['affaire_etape_traitement_id']
    ).count()
    if facture_client_id_new and facture_client_id_old != facture_client_id_new and nb_etape_traitement >= 1:
        Utils.sendMailClientHorsCanton(request, facture_record.client_id, facture_record.affaire_id)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Facture.__tablename__))


@view_config(route_name='factures', request_method='DELETE', renderer='json')
@view_config(route_name='factures_s', request_method='DELETE', renderer='json')
def factures_delete_view(request):
    """
    Delete facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    facture_id = request.params['id'] if 'id' in request.params else None

    # Check if emolument_facture_repartition exists and delete it before
    results = request.dbsession.query(
        EmolumentAffaireRepartition
    ).filter(
        EmolumentAffaireRepartition.facture_id == facture_id
    ).all()

    if results and len(results) > 0:
        for result in results:
            # set emolument to "unused" if this is not the case so it is set back to editable mode
            emol = request.dbsession.query(
                EmolumentAffaire
            ).filter(
                EmolumentAffaire.id == result.emolument_affaire_id
            ).first()

            emol.utilise = False

            # Remove emolument_facture_repartition
            request.dbsession.delete(result)

    # remove facture
    facture = request.dbsession.query(Facture).filter(Facture.id == facture_id).first()

    if not facture:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Facture.__tablename__, facture_id))

    request.dbsession.delete(facture)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Facture.__tablename__))
