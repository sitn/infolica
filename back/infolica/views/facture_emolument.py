# -*- coding: utf-8 -*--
from sqlalchemy.sql.elements import and_
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.response import Response


from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Facture, TableauEmoluments, VNumerosAffaires
from infolica.models.models import EmolumentAffaire, Emolument, EmolumentAffaireRepartition
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
import json
import datetime
import requests

###########################################################
# EMOLUMENTS
###########################################################


@view_config(route_name='tableau_emoluments', request_method='GET', renderer='json')
def tableau_emoluments_view(request):
    """
    Return table of emoluments 
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(TableauEmoluments).order_by(TableauEmoluments.id).all()
    return Utils.serialize_many(query)


@view_config(route_name='emolument_affaire', request_method='GET', renderer='json')
def emolument_affaire_view(request):
    """
    Return emolument_affaire
    """
    # Check connected
    if not check_connected(request):
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
        ).order_by(
            Emolument.batiment.asc() # Really important with respect to implementation of loading form_detail_batiment in front !! 
        ).all()
        
        batiment_f = [y for _, y in query_bat]
        numeros = []
        numeros_id = []
        if emolument_affaire_i.numeros_id and len(emolument_affaire_i.numeros_id) > 0:
            numeros_id = emolument_affaire_i.numeros_id
            numeros = Utils.serialize_many(request.dbsession.query(VNumerosAffaires).filter(
                and_(
                    VNumerosAffaires.numero_id.in_(tuple(emolument_affaire_i.numeros_id)),
                    VNumerosAffaires.affaire_id == emolument_affaire_i.affaire_id
                )
            ).all())
        
        # Récupérer les liens sur la facture (répartition des montants)
        facture_repartition = Utils.serialize_many(
            request.dbsession.query(EmolumentAffaireRepartition).filter(
                EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_i.id
            ).all()
        )

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
                batiment_f = batiment_f,
                numeros_id = numeros_id,
                numeros = numeros,
                facture_type_id = emolument_affaire_i.facture_type_id,
                utilise = emolument_affaire_i.utilise,
                facture_repartition = facture_repartition
            )
        )
    
    return result


@view_config(route_name='emolument', request_method='GET', renderer='json')
def emolument_view(request):
    """
    Return emoluments of emoluments_affaire 
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    # get TableauEmoluments
    tableauEmoluments = request.dbsession.query(
        TableauEmoluments
    ).filter(
        TableauEmoluments.date_sortie == None
    ).all()

    tableauEmoluments = Utils.serialize_many(tableauEmoluments)

    # get emolumentsAffaire saved with emolument_affaire_id
    emolument_affaire_id = request.params['emolument_affaire_id'] if 'emolument_affaire_id' in request.params else None

    emolumentsAffaire = request.dbsession.query(
        Emolument
    ).filter(
        Emolument.emolument_affaire_id == emolument_affaire_id
    ).all()

    emolumentsAffaire = Utils.serialize_many(emolumentsAffaire)

    # check if emolumentAffaire is used
    emolumentAffaireUsed = request.dbsession.query(
        EmolumentAffaire.utilise
    ).filter(
        EmolumentAffaire.id == emolument_affaire_id
    ).scalar()

    for ea in emolumentsAffaire:
        for te in tableauEmoluments:
            if ea['tableau_emolument_id'] == te['id'] and not emolumentAffaireUsed and not te['montant'] == 0:
                ea['prix_unitaire'] = te['montant']
                ea['montant'] = ea['nombre'] * ea['prix_unitaire'] * ea['batiment_f']

    return emolumentsAffaire


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
                    nombre=float(batiment_i[emolument_i]['nombre']),
                    batiment=int(batiment_i[emolument_i]['batiment']),
                    batiment_f=float(batiment_i[emolument_i]['batiment_f']),
                    montant=float(batiment_i[emolument_i]['montant'])
                )

                record = Emolument()
                record = Utils.set_model_record(record, params)

                request.dbsession.add(record)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Emolument.__tablename__))


