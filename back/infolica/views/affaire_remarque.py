from pyramid.view import view_config
import pyramid.httpexceptions as exc
from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

###########################################################
# REMARQUES AFFAIRE
###########################################################

""" GET remarque affaire"""
@view_config(route_name='affaires_remarques_by_affaire_id', request_method='GET', renderer='json')
def affaires_remarques_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    records = request.dbsession.query(models.RemarqueAffaire, models.Operateur)\
        .filter(models.RemarqueAffaire.affaire_id == affaire_id)\
        .filter(models.RemarqueAffaire.operateur_id == models.Operateur.id).all()

    ra_json = list()
    for ra, op in records:
        ra_json.append(Utils._params(id=ra.id, nom=op.nom, prenom=op.prenom,
                                     remarque=ra.remarque, date=ra.date.isoformat()))

    return ra_json


""" POST remarque affaire"""
@view_config(route_name='remarques_affaires', request_method='POST', renderer='json')
@view_config(route_name='remarques_affaires_s', request_method='POST', renderer='json')
def affaires_remarques_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_remarque_edition']):
        raise exc.HTTPForbidden()

    model = models.RemarqueAffaire()
    model = Utils.set_model_record(model, request.params)

    with transaction.manager:
        request.dbsession.add(model)
        # Commit transaction
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.RemarqueAffaire.__tablename__))


""" PUT remarque affaire"""
@view_config(route_name='remarques_affaires', request_method='PUT', renderer='json')
@view_config(route_name='remarques_affaires_s', request_method='PUT', renderer='json')
def remarques_affaires_update_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_remarque_edition']):
        raise exc.HTTPForbidden()

    remarque_affaire_id = request.params['id'] if 'id' in request.params else None

    record = request.dbsession.query(models.RemarqueAffaire).filter(
        models.RemarqueAffaire.id == remarque_affaire_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.RemarqueAffaire.__tablename__, remarque_affaire_id))

    record = Utils.set_model_record(record, request.params)

    with transaction.manager:
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.RemarqueAffaire.__tablename__))


""" DELETE remarque affaire"""
@view_config(route_name='remarques_affaires_by_id', request_method='DELETE', renderer='json')
def remarques_affaires_delete_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_remarque_edition']):
        raise exc.HTTPForbidden()

    remarque_affaire_id = request.matchdict['id']

    record = request.dbsession.query(models.RemarqueAffaire).filter(
        models.RemarqueAffaire.id == remarque_affaire_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.RemarqueAffaire.__tablename__, remarque_affaire_id))

    with transaction.manager:
        request.dbsession.delete(record)
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.RemarqueAffaire.__tablename__))
