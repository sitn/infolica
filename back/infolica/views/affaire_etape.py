from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import AffaireEtape, AffaireEtapeIndex, VEtapesAffaires
from infolica.scripts.utils import Utils

import transaction

###########################################################
# ETAPES AFFAIRE
###########################################################

""" GET etapes index"""
@view_config(route_name='etapes_index', request_method='GET', renderer='json')
@view_config(route_name='etapes_index_s', request_method='GET', renderer='json')
def etapes_index_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    records = request.dbsession.query(AffaireEtapeIndex).filter(
        AffaireEtapeIndex.ordre != None
        ).order_by(AffaireEtapeIndex.ordre.asc()).all()
    return Utils.serialize_many(records)

""" GET etapes affaire"""
@view_config(route_name='affaire_etapes_by_affaire_id', request_method='GET', renderer='json')
def affaires_etapes_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    records = request.dbsession.query(VEtapesAffaires).filter(
        VEtapesAffaires.affaire_id == affaire_id
    ).all()

    return Utils.serialize_many(records)

""" POST remarque affaire"""
@view_config(route_name='etapes', request_method='POST', renderer='json')
@view_config(route_name='etapes_s', request_method='POST', renderer='json')
def etapes_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_etape_edition']):
        raise exc.HTTPForbidden()

    model = AffaireEtape()
    model = Utils.set_model_record(model, request.params)

    with transaction.manager:
        request.dbsession.add(model)
        # Commit transaction
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(AffaireEtape.__tablename__))

""" DELETE remarque affaire"""
@view_config(route_name='etapes_by_id', request_method='DELETE', renderer='json')
def etapes_delete_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_etape_edition']):
        raise exc.HTTPForbidden()

    affaire_etape_id = request.matchdict['id']

    record = request.dbsession.query(AffaireEtape).filter(
        AffaireEtape.id == affaire_etape_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(AffaireEtape.__tablename__, affaire_etape_id))

    with transaction.manager:
        request.dbsession.delete(record)
        # Commit transaction
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(AffaireEtape.__tablename__))


