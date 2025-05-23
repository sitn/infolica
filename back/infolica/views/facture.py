# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Affaire, AffaireEtape, Client, ClientType, Numero
from infolica.models.models import EmolumentAffaire, EmolumentAffaireRepartition
from infolica.models.models import Facture, FactureType, VFactures
from infolica.scripts.mail_templates import MailTemplates
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
import json
from datetime import datetime

###########################################################
# FACTURE
###########################################################


@view_config(route_name="factures", request_method="GET", renderer="json")
@view_config(route_name="factures_s", request_method="GET", renderer="json")
def factures_view(request):
    """
    Return all factures
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(VFactures).all()
    return Utils.serialize_many(query)


@view_config(route_name="facture_type", request_method="GET", renderer="json")
def facture_type_view(request):
    """
    Return all facture types
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(FactureType).all()
    return Utils.serialize_many(query)


@view_config(route_name="affaires_factures_by_affaire_id", request_method="GET", renderer="json")
def affaires_factures_view(request):
    """
    Return all factures in affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict["id"]

    factures = (
        request.dbsession.query(
            Facture,
            Affaire,
            Client,
            ClientType,
            EmolumentAffaireRepartition,
        )
        .filter(Facture.client_id == Client.id)
        .filter(ClientType.id == Client.type_client)
        .filter(Facture.affaire_id == Affaire.id)
        .filter(Facture.affaire_id == affaire_id)
        .join(EmolumentAffaireRepartition, EmolumentAffaireRepartition.facture_id == Facture.id, isouter=True)
        .all()
    )

    facture_list = []
    for facture, affaire, client, client_type, emolumentAffaireRepartition in factures:

        compiled_adress = Utils.clientAdressFormatter(client, premiere_ligne=facture.client_premiere_ligne, sep="\n")
        client_remarque = Utils.clientRemarkBuilder(client)

        numeros = []
        numeros_id = []
        if facture.numeros is not None:
            numeros = request.dbsession.query(Numero.numero).filter(Numero.id.in_(facture.numeros)).order_by(Numero.numero.asc()).all()
            numeros = [num[0] for num in numeros]
            numeros_id = facture.numeros

        facture_list.append(
            {
                "id": facture.id,
                "affaire_id": affaire_id,
                "affaire_vref": affaire.vref,
                "type_id": facture.type_id,
                "sap": facture.sap,
                "client_type_id": client.type_client,
                "client_type": client_type.nom,
                "client_id": client.id,
                # "client_entreprise": client.entreprise,
                # "client_titre": client.titre,
                # "client_nom": client.nom,
                # "client_prenom": client.prenom,
                # "client_co": client.co,
                # "client_adresse": client.adresse,
                # "client_npa": client.npa,
                # "client_localite": client.localite,
                # "client_case_postale": client.case_postale,
                # "client_tel_fixe": client.tel_fixe,
                # "client_fax": client.fax,
                # "client_tel_portable": client.tel_portable,
                # "client_mail": client.mail,
                # "client_entree": datetime.strftime(client.entree, "%d.%m.%Y") if client.entree is not None else None,
                # "client_sortie": datetime.strftime(client.sortie, "%d.%m.%Y") if client.sortie is not None else None,
                "client_no_sap": client.no_sap,
                # "client_no_bdp_bdee": client.no_bdp_bdee,
                # "client_complement": facture.client_complement,
                "client_premiere_ligne": facture.client_premiere_ligne,
                "client_compiled_adress": compiled_adress,
                "client_remarque": client_remarque,
                "montant_mo": f"{facture.montant_mo:.2f}",
                "montant_mat_diff": f"{facture.montant_mat_diff:.2f}",
                "montant_rf": f"{facture.montant_rf:.2f}",
                "montant_tva": f"{facture.montant_tva:.2f}",
                "montant_total": f"{facture.montant_total:.2f}",
                "date": datetime.strftime(facture.date, "%d.%m.%Y") if facture.date is not None else None,
                "remarque": facture.remarque,
                "numeros": numeros,
                "numeros_id": numeros_id,
                "emolument_affaire_id": emolumentAffaireRepartition.emolument_affaire_id if emolumentAffaireRepartition else None,
            }
        )

    return facture_list


@view_config(route_name="factures", request_method="POST", renderer="json")
@view_config(route_name="factures_s", request_method="POST", renderer="json")
def factures_new_view(request):
    """
    Add new facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    params = {}
    for key in request.params:
        if key == "numeros":
            params[key] = json.loads(request.params[key])
        else:
            params[key] = request.params[key]

    Utils.addNewRecord(request, Facture, params)

    # send mail if client is new and outside canton NE
    if "client_id" in request.params:
        client_id = request.params["client_id"]
        affaire_id = request.params["affaire_id"]
        nb_etape_traitement = request.dbsession.query(AffaireEtape).filter(AffaireEtape.affaire_id == affaire_id).filter(AffaireEtape.etape_id == request.registry.settings["affaire_etape_traitement_id"]).count()
        if nb_etape_traitement >= 1:
            MailTemplates.sendMailClientHorsCanton(request, client_id, affaire_id)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Facture.__tablename__))