@view_config(route_name='emolument_affaire', request_method='PUT', renderer='json')
def update_emolument_affaire_view(request):
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


@view_config(route_name='emolument_affaire_freeze', request_method='PUT', renderer='json')
def update_emolument_affaire_freeze_view(request):
    """
    Freeze emolument_affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    params = request.params
    
    record_id = params['emolument_affaire_id'] if 'emolument_affaire_id' in params else None

    record = request.dbsession.query(EmolumentAffaire).filter(
        EmolumentAffaire.id == record_id
    ).first()

    record = Utils.set_model_record(record, params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentAffaire.__tablename__))


@view_config(route_name='emolument', request_method='PUT', renderer='json')
def update_emolument_view(request):
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

    emoluments = query.all()

    for batiment_i in data:
        for emolument_i in batiment_i:
            record = None
            for index, item in enumerate(emoluments):
                if (item.batiment == batiment_i[emolument_i]['batiment'] and 
                    item.tableau_emolument_id == batiment_i[emolument_i]['tableau_emolument_id']):
                    record = emoluments.pop(index)
                    break
            

            if not record is None:
                # comparer les valeurs enregistrées
                if (not float(record.montant) == float(batiment_i[emolument_i]['montant']) \
                    or not record.position == batiment_i[emolument_i]['nom'] \
                    or not float(record.prix_unitaire) == float(batiment_i[emolument_i]['prix_unitaire']) \
                    or not float(record.nombre) == float(batiment_i[emolument_i]['nombre']) \
                    or not float(record.batiment_f) == float(batiment_i[emolument_i]['batiment_f'])):

                    # Mettre à jour les données si le nouveau montant n'est pas nul
                    if float(batiment_i[emolument_i]['montant']) > 0:
                        params = Utils._params(
                            position=batiment_i[emolument_i]['nom'],
                            prix_unitaire=float(batiment_i[emolument_i]['prix_unitaire']),
                            nombre=float(batiment_i[emolument_i]['nombre']),
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
                        nombre=float(batiment_i[emolument_i]['nombre']),
                        batiment=int(batiment_i[emolument_i]['batiment']),
                        batiment_f=float(batiment_i[emolument_i]['batiment_f']),
                        montant=float(batiment_i[emolument_i]['montant'])
                    )

                    record = Emolument()
                    record = Utils.set_model_record(record, params)

                    request.dbsession.add(record)

    # delete all remaining emoluments
    for item in emoluments:
        request.dbsession.delete(item)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Emolument.__tablename__))


@view_config(route_name='emolument_affaire', request_method='DELETE', renderer='json')
def emolument_affaire_delete_view(request):
    """
    Delete emolument_affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params['emolument_affaire_id'] if "emolument_affaire_id" in request.params else None
    affaire_id = request.params['affaire_id'] if "affaire_id" in request.params else None

    # Remove from EmolumentAffaire
    record = request.dbsession.query(EmolumentAffaire).filter(
        EmolumentAffaire.id == emolument_affaire_id
    ).filter(
        EmolumentAffaire.affaire_id == affaire_id
    ).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(EmolumentAffaire.__tablename__, emolument_affaire_id))

    request.dbsession.delete(record)

    # Remove from Emolument
    records = request.dbsession.query(Emolument).filter(
        Emolument.emolument_affaire_id == emolument_affaire_id
    ).all()

    for record in records:
        request.dbsession.delete(record)


    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Emolument.__tablename__))


#######################################
###  EMOLUMENT AFFAIRE REPARTITION  ###
#######################################

@view_config(route_name='emolument_affaire_repartiton', request_method='GET', renderer='json')
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

    if len(records)>0:
        return Utils.serialize_many(records)
    else:
        return []


