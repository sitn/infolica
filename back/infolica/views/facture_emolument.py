# -*- coding: utf-8 -*--
import datetime
import json
import math

import pyramid.httpexceptions as exc
import requests
from infolica.models.constant import Constant
from infolica.models.models import Affaire, AffaireNumero, Cadastre, Emolument, EmolumentAffaire, EmolumentAffaireRepartition, Facture, FactureParametres, Numero, TableauEmoluments, VAffaire, VNumerosAffaires
from infolica.scripts.authentication import check_connected
from infolica.scripts.utils import Utils
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import func, or_
from sqlalchemy.sql.elements import and_

###########################################################
# EMOLUMENTS
###########################################################


def _round_nearest(x, a=0.05):
    return round(round(x / a) * a, -int(math.floor(math.log10(a))))


def _numeros_emoluments_affaire(request, affaire_id):
    affaire_numero_type_ancien_id = int(request.registry.settings["affaire_numero_type_ancien_id"])

    num_aff = (
        request.dbsession.query(Numero.id, Numero.numero, Cadastre.nom)
        .join(Cadastre, Cadastre.id == Numero.cadastre_id)
        .join(AffaireNumero, AffaireNumero.numero_id == Numero.id)
        .filter(AffaireNumero.affaire_id == affaire_id, AffaireNumero.type_id == affaire_numero_type_ancien_id)
        .order_by(Cadastre.nom, Numero.numero)
        .all()
    )

    num_emol = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.affaire_id == affaire_id).all()

    numeros = []
    for num_aff_i in num_aff:
        numero_i = {"numero_id": num_aff_i.id, "numero": num_aff_i.numero, "cadastre": num_aff_i.nom, "emolument_affaire_id": None}

        for ne in num_emol:
            if num_aff_i.id in ne.numeros_id:
                numero_i["emolument_affaire_id"] = ne.id
                break

        numeros.append(numero_i)

    return numeros


@view_config(route_name="facture_parametres", request_method="GET", renderer="json")
def tableau_facture_parametres_view(request):
    """
    Return actual parameters and values
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    today = datetime.date.today()
    results = (
        request.dbsession.query(FactureParametres)
        .filter(
            FactureParametres.valable_de <= today,
            or_(
                FactureParametres.valable_a >= today,
                FactureParametres.valable_a == None,
            ),
        )
        .all()
    )

    params = {}
    for result in results:
        if result.nom not in params.keys():
            params[result.nom] = result.valeur

    return {"facture_parametres": params}


@view_config(route_name="emolument_affaire", request_method="GET", renderer="json")
def emolument_affaire_view(request):
    """
    Return emolument_affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params["affaire_id"] if "affaire_id" in request.params else None

    query = request.dbsession.query(EmolumentAffaire)

    if affaire_id is not None:
        query = query.filter(EmolumentAffaire.affaire_id == affaire_id)

    emolument_affaire = query.all()

    # Récupérer les données des bâtiments
    result = []
    for emolument_affaire_i in emolument_affaire:
        query_bat = (
            request.dbsession.query(Emolument.batiment, Emolument.batiment_f)
            .filter(Emolument.emolument_affaire_id == emolument_affaire_i.id)
            .filter(Emolument.batiment > 0)
            .group_by(Emolument.batiment, Emolument.batiment_f)
            .order_by(Emolument.batiment.asc())  # Really important with respect to implementation of loading form_detail_batiment in front !!
            .all()
        )

        batiment_f = [y for _, y in query_bat]
        numeros = []
        numeros_id = []
        if emolument_affaire_i.numeros_id and len(emolument_affaire_i.numeros_id) > 0:
            numeros_id = emolument_affaire_i.numeros_id
            numeros = Utils.serialize_many(request.dbsession.query(VNumerosAffaires).filter(and_(VNumerosAffaires.numero_id.in_(tuple(emolument_affaire_i.numeros_id)), VNumerosAffaires.affaire_id == emolument_affaire_i.affaire_id)).all())

        # Récupérer les liens sur la facture (répartition des montants)
        facture_repartition = Utils.serialize_many(request.dbsession.query(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_i.id).all())

        result.append(
            Utils._params(
                id=emolument_affaire_i.id,
                affaire_id=emolument_affaire_i.affaire_id,
                pente_pc=emolument_affaire_i.pente_pc,
                diff_visibilite_pc=emolument_affaire_i.diff_visibilite_pc,
                trafic_pc=emolument_affaire_i.trafic_pc,
                zi=emolument_affaire_i.zi,
                indice_application=emolument_affaire_i.indice_application,
                tva_pc=emolument_affaire_i.tva_pc,
                remarque=emolument_affaire_i.remarque,
                nb_batiments=len(batiment_f),
                batiment_f=batiment_f,
                numeros_id=numeros_id,
                numeros=numeros,
                facture_type_id=emolument_affaire_i.facture_type_id,
                utilise=emolument_affaire_i.utilise,
                facture_repartition=facture_repartition,
            )
        )

    return result


