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


@view_config(route_name='tableau_emoluments', request_method='GET', renderer='json')
def tableau_emoluments_view(request):
    """
    Return table of emoluments 
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(TableauEmoluments).all()
    return Utils.serialize_many(query)


@view_config(route_name='emolument_affaire', request_method='GET', renderer='json')
def emolument_affaire_view(request):
    """
    Return emolument_affaire
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None

    query = request.dbsession.query(EmolumentAffaire)
    
    if not affaire_id is None:
        query = query.filter(EmolumentAffaire.affaire_id == affaire_id)
    
    emolument_affaire = query.all()
    
    
    # Récupérer les données des bâtiments
    result = []
    for emolument_affaire_i in emolument_affaire:
        query_bat = request.dbsession.query(
            Emolument.batiment,
            Emolument.batiment_f
        ).filter(
            Emolument.emolument_affaire_id == emolument_affaire_i.id
        ).filter(
            Emolument.batiment > 0
        ).group_by(
            Emolument.batiment,
            Emolument.batiment_f
        ).all()
        
        batiment_f = [y for _, y in query_bat]

        result.append(
            Utils._params(
                id = emolument_affaire_i.id,
                affaire_id = emolument_affaire_i.affaire_id,
                pente_pc = emolument_affaire_i.pente_pc,
                diff_visibilite_pc = emolument_affaire_i.diff_visibilite_pc,
                trafic_pc = emolument_affaire_i.trafic_pc,
                zi = emolument_affaire_i.zi ,
                indice_application = emolument_affaire_i.indice_application,
                tva_pc = emolument_affaire_i.tva_pc,
                remarque = emolument_affaire_i.remarque,
                nb_batiments = len(batiment_f),
                batiment_f = batiment_f
            )
        )
    
    return result


@view_config(route_name='emolument', request_method='GET', renderer='json')
def emolument_view(request):
    """
    Return emoluments of emoluments_affaire 
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params['emolument_affaire_id'] if 'emolument_affaire_id' in request.params else None

    query = request.dbsession.query(Emolument).filter(
        Emolument.emolument_affaire_id == emolument_affaire_id
    ).all()

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


@view_config(route_name='emolument_affaire', request_method='PUT', renderer='json')
def emolument_affaire_new_view(request):
    """
    Update emolument_affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    params = request.params
    data = json.loads(params["data"])

    record_id = request.params['emolument_affaire_id'] if 'emolument_affaire_id' in request.params else None   

    record = request.dbsession.query(EmolumentAffaire).filter(
        EmolumentAffaire.id == record_id
    ).first()

    record = Utils.set_model_record(record, data)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentAffaire.__tablename__))


@view_config(route_name='emolument', request_method='PUT', renderer='json')
def emolument_new_view(request):
    """
    Update emolument
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    params = request.params
    data = json.loads(params['data'])
    emolument_affaire_id = params['emolument_affaire_id']

    # Query existing data
    query = request.dbsession.query(Emolument).filter(
        Emolument.emolument_affaire_id == emolument_affaire_id
    )

    for batiment_i in data:
        for emolument_i in batiment_i:
            # get emolument if already exists in DB
            record = query.filter(
                Emolument.batiment==batiment_i[emolument_i]['batiment']
            ).filter(
                Emolument.tableau_emolument_id==batiment_i[emolument_i]['tableau_emolument_id']
            ).first()

            if not record is None:
                # comparer les valeurs enregistrées
                if (not float(record.montant) == float(batiment_i[emolument_i]['montant']) \
                    or not record.position == batiment_i[emolument_i]['nom'] \
                    or not int(record.nombre) == int(batiment_i[emolument_i]['nombre']) \
                    or not float(record.batiment_f) == float(batiment_i[emolument_i]['batiment_f'])):

                    # Mettre à jour les données si le nouveau montant n'est pas nul
                    if float(batiment_i[emolument_i]['montant']) > 0:
                        params = Utils._params(
                            position=batiment_i[emolument_i]['nom'],
                            nombre=int(batiment_i[emolument_i]['nombre']),
                            batiment_f=float(batiment_i[emolument_i]['batiment_f']),
                            montant=float(batiment_i[emolument_i]['montant'])
                        )

                        record = Utils.set_model_record(record, params)
                    else:
                        # supprimer l'émolument
                        request.dbsession.delete(record)
                    
            else:
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