@view_config(route_name="factures", request_method="PUT", renderer="json")
@view_config(route_name="factures_s", request_method="PUT", renderer="json")
def factures_update_view(request):
    """
    Update facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    # id_facture
    id_facture = None

    if "id" in request.params:
        id_facture = request.params["id"]

    # Get the facture
    facture_record = request.dbsession.query(Facture).filter(Facture.id == id_facture).first()

    facture_client_id_old = int(facture_record.client_id)
    facture_client_id_new = int(request.params["client_id"]) if "client_id" in request.params else None

    params = {}
    for key in request.params:
        if key == "numeros":
            params[key] = json.loads(request.params[key])
        else:
            params[key] = request.params[key]

    if not facture_record:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(Facture.__tablename__, id_facture))

    facture_record = Utils.set_model_record(facture_record, params)

    # send mail if client is new and outside canton NE
    nb_etape_traitement = request.dbsession.query(AffaireEtape).filter(AffaireEtape.affaire_id == facture_record.affaire_id).filter(AffaireEtape.etape_id == request.registry.settings["affaire_etape_traitement_id"]).count()
    if facture_client_id_new and facture_client_id_old != facture_client_id_new and nb_etape_traitement >= 1:
        MailTemplates.sendMailClientHorsCanton(request, facture_record.client_id, facture_record.affaire_id)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Facture.__tablename__))


@view_config(route_name="factures", request_method="DELETE", renderer="json")
@view_config(route_name="factures_s", request_method="DELETE", renderer="json")
def factures_delete_view(request):
    """
    Delete facture
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    facture_id = request.params["id"] if "id" in request.params else None

    # Check if emolument_facture_repartition exists and delete it before
    results = request.dbsession.query(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.facture_id == facture_id).all()

    if results and len(results) > 0:
        for result in results:
            # set emolument to "unused" if this is not the case so it is set back to editable mode
            emol = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == result.emolument_affaire_id).first()

            emol.utilise = False

            # Remove emolument_facture_repartition
            request.dbsession.delete(result)

    # remove facture
    facture = request.dbsession.query(Facture).filter(Facture.id == facture_id).first()

    if not facture:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(Facture.__tablename__, facture_id))

    request.dbsession.delete(facture)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Facture.__tablename__))


@view_config(route_name="clients_factures_by_affaire_id", request_method="GET", renderer="json")
def clients_factures_by_affaire_view(request):
    """
    Return all client factures in affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict["id"]
    facture_type_facture_id = request.registry.settings["facture_type_facture_id"]

    results = request.dbsession.query(
        Facture,
        Client,
    ).filter(
        Facture.type_id == facture_type_facture_id
    ).filter(
        Facture.affaire_id == affaire_id
    ).filter(
        Facture.client_id == Client.id
    ).all()

    client_list = []
    count = 0
    for facture, client in results:
        compiled_adress = Utils.clientAdressFormatter(client, premiere_ligne=facture.client_premiere_ligne, sep="\n")
        compiled_adress_shortened = Utils.clientAdressFormatter(client, premiere_ligne=facture.client_premiere_ligne, shortened=True)

        if not any(x["client_adresse"] == compiled_adress for x in client_list):
            count += 1

            client_remarque = Utils.clientRemarkBuilder(client, checkNeedOtherClientFacture=False)

            client_list.append(
                {
                    "id": count,
                    "client_id": client.id,
                    "client_adresse_court": compiled_adress_shortened,
                    "client_adresse": compiled_adress,
                    "client_remarque": client_remarque,
                }
            )

    return client_list