@view_config(route_name="emolument", request_method="GET", renderer="json")
def emolument_view(request):
    """
    Return emoluments of emoluments_affaire
    """
    if not check_connected(request):
        raise exc.HTTPForbidden()

    today = datetime.date.today()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None
    emoluments_divers_tarifhoraire_id = int(request.registry.settings["emoluments_divers_tarifhoraire_id"])

    emol_affaire = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == emolument_affaire_id).first()
    form_general = Utils.serialize_one(emol_affaire)

    if emol_affaire.utilise is True:
        today_last = today
        fact = request.dbsession.query(Facture).join(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == emol_affaire.id).first()
        today = getattr(fact, "date", None)
        if today is None:
            today = request.dbsession.query(Affaire.date_envoi).filter(Affaire.id == emol_affaire.affaire_id).scalar()
        if today is None:
            today = today_last

    nb_batiments = request.dbsession.query(func.max(Emolument.batiment)).filter(Emolument.emolument_affaire_id == emolument_affaire_id).scalar()
    if nb_batiments is None:
        nb_batiments = 0

    existing_emoluments_query = request.dbsession.query(Emolument).filter(Emolument.emolument_affaire_id == emolument_affaire_id)

    # emoluments
    table = request.dbsession.query(TableauEmoluments).filter(TableauEmoluments.date_entree <= today, or_(TableauEmoluments.date_sortie > today, TableauEmoluments.date_sortie == None)).order_by(TableauEmoluments.categorie_id, TableauEmoluments.sous_categorie_id, TableauEmoluments.ordre).all()

    emoluments = []
    divers_tarifhoraire = []
    c = 0
    last_categorie_id = ""
    last_sous_categorie_id = ""
    categorie = []
    sous_categorie = []
    batiments_f = [0] * nb_batiments
    for position in table:
        if position.id == emoluments_divers_tarifhoraire_id:
            existing_emoluments = existing_emoluments_query.filter(Emolument.tableau_emolument_id == int(emoluments_divers_tarifhoraire_id)).all()
            for ee in existing_emoluments:
                position_ = {
                    "nom": ee.position,
                    "nombre": ee.nombre,
                    "montant": ee.prix_unitaire,
                    "prix": ee.montant,
                }
                divers_tarifhoraire.append(position_)
            continue

        c += 1
        if c > 1:
            if last_sous_categorie_id != position.sous_categorie_id or (last_sous_categorie_id == position.sous_categorie_id and last_categorie_id != position.categorie_id):
                # New category
                categorie.append(sous_categorie)
                sous_categorie = []
            if last_categorie_id != position.categorie_id:
                # New subcategory
                emoluments.append(categorie)
                categorie = []

        position_ = Utils.serialize_one(position)
        position_["nombre"] = [0] * (nb_batiments + 1)
        position_["prix"] = [0] * (nb_batiments + 1)

        # check if emolument already exists un database
        existing_emoluments = existing_emoluments_query.filter(Emolument.tableau_emolument_id == int(position_["id"])).all()
        for ee in existing_emoluments:
            position_["nombre"][ee.batiment] = ee.nombre
            position_["prix"][ee.batiment] = ee.montant
            if ee.batiment > 0 and batiments_f[ee.batiment - 1] == 0:
                batiments_f[ee.batiment - 1] = ee.batiment_f

        sous_categorie.append(position_)

        last_categorie_id = position.categorie_id
        last_sous_categorie_id = position.sous_categorie_id

    categorie.append(sous_categorie)
    emoluments.append(categorie)

    form_general["batiment_f"] = batiments_f
    form_general["nb_batiments"] = len(batiments_f)

    numeros = _numeros_emoluments_affaire(request, form_general["affaire_id"])

    return {"emoluments": json.dumps(emoluments), "form_general": json.dumps(form_general), "divers_tarifhoraire": json.dumps(divers_tarifhoraire), "numeros": json.dumps(numeros)}


