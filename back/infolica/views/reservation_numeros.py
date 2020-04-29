from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
from .. import models
from ..views.numero import numeros_new_view, affaire_numero_new_view, numeros_etat_histo_new_view
from ..views.numero_relation import numeros_relations_new_view

""" Add new numeros in affaire"""
@view_config(route_name='reservation_numeros', request_method='POST', renderer='json')
@view_config(route_name='reservation_numeros_s', request_method='POST', renderer='json')
def reservation_numeros_new_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_numero_edition']):
        raise exc.HTTPForbidden()

    # Get affaire_id
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    cadastre_id = request.params['cadastre_id'] if 'cadastre_id' in request.params else None
    plan_id = request.params['plan_id'] if 'plan_id' in request.params else None

    # Get first available number (BF, DDP, PPE, PCOP)
    ln = Utils.last_number(request, cadastre_id, [1, 2, 3, 4])

    c = 0
    # Biens-fonds
    if 'bf' in request.params:
        for i in range(int(request.params['bf'])):
            c += 1
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=1, etat_id=1, numero=ln + c)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)
            # enregistrer l'historique de l'état
            params = Utils._params(numero_id=numero_id, numero_etat_id=1)
            numeros_etat_histo_new_view(request, params)

    if 'ddp' in request.params:
        for i in range(int(request.params['ddp'])):
            c += 1
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=2, etat_id=1, numero=ln + c)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)
            # enregistrer l'historique de l'état
            params = Utils._params(numero_id=numero_id, numero_etat_id=1)
            numeros_etat_histo_new_view(request, params)
            # enregistrer le DDP sur un bien-fonds de base
            numero_id_base = request.params['ddp_base'] if 'ddp_base' in request.params else None
            params = Utils._params(numero_id_base=numero_id_base, numero_id_associe=numero_id, relation_type_id=2, affaire_id=affaire_id)
            numeros_relations_new_view(request, params)

    if 'ppe' in request.params:
        unite_start_idx = Utils.get_index_from_unite(
            request.params["ppe_unite"].upper()) if "ppe_unite" in request.params else 0
        for i in range(int(request.params['ppe'])):
            c += 1
            # enregistrer un nouveau numéro
            suffixe = Utils.get_unite_from_index(unite_start_idx + i)
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=3, etat_id=1, numero=ln + c, suffixe=suffixe)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)
            # enregistrer l'historique de l'état
            params = Utils._params(numero_id=numero_id, numero_etat_id=1)
            numeros_etat_histo_new_view(request, params)
            # enregistrer le DDP sur un bien-fonds de base
            numero_id_base = request.params['ppe_base'] if 'ppe_base' in request.params else None
            params = Utils._params(numero_id_base=numero_id_base, numero_id_associe=numero_id, relation_type_id=3, affaire_id=affaire_id)
            numeros_relations_new_view(request, params)

    if 'pcop' in request.params:
        for i in range(int(request.params['pcop'])):
            c += 1
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=4, etat_id=1, numero=ln + c, suffixe="part")
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)
            # enregistrer l'historique de l'état
            params = Utils._params(numero_id=numero_id, numero_etat_id=1)
            numeros_etat_histo_new_view(request, params)
            # enregistrer le DDP sur un bien-fonds de base
            numero_id_base = request.params['pcop_base'] if 'pcop_base' in request.params else None
            params = Utils._params(numero_id_base=numero_id_base, numero_id_associe=numero_id, relation_type_id=4, affaire_id=affaire_id)
            numeros_relations_new_view(request, params)

    if 'pfp3' in request.params:
        ln = Utils.last_number(request, cadastre_id, [5])
        for i in range(int(request.params['pfp3'])):
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=5, etat_id=2, numero=ln + i+1)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)

    if 'bat' in request.params:
        ln = Utils.last_number(request, cadastre_id, [6])
        for i in range(int(request.params['bat'])):
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=6, etat_id=2, numero=ln + i+1)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)
    
    if 'dp' in request.params:
        ln = Utils.last_number(request, cadastre_id, [6])
        for i in range(int(request.params['dp'])):
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=10, etat_id=2, numero=ln + i+1)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)

    if 'pcs' in request.params:
        ln = Utils.last_number(request, cadastre_id, [7])
        for i in range(int(request.params['pcs'])):
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=7, etat_id=2, numero=ln + i+1)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)

    if 'paux' in request.params:
        ln = Utils.last_number(request, cadastre_id, [8], plan_id=plan_id)
        for i in range(int(request.params['paux'])):
            # enregistrer un nouveau numéro
            params = Utils._params(
                cadastre_id=cadastre_id, type_id=8, etat_id=2, numero=ln + i+1, plan_id=plan_id)
            numero_id = numeros_new_view(request, params)
            # enregistrer le lien affaire-numéro
            params = Utils._params(
                affaire_id=affaire_id, numero_id=numero_id, modifie=False, type_id=2)
            affaire_numero_new_view(request, params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Numero.__tablename__))