@view_config(route_name='emolument_affaire_repartiton', request_method='POST', renderer='json')
def emolument_affaire_repartiton_new_view(request):
    """
    Add new emolument_affaire_repartiton
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None
    emolument_facture_repartition = json.loads(request.params["emolument_facture_repartition"]) if "emolument_facture_repartition" in request.params else None

    # get records of current emolument_affaire_id
    emolumentAffaireRepartition = request.dbsession.query(EmolumentAffaireRepartition).filter(
        EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_id
    ).all()
    

    # iterate through emolument_facture_repartition
    for efr_i in emolument_facture_repartition:
        # test if efr_i exists already in db
        record = None
        for idx, eaf_i in enumerate(emolumentAffaireRepartition):
            if eaf_i.facture_id == efr_i['id']:
                # La relation existe déjà, la modifier
                record = emolumentAffaireRepartition.pop(idx)
                break
            
        if not record is None:
            if float(record.repartition) != float(efr_i['emolument_repartition']):
                if float(efr_i['emolument_repartition']) == 0:
                    # supprimer l'entrée car la répartition est nulle
                    request.dbsession.delete(record)
                else:
                    # enregistrer la nouvelle répartition
                    params = Utils._params(
                        facture_id = efr_i['id'],
                        emolument_affaire_id = emolument_affaire_id,
                        repartition = efr_i['emolument_repartition']
                    )
                    record = Utils.set_model_record(record, params)
        
        else:
            # Créer l'entrée inexistante et si la répartition est non nulle
            if float(efr_i['emolument_repartition']) > 0:
                record = EmolumentAffaireRepartition()
                params = Utils._params(
                    facture_id = efr_i['id'],
                    emolument_affaire_id = emolument_affaire_id,
                    repartition = efr_i['emolument_repartition']
                )
                record = Utils.set_model_record(record, params)

                request.dbsession.add(record)

    # remove items in db not posted
    for item in emolumentAffaireRepartition:
        request.dbsession.delete(item)            

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(EmolumentAffaireRepartition.__tablename__))


@view_config(route_name='emolument_affaire_repartiton', request_method='DELETE', renderer='json')
def emolument_affaire_repartiton_delete_view(request):
    """
    Delete emolument_affaire_repartiton by emolument_affaire_id
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_facture_edition']):
        raise exc.HTTPForbidden()

    emolument_affaire_id = request.params["emolument_affaire_id"] if "emolument_affaire_id" in request.params else None

    records = request.dbsession.query(EmolumentAffaireRepartition).filter(
        EmolumentAffaireRepartition.emolument_affaire_id == emolument_affaire_id
    ).all()

    for record in records:
        request.dbsession.delete(record)