@view_config(route_name="emolument", request_method="POST", renderer="json")
def emolument_new_view(request):
    """
    Add new emolument
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    emoluments_divers_tarifhoraire_id = int(request.registry.settings["emoluments_divers_tarifhoraire_id"])

    form_general = json.loads(request.params["form_general"]) if "form_general" in request.params else None
    emoluments = json.loads(request.params["emoluments"]) if "emoluments" in request.params else None
    divers_tarifhoraire = json.loads(request.params["divers_tarifhoraire"]) if "divers_tarifhoraire" in request.params else None

    # save form_general
    if form_general["id"] is None:
        emol_affaire = EmolumentAffaire()
        emol_affaire = Utils.set_model_record(emol_affaire, form_general)
        request.dbsession.add(emol_affaire)
        request.dbsession.flush()
    else:
        emol_affaire = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == form_general["id"]).first()
        emol_affaire = Utils.set_model_record(emol_affaire, form_general)
        request.dbsession.flush()

    # save form_general
    existing_emoluments = request.dbsession.query(Emolument).filter(Emolument.emolument_affaire_id == emol_affaire.id).all()
    for emol in existing_emoluments:
        request.dbsession.delete(emol)

    for category in emoluments:
        for scategory in category:
            for position in scategory:
                for i in range(len(position["nombre"])):
                    if float(position["nombre"][i] or 0) > 0 or float(position["prix"][i] or 0) > 0:
                        params = Utils._params(
                            emolument_affaire_id=emol_affaire.id,
                            tableau_emolument_id=int(position["id"]),
                            position=position["nom"],
                            prix_unitaire=_round_nearest(float(position["montant"]) or 0),
                            nombre=float(position["nombre"][i] or "0"),
                            batiment=i,
                            batiment_f=1 if i == 0 else float(form_general["batiment_f"][i - 1]),
                            montant=_round_nearest(float(position["prix"][i]) or 0),
                        )

                        # save emolument
                        record = Emolument()
                        record = Utils.set_model_record(record, params)

                        request.dbsession.add(record)

    # save divers tarif horaire
    for dth in divers_tarifhoraire:
        if dth["nom"] is not None and dth["nombre"] is not None and dth["montant"] is not None and dth["nom"] != "" and dth["nombre"] != "" and dth["montant"] != "":
            params = Utils._params(
                emolument_affaire_id=emol_affaire.id, tableau_emolument_id=emoluments_divers_tarifhoraire_id, position=dth["nom"], prix_unitaire=_round_nearest(float(dth["montant"]) or 0), nombre=float(dth["nombre"]), batiment=0, batiment_f=1, montant=_round_nearest(float(dth["prix"]) or 0)
            )

            # save emolument
            record = Emolument()
            record = Utils.set_model_record(record, params)

            request.dbsession.add(record)

    return {"emolument_affaire_id": emol_affaire.id}


@view_config(route_name="emolument", request_method="DELETE", renderer="json")
def emolument_delete_view(request):
    """
    Delete emolument
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None

    # get emolument affaire
    emol_affaire = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == emolument_affaire_id).first()

    # delete linked emoluments
    existing_emoluments = request.dbsession.query(Emolument).filter(Emolument.emolument_affaire_id == emol_affaire.id).all()
    for emol in existing_emoluments:
        request.dbsession.delete(emol)

    # get emolument_affaire_repartition and delete them if exist
    ear = request.dbsession.query(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_id).all()
    for ear_i in ear:
        request.dbsession.delete(ear_i)

    request.dbsession.flush()

    # finally delete emolument affaire
    request.dbsession.delete(emol_affaire)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(EmolumentAffaire.__tablename__))


