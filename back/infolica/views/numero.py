from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from ..exceptions.custom_error import CustomError
from .. import models


""" Return all numeros"""

@view_config(route_name='numeros', request_method='GET', renderer='json')
@view_config(route_name='numeros_s', request_method='GET', renderer='json')
def numeros_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        query = request.dbsession.query(models.VNumeros).all()
        return Utils.serialize_many(query)

    except Exception as e:
        raise e


""" Return all types_numeros"""
@view_config(route_name='types_numeros', request_method='GET', renderer='json')
@view_config(route_name='types_numeros_s', request_method='GET', renderer='json')
def types_numeros_view(request):
    try:
        query = request.dbsession.query(models.NumeroType).all()
        return Utils.serialize_many(query)

    except Exception as e:
        raise e


""" Return all etats_numeros"""
@view_config(route_name='etats_numeros', request_method='GET', renderer='json')
@view_config(route_name='etats_numeros_s', request_method='GET', renderer='json')
def etats_numeros_view(request):
    try:
        query = request.dbsession.query(models.NumeroEtat).all()
        return Utils.serialize_many(query)

    except Exception as e:
        raise e


""" Return numeros by id"""
@view_config(route_name='numero_by_id', request_method='GET', renderer='json')
def numeros_by_id_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        # Get controle mutation id
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.VNumeros).filter(
            models.VNumeros.id == id).first()
        return Utils.serialize_one(query)

    except Exception as e:
        raise e


""" Search numeros"""
@view_config(route_name='recherche_numeros', request_method='POST', renderer='json')
@view_config(route_name='recherche_numeros_s', request_method='POST', renderer='json')
def numeros_search_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        settings = request.registry.settings
        search_limit = int(settings['search_limit'])
        conditions = Utils.get_search_conditions(models.VNumeros, request.params)
        query = request.dbsession.query(models.VNumeros).order_by(models.VNumeros.cadastre,
                                                                  models.VNumeros.numero.desc()).filter(
            *conditions).limit(search_limit).all()
        return Utils.serialize_many(query)

    except Exception as e:
        raise e


""" Add new numeros"""
@view_config(route_name='numeros', request_method='POST', renderer='json')
@view_config(route_name='numeros_s', request_method='POST', renderer='json')
def numeros_new_view(request, params=None):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise exc.HTTPForbidden()

        if not params:
            params = request.params

        # nouveau numero
        record = models.Numero()
        record = Utils.set_model_record(record, params)

        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            Utils.get_data_save_response(
                Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))
            return record.id

    except Exception as e:
        raise e


""" Update numeros"""
@view_config(route_name='numeros', request_method='PUT', renderer='json')
@view_config(route_name='numeros_s', request_method='PUT', renderer='json')
def numeros_update_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise exc.HTTPForbidden()

        # Get numero id
        id = request.params['id'] if 'id' in request.params else None

        # Get numero record
        record = request.dbsession.query(models.Numero).filter(
            models.Numero.id == id).first()

        if not record:
            raise CustomError(
                CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Numero.__tablename__, id))

        last_record_etat_id = record.etat_id
        record = Utils.set_model_record(record, request.params)

        with transaction.manager:
            # Commit transaction
            transaction.commit()

            if 'etat_id' in request.params:
                if request.params['etat_id'] != last_record_etat_id:
                    params = Utils._params(
                        numero_id=record.id, numero_etat_id=request.params['etat_id'])
                    numeros_etat_histo_new_view(request, params)

            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except Exception as e:
        raise e


""" Supprimer/abandonner numeros by id"""
@view_config(route_name='numero_by_id', request_method='DELETE', renderer='json')
def numeros_by_id_delete_view(request):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise exc.HTTPForbidden()

        # Get numero by id
        id = request.matchdict['id']
        query = request.dbsession.query(models.Numero).filter(
            models.Numero.id == id).first()

        if query:
            if query.etat_id == 1:  # projet
                query.etat_id = 3
            elif query.etat_id == 3:  # abandonné
                query.etat_id = 1
            # elif query.etat_id == 2: # vigueur
            #     query.etat_id = 4

            with transaction.manager:
                transaction.commit()

    except Exception as e:
        raise e


###########################################################
# NUMERO ETAT HISTO
###########################################################

""" Add new numero_etat_histo """
@view_config(route_name='numeros_etat_histo', request_method='POST', renderer='json')
@view_config(route_name='numeros_etat_histo_s', request_method='POST', renderer='json')
def numeros_etat_histo_new_view(request, params=None):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise exc.HTTPForbidden()

        if not params:
            params = request.params

        # nouveau numero
        record = models.NumeroEtatHisto()
        record = Utils.set_model_record(record, params)

        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(
                models.NumeroEtatHisto.__tablename__))
            return record.id

    except Exception as e:
        raise e


###########################################################
# AFFAIRE-NUMERO
###########################################################

""" Return all numeros in affaire"""
@view_config(route_name='affaire_numeros_by_affaire_id', request_method='GET', renderer='json')
def affaire_numeros_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        affaire_id = request.matchdict["id"]

        records = request.dbsession.query(models.VNumerosAffaires).filter(
            models.VNumerosAffaires.affaire_id == affaire_id).all()
        return Utils.serialize_many(records)

    except Exception as e:
        raise e


""" Add new affaire-numero """
@view_config(route_name='affaire_numeros', request_method='POST', renderer='json')
@view_config(route_name='affaire_numeros_s', request_method='POST', renderer='json')
def affaire_numero_new_view(request, params=None):
    try:
        # Check authorization
        if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
            raise exc.HTTPForbidden()

        if not params:
            params = request.params
        # nouveau affaire_numero
        record = models.AffaireNumero()
        record = Utils.set_model_record(record, params)

        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

    except Exception as e:
        raise e


###########################################################
# NUMERO- AFFAIRE
###########################################################

""" Return all affaires touching one numero """
@view_config(route_name='numero_affaires_by_numero_id', request_method='GET', renderer='json')
def numeros_affaire_view(request):
    try:
        # Check connected
        if not Utils.check_connected(request):
            raise exc.HTTPForbidden()

        numero_id = request.matchdict['id']

        query = request.dbsession.query(models.VNumerosAffaires).filter(
            models.VNumerosAffaires.numero_id == numero_id).all()

        if not query:
            raise CustomError.RECORD_WITH_ID_NOT_FOUND.format(
                models.VNumerosAffaires.__tablename__, numero_id)

        return Utils.serialize_many(query)

    except Exception as e:
        raise e