@view_config(route_name='export_emoluments_pdf', request_method='POST')
def export_emoluments_pdf_view(request):
    """
    Create PDF of emoluments
    """
    # Check authorization
    if not check_connected(request):
        raise exc.HTTPForbidden()

    now = datetime.datetime.now()

    # get request params
    tableau_emoluments_id = request.params['tableau_emoluments_id'] if 'tableau_emoluments_id' in request.params else None
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    tableau_emoluments_html = request.params['tableau_emoluments_html'] if 'tableau_emoluments_html' in request.params else None
    tableau_recapitulatif_html = request.params['tableau_recapitulatif_html'] if 'tableau_recapitulatif_html' in request.params else None

    # get facture_id
    factures = request.dbsession.query(
        Facture
    ).join(
        EmolumentAffaireRepartition
    ).filter(
        EmolumentAffaireRepartition.emolument_affaire_id == tableau_emoluments_id
    ).all()

    d = {"now": now.strftime("%d.%m.%Y, %H:%M:%S")}

    header_str = "<html><head><style>"

    ppp = """
        .logo {{
            width: 3.68cm;
            image-resolution: 300dpi
        }}
        table {{
        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }}
        td, th {{
        border: 1px solid #ddd;
        padding: 2px;
        }}
        tr:nth-child(even){{background-color: #f2f2f2;}}
        th {{
        padding-top: 4px;
        padding-bottom: 4px;
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
                font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 9px;
                border-top: .25pt solid #666;
                width: 75%;
            }}
            @bottom-right {{
                content: "SERVICE DE LA GEOMATIQUE ET DU REGISTRE FONCIER";
                font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 9px;
            }}
        }}
        h1 {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 20px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 20px; }}
        p {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 11px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 15px; }}
        th {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 11px; font-style: normal; font-variant: normal; font-weight: bold; line-height: 15px; border-color: black; border-style: solid; border-width: 1px; }}
        td {{ font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif; font-size: 11px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 15px; border-color: black; border-style: solid; border-width: 1px; }}
        
        .nbInput {{ width: 50px; text-align: center; }}
        .nbField {{ margin: 0px; margin-bottom: 2px; min-height: 15px !important; padding: 3px 0px 0px 0px !important; }}
        .subtitle {{ background-color: lightgray; }}
        .alignRight {{ text-align: right !important; }}
        .alignCenter {{ text-align: center !important; }}
        .notEditable {{ background-color: lightgray; }}
        .montantTotal {{ font-weight: bold; }}
        .tabulation {{ padding-left: 15px !important; font-style: italic; }}
        .tabulation-2 {{ padding-left: 30px !important; font-style: italic; }}
        .batiment-separator {{ border-left: 3px solid black !important; }}
        .code {{ max-width: 50px !important; }}
        .position {{ max-width: 250px !important; }}
        .position_divers {{ max-width: 250px !important; }}
        .position_recapitulatif {{ max-width: 400px !important; }}
        .unite {{ max-width: 100px !important; }}
        .prix_unitaire {{ max-width: 120px !important; }}
        .nombre {{ max-width: 70px !important; }}
        .montant {{ max-width: 80px; }}
        .overHead {{ line-break: normal !important; font-weight: normal !important; font-style: italic; text-align: left; border-top: 0px !important; border-left: 0px !important; border-right: 0px !important; padding-bottom: 10px !important; }}
        .rowChapterDistinction {{ border-top: 3px solid; }}
        """ 

    header_str += ppp.format(**d)
    header_str += "</style></head><body>"
    header_str += "<img class='logo' src='https://sitn.ne.ch/web/images/06ne.ch_RVB.png' alt='Logo'>"
    header_str += '<p style="font-size: 10px; line-height: 12px; margin-top: 0px; padding-top: 4px; margin-left: 0px; padding-left: 0px;"><b>DÉPARTEMENT DU DÉVELOPPEMENT<br> \
                    TERRITORIAL ET DE L\'ENVIRONNEMENT</b><br> \
                    SERVICE DE LA GÉOMATIQUE ET<br> \
                    DU REGISTRE FONCIER</p>'

    header_str += "<h1>Tableau des émoluments de la mensuration officielle</h1>"
    header_str += "<p>Affaire N° " + str(affaire_id) + "</p>"
    header_str += "<p>Facture(s) N° " + ", ".join([(str(facture.sap) if facture.sap is not None else "N° SAP inconnu") + " (" + datetime.datetime.strftime(facture.date, "%d.%m.%Y") + ")" for facture in factures]) + "</p>"
    header_str += "<p>Emolument N° " + str(tableau_emoluments_id) + "</p>"


    tableau_emoluments_html = header_str + tableau_emoluments_html
    tableau_emoluments_html += '<br><p style="font-size:20px;"><b>Récapitulatif</b></p>'
    tableau_emoluments_html += tableau_recapitulatif_html + "</body></html>"

    filename = "Tableau_émoluments_" + str(tableau_emoluments_id) + "_Affaire_" + str(affaire_id) + ".pdf"

    result = requests.post("https://sitnintra.ne.ch/weasy/pdf?filename=" + filename, data=tableau_emoluments_html)

    response = Response(result.content)
    params = response.content_type_params
    params['filename'] = filename
    response.content_type = 'application/pdf'
    response.content_type_params = params
    return response