@view_config(route_name="emolument_affaire_freeze", request_method="PUT", renderer="json")
def update_emolument_affaire_freeze_view(request):
    """
    Freeze emolument_affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    params = request.params

    record_id = params["emolument_affaire_id"] if "emolument_affaire_id" in params else None

    record = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == record_id).first()

    record = Utils.set_model_record(record, params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentAffaire.__tablename__))


#######################################
###  EMOLUMENT AFFAIRE REPARTITION  ###
#######################################


@view_config(route_name="emolument_affaire_repartiton", request_method="GET", renderer="json")
def emolument_affaire_repartiton_view(request):
    """
    get emolument_affaire_repartiton
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    records = request.dbsession.query(EmolumentAffaireRepartition)

    if "emolument_affaire_id" in request.params:
        records = records.filter(EmolumentAffaireRepartition.emolument_affaire_id == request.params["emolument_affaire_id"])

    if "facture_id" in request.params:
        records = records.filter(EmolumentAffaireRepartition.facture_id == request.params["facture_id"])

    records = records.all()

    if len(records) > 0:
        return Utils.serialize_many(records)
    else:
        return []


@view_config(route_name="emolument_affaire_repartiton", request_method="POST", renderer="json")
def emolument_affaire_repartiton_new_view(request):
    """
    Add new emolument_affaire_repartiton
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None
    emolument_facture_repartition = json.loads(request.params["emolument_facture_repartition"]) if "emolument_facture_repartition" in request.params else None

    # get records of current emolument_affaire_id
    emolumentAffaireRepartition = request.dbsession.query(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_id).all()

    # iterate through emolument_facture_repartition
    for efr_i in emolument_facture_repartition:
        # test if efr_i exists already in db
        record = None
        for idx, eaf_i in enumerate(emolumentAffaireRepartition):
            if eaf_i.facture_id == efr_i["id"]:
                # La relation existe déjà, la modifier
                record = emolumentAffaireRepartition.pop(idx)
                break

        if record is not None:
            if float(record.repartition) != float(efr_i["emolument_repartition"]):
                if float(efr_i["emolument_repartition"]) == 0:
                    # supprimer l'entrée car la répartition est nulle
                    request.dbsession.delete(record)
                else:
                    # enregistrer la nouvelle répartition
                    params = Utils._params(facture_id=efr_i["id"], emolument_affaire_id=emolument_affaire_id, repartition=efr_i["emolument_repartition"])
                    record = Utils.set_model_record(record, params)

        else:
            # Créer l'entrée inexistante et si la répartition est non nulle
            if float(efr_i["emolument_repartition"]) > 0:
                record = EmolumentAffaireRepartition()
                params = Utils._params(facture_id=efr_i["id"], emolument_affaire_id=emolument_affaire_id, repartition=efr_i["emolument_repartition"])
                record = Utils.set_model_record(record, params)

                request.dbsession.add(record)

    # remove items in db not posted
    for item in emolumentAffaireRepartition:
        request.dbsession.delete(item)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentAffaireRepartition.__tablename__))


@view_config(route_name="emolument_affaire_repartiton", request_method="DELETE", renderer="json")
def emolument_affaire_repartiton_delete_view(request):
    """
    Delete emolument_affaire_repartiton by emolument_affaire_id
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings["affaire_facture_edition"]):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None

    records = request.dbsession.query(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_id).all()

    for record in records:
        request.dbsession.delete(record)


@view_config(route_name="tableau_emoluments_new", request_method="GET", renderer="json")
def tableau_emoluments_new_view(request):
    """
    Get tableau of emoluments
    """
    # Check authorization
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.params["affaire_id"] if "affaire_id" in request.params else None

    today = datetime.date.today()

    emoluments_divers_tarifhoraire_id = int(request.registry.settings["emoluments_divers_tarifhoraire_id"])

    # get active emoluments
    table = (
        request.dbsession.query(TableauEmoluments)
        .filter(
            TableauEmoluments.date_entree <= today,
            or_(TableauEmoluments.date_sortie > today, TableauEmoluments.date_sortie == None),
            TableauEmoluments.id != emoluments_divers_tarifhoraire_id,  # dont take into account diver-tarif-horaire which is generated by the front of the application
        )
        .order_by(TableauEmoluments.categorie_id, TableauEmoluments.sous_categorie_id, TableauEmoluments.ordre)
        .all()
    )

    result = []
    c = 0
    last_categorie_id = ""
    last_sous_categorie_id = ""
    categorie = []
    sous_categorie = []
    for position in table:
        c += 1
        if c > 1:
            if last_sous_categorie_id != position.sous_categorie_id or (last_sous_categorie_id == position.sous_categorie_id and last_categorie_id != position.categorie_id):
                categorie.append(sous_categorie)
                sous_categorie = []
            if last_categorie_id != position.categorie_id:
                result.append(categorie)
                categorie = []

        sous_categorie.append(Utils.serialize_one(position))

        last_categorie_id = position.categorie_id
        last_sous_categorie_id = position.sous_categorie_id

    categorie.append(sous_categorie)
    result.append(categorie)

    numeros = _numeros_emoluments_affaire(request, affaire_id)

    return {"emoluments": result, "numeros": numeros}


