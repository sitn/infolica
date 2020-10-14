# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Numero
from infolica.scripts.utils import Utils
from infolica.views.numero import numeros_new_view, affaire_numero_new_view
from infolica.views.numero import numeros_etat_histo_new_view
from infolica.views.numero_relation import numeros_relations_new_view


@view_config(route_name='reservation_numeros', request_method='POST', renderer='json')
@view_config(route_name='reservation_numeros_s', request_method='POST', renderer='json')
def reservation_numeros_new_view(request):
    """
    Add new numeros in affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    nombre = int(request.params["nombre"]) if "nombre" in request.params else None
    affaire_id = int(request.params["affaire_id"]) if "affaire_id" in request.params else None
    cadastre_id = int(request.params["cadastre_id"]) if "cadastre_id" in request.params else None
    etat_id = int(request.params["etat_id"]) if "etat_id" in request.params else None
    type_id = int(request.params["type_id"]) if "type_id" in request.params else None
    numero_base_id = int(request.params["numero_base_id"]) if "numero_base_id" in request.params else None
    ppe_suffixe_start = request.params["ppe_suffixe_start"] if "ppe_suffixe_start" in request.params else None

    if not (affaire_id and nombre and cadastre_id and etat_id and type_id):
        raise CustomError(CustomError.GENERAL_EXCEPTION)

    settings = request.registry.settings

    # Récupère les id des états des biens-fonds de la config
    numero_projet_id = int(settings['numero_projet_id'])

    # Récupère les id des biens-fonds de la config
    numero_bf_id = int(settings['numero_bf_id'])
    numero_ddp_id = int(settings['numero_ddp_id'])
    numero_ppe_id = int(settings['numero_ppe_id'])
    numero_pcop_id = int(settings['numero_pcop_id'])
    affaire_numero_type_nouveau_id = int(settings['affaire_numero_type_nouveau_id'])
    numero_relation_mutation_id = int(settings['numero_relation_mutation_id'])
    numero_relation_ddp_id = int(settings['numero_relation_ddp_id'])
    numero_relation_ppe_id = int(settings['numero_relation_ppe_id'])
    numero_relation_pcop_id = int(settings['numero_relation_pcop_id'])

    # Définit la relation entre le numéro de base et le numéro associé
    # + Récupère l'id du suffixe de l'unité PPE de départ
    suffixe = None
    if type_id == numero_ddp_id:
        relation_type_id = numero_relation_ddp_id
    elif type_id == numero_ppe_id:
        relation_type_id = numero_relation_ppe_id
        unite_start_idx = Utils.get_index_from_unite(request.params["ppe_suffixe_start"].upper()) if "ppe_suffixe_start" in request.params else 0
    elif type_id == numero_pcop_id:
        relation_type_id = numero_relation_pcop_id
        suffixe = "part"

    # Récupère le dernier numéro de bien-fonds réservé dans le cadastre
    ln = Utils.last_number(request, cadastre_id, [numero_bf_id, numero_ddp_id, numero_ppe_id, numero_pcop_id])

    # Enregistrer le numéro
    for i in range(nombre):

        if type_id == numero_ppe_id:
            # Update 
            suffixe = Utils.get_unite_from_index(unite_start_idx + i)
        
        params = Utils._params(cadastre_id=cadastre_id, type_id=type_id, etat_id=etat_id, numero=ln+i+1, suffixe=suffixe)
        numero_id = numeros_new_view(request, params)
        # enregistrer le lien affaire-numéro
        params = Utils._params(affaire_id=affaire_id, numero_id=numero_id, actif=True, type_id=affaire_numero_type_nouveau_id)
        affaire_numero_new_view(request, params)
        # enregistrer l'historique de l'état
        params = Utils._params(numero_id=numero_id, numero_etat_id=etat_id)
        numeros_etat_histo_new_view(request, params)
        # enregistrer le numéro sur un bien-fonds de base si nécessaire
        if numero_base_id:
            params = Utils._params(numero_id_base=numero_base_id, numero_id_associe=numero_id, relation_type_id=relation_type_id, affaire_id=affaire_id)
            numeros_relations_new_view(request, params)


    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Numero.__tablename__))
