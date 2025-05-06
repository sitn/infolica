# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Operateur, EtapeMailer, Service, NotesMAJ, Role
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import BigInteger, func

import json


def _updateOperateurNotifications(request, operateur_id, etapesMailerList):
    affaire_etapes_mailer = func.array_agg(EtapeMailer.etape_id, type_=ARRAY(BigInteger)).label('affaire_etapes_mailer')
    aem_old = request.dbsession.query(
        EtapeMailer.operateur_id,
        affaire_etapes_mailer
    ).filter(
        EtapeMailer.operateur_id == operateur_id
    ).group_by(
        EtapeMailer.operateur_id
    ).first()

    tmp = []
    if aem_old is not None:
        tmp = aem_old.affaire_etapes_mailer

    aem_old = set(tmp)

    aem2create = etapesMailerList.difference(aem_old)
    aem2delete = aem_old.difference(etapesMailerList)

    for em in aem2create:
        params = {
            'etape_id': em,
            'operateur_id': operateur_id,
            'sendmail': True
        }
        Utils.addNewRecord(request, EtapeMailer, params)

    for em in aem2delete:
        em2delete = request.dbsession.query(
            EtapeMailer
        ).filter(
            EtapeMailer.operateur_id == operateur_id,
            EtapeMailer.etape_id == em
        ).first()
        request.dbsession.delete(em2delete)
    return


@view_config(route_name='operateurs', request_method='GET', renderer='json')
@view_config(route_name='operateurs_s', request_method='GET', renderer='json')
def operateurs_view(request):
    """
    Return all operateurs
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(
        Operateur
    ).filter(
        Operateur.sortie == None
    ).order_by(
        Operateur.prenom
    ).all()

    operateurs = Utils.serialize_many(query)

    for op in operateurs:
        op['prenom_nom'] = ' '.join([op['prenom'], op['nom']])

    return operateurs


@view_config(route_name='operateur_by_id', request_method='GET', renderer='json')
def operateur_by_id_view(request):
    """
    Return operateur by id
    """
    authorized_services = [*[request.registry.settings['service_mo'].replace(' ', '')], *request.registry.settings['preavis_services_externes'].replace(' ', '').split(',')]

    # Check connected
    if not check_connected(request, services=authorized_services):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    query = request.dbsession.query(Operateur).filter(
        Operateur.id == id).first()
    return Utils.serialize_one(query)


@view_config(route_name='operateur_update', request_method='GET', renderer='json')
def operateur_update_view(request):
    """
    Return operateur_update
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    operateur_id = request.params['operateur_id'] if 'operateur_id' in request.params else None

    operateur = request.dbsession.query(
        Operateur,
    ).filter(
        Operateur.id == operateur_id,
    ).first()

    affaire_etapes_mailer = func.array_agg(EtapeMailer.etape_id, type_=ARRAY(BigInteger)).label('affaire_etapes_mailer')
    operateur_etapes_mailer = request.dbsession.query(
        EtapeMailer.operateur_id,
        affaire_etapes_mailer
    ).filter(
        EtapeMailer.operateur_id == operateur_id,
    ).group_by(
        EtapeMailer.operateur_id
    ).first()

    operateur = Utils.serialize_one(operateur)

    tmp = []
    if operateur_etapes_mailer is not None:
        tmp = operateur_etapes_mailer.affaire_etapes_mailer

    operateur['affaire_etapes_mailer'] = tmp

    return operateur


@view_config(route_name='recherche_operateurs', request_method='POST', renderer='json')
@view_config(route_name='recherche_operateurs_s', request_method='POST', renderer='json')
def operateurs_search_view(request):
    """
    Search operateurs
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])
    old_operateurs = request.params["old_operateurs"]=="true" if "old_operateurs" in request.params else False

    if "moreResults" in request.params.keys():
        search_limit += int(request.params["moreResults"])

    conditions = Utils.get_search_conditions(Operateur, request.params, ignore_params=["old_operateurs", "moreResults"])


    # Check date_sortie is null
    conditions = [] if not conditions or len(conditions) == 0 else conditions

    if old_operateurs is False:
        conditions.append(Operateur.sortie == None)

    query = request.dbsession.query(Operateur).filter(*conditions)

    nb_operateurs_total = query.with_entities(func.count(Operateur.id)).scalar()

    operateurs = query.order_by(Operateur.nom, Operateur.prenom).limit(search_limit).all()

    operateurs = Utils.serialize_many(operateurs)

    for op in operateurs:
        op["role"] = request.dbsession.query(Role.nom).filter(Role.id==op["role_id"]).scalar()
        op["entree_sort"] = datetime.strptime(op["entree"], "%Y-%m-%d").timestamp() if op["entree"] is not None else 0
        op["sortie_sort"] = datetime.strptime(op["sortie"], "%Y-%m-%d").timestamp() if op["sortie"] is not None else 0

    result = {
        "operateur_liste": operateurs,
        "nb_operateurs_total": nb_operateurs_total,
    }

    return result


@view_config(route_name='operateurs', request_method='POST', renderer='json')
@view_config(route_name='operateurs_s', request_method='POST', renderer='json')
def operateurs_new_view(request):
    """
    Add new operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur instance
    model = Utils.set_model_record(Operateur(), request.params)

    model.service = request.dbsession.query(Service.abreviation).filter(Service.id == model.service_id).scalar() if model.service_id else None
    model.last_notemaj_id = request.dbsession.query(func.max(NotesMAJ.id)).scalar()
    model.role = request.dbsession.query(Role).filter(Role.id == model.role_id).first()

    request.dbsession.add(model)
    request.dbsession.flush()

    if 'affaire_etapes_mailer' in request.params:
        aem_new = set(json.loads(request.params['affaire_etapes_mailer']))
        _updateOperateurNotifications(request, model.id, aem_new)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Operateur.__tablename__))


@view_config(route_name='operateurs', request_method='PUT', renderer='json')
@view_config(route_name='operateurs_s', request_method='PUT', renderer='json')
def operateurs_update_view(request):
    """
    Update operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(Operateur).filter(
        Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            Operateur.__tablename__, id_operateur))

    # Read params operateur
    model = Utils.set_model_record(model, request.params)

    if 'affaire_etapes_mailer' in request.params:
        aem_new = set(json.loads(request.params['affaire_etapes_mailer']))
        _updateOperateurNotifications(request, id_operateur, aem_new)


    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Operateur.__tablename__))


@view_config(route_name='operateurs', request_method='DELETE', renderer='json')
@view_config(route_name='operateurs_s', request_method='DELETE', renderer='json')
def operateurs_delete_view(request):
    """
    Delete operateur
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['fonction_admin']):
        raise exc.HTTPForbidden()

    # Get operateur_id
    id_operateur = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(Operateur).filter(
        Operateur.id == id_operateur).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            Operateur.__tablename__, id_operateur))

    model.sortie = datetime.utcnow()

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Operateur.__tablename__))