@view_config(route_name="export_emoluments_pdf", request_method="POST")
def export_emoluments_pdf_view(request):
    """
    Create PDF of emoluments
    """
    # Check authorization
    if not check_connected(request):
        raise exc.HTTPForbidden()

    now = datetime.datetime.now()

    # get request params
    tableau_emoluments_id = request.params["tableau_emoluments_id"] if "tableau_emoluments_id" in request.params else None
    affaire_id = request.params["affaire_id"] if "affaire_id" in request.params else None
    tableau_emoluments_html = request.params["tableau_emoluments_html"] if "tableau_emoluments_html" in request.params else None
    tableau_recapitulatif_html = request.params["tableau_recapitulatif_html"] if "tableau_recapitulatif_html" in request.params else None

    # get facture_id
    factures = request.dbsession.query(Facture).join(EmolumentAffaireRepartition).filter(EmolumentAffaireRepartition.emolument_affaire_id == tableau_emoluments_id).all()

    # get affaire
    affaire = request.dbsession.query(VAffaire).filter(VAffaire.id == affaire_id).first()

    # get bf_emolument
    numeros_id = request.dbsession.query(EmolumentAffaire).filter(EmolumentAffaire.id == tableau_emoluments_id).first().numeros_id
    emolument_bf_html = None
    if numeros_id is not None:
        emolument_bf_html = []
        for num_id in numeros_id:
            emolument_bf_html.append(str(request.dbsession.query(Numero).filter(Numero.id == num_id).first().numero))

        emolument_bf_html = ", ".join(emolument_bf_html)

    d = {"now": now.strftime("%d.%m.%Y, %H:%M:%S")}

    header_str = '<html><head><meta charset="utf-8"><style>'

    ppp = """
        .logo {{
            width: 3.68cm;
            image-resolution: 300dpi
        }}
        table {{
        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
        border-collapse: collapse;
        max-width: 17cm !important;
        }}
        tr:nth-child(even){{background-color: #f2f2f2;}}
        th {{
        padding-top: 1mm;
        padding-bottom: 1mm;
        text-align: left;
        background-color: #499c6c;
        color: white;
        }}
        @page {{
            size: A4 portrait;
            margin: 2cm;
            counter-increment: page;
            @bottom-center {{
                content: "Page " counter(page) " de " counter(pages) ", impression du {now}";
                font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 7pt;
                border-top: .25pt solid #666;
                width: 60%;
            }}
            @bottom-right {{
                content: "SERVICE DE LA GEOMATIQUE ET DU REGISTRE FONCIER";
                font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 7pt;
            }}
        }}
        h1 {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 15pt; font-style: normal; font-variant: normal; font-weight: 700; line-height: 20pt; }}
        p {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 8pt; font-style: normal; font-variant: normal; font-weight: 400; line-height: 9pt; }}
        th {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 8pt; font-style: normal; font-variant: normal; font-weight: bold; line-height: 9pt; border-color: black; border-style: solid; border-width: 0.1mm; }}
        td {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 8pt; font-style: normal; font-variant: normal; font-weight: 400; line-height: 9pt; border-color: black; border-style: solid; border-width: 0.1mm; }}

        .nbInput {{ width: 3mm; text-align: center; }}
        .nbField {{ margin: 0mm; margin-bottom: 1mm; min-height: 1mm !important; padding: 1mm 0mm 0mm 0mm !important; }}
        .subtitle {{ background-color: lightgray; }}
        .alignRight {{ text-align: right !important; }}
        .alignCenter {{ text-align: center !important; }}
        .notEditable {{ background-color: lightgray; }}
        .montantTotal {{ font-weight: bold; }}
        .tabulation {{ padding-left: 7.5mm !important; font-style: italic; }}
        .tabulation-2 {{ padding-left: 15mm !important; font-style: italic; }}
        .batiment-separator {{ border-left: 0.3mm solid black !important; }}
        .code {{ max-width: 5mm!important; }}
        .position {{ max-width: 50mm !important; }}
        .position_divers {{ max-width: 50mm !important; }}
        .position_recapitulatif {{ max-width: 10mm !important; }}
        .unite {{ width: 15mm !important; }}
        .prix_unitaire {{ width: 15mm !important; }}
        .nombre {{ width: 5mm !important; }}
        .montant {{ width: 16mm !important;; }}
        .overHead {{ line-break: normal !important; font-weight: normal !important; font-style: italic; text-align: left; border-top: 0mm !important; border-left: 0mm !important; border-right: 0mm !important; padding-bottom: 1mm !important; }}
        .rowChapterDistinction {{ border-top: 0.3mm solid; }}
        """

    header_str += ppp.format(**d)
    header_str += "</style></head><body>"
    header_str += "<img class='logo' src='https://sitn.ne.ch/web/images/06ne.ch_RVB.png' alt='Logo'>"
    header_str += '<p style="font-size: 8pt; line-height: 8pt; margin-top: 0mm; padding-top: 1mm; margin-left: 0mm; padding-left: 0mm;"><b>DÉPARTEMENT DU DÉVELOPPEMENT<br> \
                    TERRITORIAL ET DE L\'ENVIRONNEMENT</b><br> \
                    SERVICE DE LA GÉOMATIQUE ET<br> \
                    DU REGISTRE FONCIER</p>'

    header_str += "<h1>Tableau des émoluments de la mensuration officielle</h1>"
    header_str += "<p>Affaire n° " + str(affaire_id) + " sur le cadastre: " + affaire.cadastre + "</p>"

    # numéros de BF s'ils sont rattachés
    if emolument_bf_html is not None and emolument_bf_html != "":
        header_str += "<p>Bien(s)-fonds n° " + emolument_bf_html + "</p>"
    header_str += "<p>Emolument n° " + str(tableau_emoluments_id) + "</p>"

    # edit facture_html
    if len(factures) == 0:
        factures_html = "Aucune facture rattachée à l'émolument"
    else:
        factures_html = []
        for facture in factures:
            if facture.sap is not None and facture.date is not None:
                factures_html.append("n°" + str(facture.sap) + " du " + datetime.datetime.strftime(facture.date, "%d.%m.%Y"))
        factures_html = " / ".join(factures_html)
    if factures_html == "" or factures_html == []:
        factures_html = "La facture n'a pas encore été envoyée"

    header_str += "<p>Facture(s): " + factures_html + "</p>"

    tableau_emoluments_html = header_str + tableau_emoluments_html
    tableau_emoluments_html += '<br><p style="font-size:15pt;"><b>Récapitulatif</b></p>'
    tableau_emoluments_html += tableau_recapitulatif_html + "</body></html>"

    filename = "Tableau_émoluments_" + str(tableau_emoluments_id) + "_Affaire_" + str(affaire_id) + ".pdf"

    result = requests.post(request.registry.settings["weasyprint_baseurl"] + filename, data=tableau_emoluments_html)

    response = Response(result.content)
    params = response.content_type_params
    params["filename"] = filename
    response.content_type = "application/pdf"
    response.content_type_params = params
    return response
    tableau_emoluments_html = header_str + tableau_emoluments_html
    tableau_emoluments_html += '<br><p style="font-size:15pt;"><b>Récapitulatif</b></p>'
    tableau_emoluments_html += tableau_recapitulatif_html + "</body></html>"

    filename = "Tableau_émoluments_" + str(tableau_emoluments_id) + "_Affaire_" + str(affaire_id) + ".pdf"

    result = requests.post(request.registry.settings["weasyprint_baseurl"] + filename, data=tableau_emoluments_html)

    response = Response(result.content)
    params = response.content_type_params
    params["filename"] = filename
    response.content_type = "application/pdf"
    response.content_type_params = params
    return response
