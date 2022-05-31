# -*- coding: utf-8 -*--
from math import ceil
from infolica.scripts.mailer import send_mail
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Affaire, AffaireEtape, PreavisDecision, VAffaire, Operateur, Service
from infolica.models.models import PreavisRemarque
from infolica.models.models import Preavis, PreavisType, VAffairesPreavis
from infolica.scripts.utils import Utils
from infolica.scripts.mail_templates import MailTemplates
from infolica.scripts.authentication import check_connected

from datetime import datetime
import time
import os
import shutil

from sqlalchemy import func, cast, Text, or_

###########################################################
# PREAVIS AFFAIRE
###########################################################


@view_config(route_name='preavis_type', request_method='GET', renderer='json')
@view_config(route_name='preavis_type_s', request_method='GET', renderer='json')
def preavis_type_view(request):
    """
    GET preavis type
    """
    records = request.dbsession.query(PreavisType).all()
    return Utils.serialize_many(records)


@view_config(route_name='affaire_preavis_by_affaire_id', request_method='GET', renderer='json')
def affaire_preavis_view(request):
    """
    GET preavis affaire
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    records = request.dbsession.query(VAffairesPreavis).filter(
        VAffairesPreavis.affaire_id == affaire_id
    ).all()

    preavis = Utils.serialize_many(records)

    for p in preavis:
        p['unread_remarks'] = Utils.check_unread_preavis_remarks(request, affaire_id, service_id=p['service_id'])
    
    return preavis


@view_config(route_name='preavis', request_method='POST', renderer='json')
@view_config(route_name='preavis_s', request_method='POST', renderer='json')
def preavis_new_view(request):
    """
    POST preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    model = Preavis()
    model = Utils.set_model_record(model, request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Preavis.__tablename__))


@view_config(route_name='preavis', request_method='PUT', renderer='json')
@view_config(route_name='preavis_s', request_method='PUT', renderer='json')
def preavis_update_view(request):
    """
    UPDATE preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    preavis_id = request.params['id'] if 'id' in request.params else None
    logstep = request.params['logstep'] == 'true' if 'logstep' in request.params else False

    preavis = request.dbsession.query(Preavis).filter(
        Preavis.id == preavis_id).first()

    if not preavis:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Preavis.__tablename__, preavis_id))

    preavis = Utils.set_model_record(preavis, request.params)

    if logstep is True:
        service = request.dbsession.query(Service).filter(Service.id == preavis.service_id).first().abreviation
        params = {
            'affaire_id': preavis.affaire_id,
            'operateur_id': preavis.operateur_service_id,
            'etape_id': request.registry.settings['affaire_etape_preavis_id'],
            'remarque': service + ' - Demande ',
            'datetime': datetime.now(),
        }
        Utils.addNewRecord(request, AffaireEtape, params=params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Preavis.__tablename__))


@view_config(route_name='preavis', request_method='DELETE', renderer='json')
@view_config(route_name='preavis_s', request_method='DELETE', renderer='json')
def preavis_delete_view(request):
    """
    DELETE preavis affaire
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_preavis_edition']):
        raise exc.HTTPForbidden()

    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None

    record = request.dbsession.query(Preavis).filter(
        Preavis.id == preavis_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(Preavis.__tablename__, preavis_id))

    request.dbsession.delete(record)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Preavis.__tablename__))



# ====================================================================
#    ROUTES POUR LES SERVICES EXTERNES
# ====================================================================

def strongAuthentication(request, preavis_id):
    # Check connected
    if check_connected(request, [request.registry.settings['service_mo'].replace(' ', '')]):
        operateur = Utils.getOperateurFromUser(request)
        return operateur
    
    if not check_connected(request, request.registry.settings['preavis_services_externes'].replace(' ', '').split(',')):
        raise exc.HTTPForbidden()

    # get service from user
    operateur = Utils.getOperateurFromUser(request)
    if operateur.service_id is None:
         exc.HTTPForbidden(detail="Opérateur non autorisé à accéder à ce contenu")
    
    if preavis_id is None:
        exc.HTTPInternalServerError(detail="L'identidifiant du préavis est manquant")

    testPreavis = request.dbsession.query(Preavis).filter(
        Preavis.service_id == operateur.service_id
    ).first()

    if testPreavis is None:
        exc.HTTPForbidden(detail="Aucune demande de préavis pour ce service")

    return operateur



@view_config(route_name='service_externe_preavis', request_method='GET', renderer='json')
def service_externe_preavis_view(request):
    """
    GET preavis for service externe
    """
    # Check connected
    if not check_connected(request, request.registry.settings['preavis_services_externes'].replace(' ', '').split(',')):
        raise exc.HTTPForbidden()

    # get service from user
    operateur = Utils.getOperateurFromUser(request)

    if operateur.service_id is None:
        exc.HTTPForbidden(detail="Opérateur non autorisé à accéder à ce contenu")

    status = request.params['status'] if 'status' in request.params else None
    search = request.params['search'] if 'search' in request.params else None

    query = request.dbsession.query(
        Preavis.id,
        Preavis.date_demande,
        Preavis.date_reponse,
        Preavis.affaire_id,
        VAffaire.cadastre,
        VAffaire.nom,
        Operateur.prenom,
        Operateur.nom
    ).join(
        VAffaire, Preavis.affaire_id == VAffaire.id
    ).join(
        Operateur, Preavis.operateur_service_id == Operateur.id, isouter=True
    ).filter(
        Preavis.service_id == operateur.service_id
    )

    if status is not None:
        if status == "open":
            query = query.filter(
                Preavis.date_reponse == None,
                Preavis.etape == 'externe'
            )
        elif status == "closed":
            query = query.filter(Preavis.etape == 'interne')
    
    if search is not None:
        search = search.split(' ')
        for s in search:
            query = query.filter(
                or_(
                    cast(VAffaire.id, Text).ilike("%" + s + "%"),
                    VAffaire.nom.ilike("%" + s + "%"),
                    VAffaire.cadastre.ilike("%" + s + "%")
                )
            )

    records = query.order_by(Preavis.date_demande.desc()).all()

    results = []
    for rec in records:
        results.append({
            'preavis_id': rec[0],
            'preavis_date_demande': datetime.strftime(rec[1], "%d.%m.%Y"),
            'preavis_date_demande_int': time.mktime(rec[1].timetuple()),
            'preavis_date_reponse': datetime.strftime(rec[2], "%d.%m.%Y") if rec[2] is not None else None,
            'preavis_date_reponse_int': time.mktime(rec[2].timetuple()) if rec[2] is not None else None,
            'preavis_affaire_id': rec[3],
            'affaire_cadastre': rec[4],
            'affaire_description': rec[5],
            'preavis_attribution': ' '.join(filter(None, [rec[6], rec[7]])),
            'unread_remarks': Utils.check_unread_preavis_remarks(request, rec[3], service_id=operateur.service_id),
        })

    return results

@view_config(route_name='service_externe_affaire', request_method='GET', renderer='json')
def service_externe_affaire_view(request):
    """
    GET affaire for service externe
    """
    # affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    strongAuthentication(request, preavis_id)

    record = request.dbsession.query(
        VAffaire.id,
        VAffaire.nom,
        VAffaire.client_commande_type_id,
        VAffaire.client_commande_entreprise,
        VAffaire.client_commande_titre,
        VAffaire.client_commande_nom,
        VAffaire.client_commande_prenom,
        VAffaire.client_commande_complement,
        VAffaire.client_commande_adresse,
        VAffaire.client_commande_co,
        VAffaire.client_commande_npa,
        VAffaire.client_commande_localite,
        VAffaire.client_commande_tel_fixe,
        VAffaire.client_commande_tel_portable,
        VAffaire.client_commande_mail,
        VAffaire.type_affaire,
        VAffaire.cadastre,
        VAffaire.date_ouverture,
        VAffaire.localisation_e,
        VAffaire.localisation_n,
        Preavis.id,
        Preavis.date_demande,
        Preavis.date_reponse,
        Preavis.etape,
    ).filter(
        Preavis.id == preavis_id,
        VAffaire.id == Preavis.affaire_id,
    ).first()

    client = "\n".join(filter(None, [
        record[3],
        record[7],
        " ".join(filter(None, [record[4], record[6],  record[5]])),
        record[8],
        " ".join(filter(None, [record[10], record[11]])),
        record[12],
        record[13],
        record[14]
    ]))

    result = {
        'id': record[0],
        'nom': record[1],
        'client': client,
        'type_affaire': record[15],
        'cadastre': record[16],
        'date_ouverture': datetime.strftime(record[17], "%d.%m.%Y"),
        'coord_e': record[18],
        'coord_n': record[19],
        'preavis_id': record[20],
        'preavis_date_demande': datetime.strftime(record[21], "%d.%m.%Y"),
        'preavis_date_reponse': datetime.strftime(record[22], "%d.%m.%Y") if record[22] is not None else None,
        'preavis_etape': record[23]
    }

    return result


@view_config(route_name='service_externe_documents', request_method='GET', renderer='json')
def service_externe_documents_view(request):
    """
    GET documents of preavis_id for service externe
    """ 
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    operateur = strongAuthentication(request, affaire_id)

    affaire_chemin = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin

    # get rel path of service
    service_relpath = request.dbsession.query(Service).filter(Service.id == operateur.service_id).first().relpath
    courriers_courriels_rel_path = request.registry.settings['courriers_courriels_rel_path']
    documents = []
    for rel_path in [service_relpath, courriers_courriels_rel_path]:
        
        affaire_rel_path = os.path.join(affaire_chemin, rel_path)

        affaire_path = os.path.join(request.registry.settings['affaires_directory'], affaire_rel_path)

        if not os.path.exists(affaire_path):
            break


        for root, _, files in os.walk(affaire_path, topdown=False):
            for name in files:
                if name.startswith(".") or name.startswith("~"):
                    continue
                file_i = {}
                file_i['filename'] = name
                file_i['rel_path'] = rel_path
                file_i['size'] = str(ceil(os.path.getsize(os.path.join(root, name))/1000)) + ' ko' # ko
                file_i['creation_sort'] = os.path.getctime(os.path.join(root, name))
                file_i['modification_sort'] = os.path.getmtime(os.path.join(root, name))
                file_i['creation'] = datetime.fromtimestamp(file_i['creation_sort']).strftime("%d.%m.%Y")
                file_i['modification'] = datetime.fromtimestamp(file_i['modification_sort']).strftime("%d.%m.%Y")
                documents.append(file_i)
    
    return documents


@view_config(route_name='service_externe_conversation', request_method='GET', renderer='json')
def service_externe_conversation_view(request):
    """
    GET conversation of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    strongAuthentication(request, preavis_id)
    
    results = []

    query = request.dbsession.query(
        Operateur.id,
        Operateur.nom,
        Operateur.prenom,
        PreavisRemarque.date,
        PreavisRemarque.remarque,
        PreavisRemarque.lu_operateur_id,
        PreavisRemarque.id,
    ).join(
        Operateur, PreavisRemarque.operateur_id == Operateur.id
    ).join(
        Preavis, PreavisRemarque.preavis_id == Preavis.id
    ).filter(
        Preavis.id == preavis_id
    ).order_by(PreavisRemarque.id.desc()).all()


    connectedUser = Utils.getOperateurFromUser(request)
    pr_remark_user_query = request.dbsession.query(Operateur)

    for res in query:
        pr_remark_user = pr_remark_user_query.filter(Operateur.id == res[0]).first()
        unread = (res[5] is None) and (not connectedUser.service_id == pr_remark_user.service_id)

        results.append({
            "operateur": ' '.join([res[2], res[1]]),
            "date": datetime.strftime(res[3], "%d.%m.%Y"),
            "message": res[4],
            "unread": unread,
            "preavis_remarque_id": res[6]
        })

    return results


@view_config(route_name='service_externe_conversation', request_method='POST', renderer='json')
def service_externe_conversation_new_view(request):
    """
    POST conversation of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    commentaire = request.params['commentaire'] if 'commentaire' in request.params else None
    operateur = strongAuthentication(request, preavis_id)
    
    preavis = request.dbsession.query(Preavis).filter(
        Preavis.id == preavis_id
    ).first()

    rp = PreavisRemarque()
    
    params = {
        'preavis_id': preavis.id,
        'remarque': commentaire,
        'operateur_id': operateur.id,
        'date': datetime.strftime(datetime.now(), "%Y-%m-%d")
    }

    model = Utils.set_model_record(rp, params)
    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(PreavisRemarque.__tablename__))


@view_config(route_name='service_externe_conversation', request_method='PUT', renderer='json')
def service_externe_conversation_update_view(request):
    """
    PUT conversation of preavis_id for service externe
    """
    preavis_remarque_id = request.params['preavis_remarque_id'] if 'preavis_remarque_id' in request.params else None
    lu_operateur_id = request.params['lu_operateur_id'] if 'lu_operateur_id' in request.params else None
    preavis_remarque = request.dbsession.query(PreavisRemarque).filter(PreavisRemarque.id == preavis_remarque_id).first()

    preavis_remarque.lu_operateur_id = lu_operateur_id

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(PreavisRemarque.__tablename__))


@view_config(route_name='service_externe_liste_decisions', request_method='GET', renderer='json')
def service_externe_liste_decision_view(request):
    """
    GET list of decisions of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    strongAuthentication(request, preavis_id)
    
    result = request.dbsession.query(
        PreavisDecision.id,
        PreavisDecision.date,
        PreavisDecision.version,
        PreavisDecision.remarque,
        PreavisType.nom,
        Operateur.prenom,
        Operateur.nom,
        PreavisDecision.preavis_type_id
    ).join(
        PreavisType, PreavisType.id == PreavisDecision.preavis_type_id
    ).join(
        Operateur, Operateur.id == PreavisDecision.operateur_service_id
    ).filter(
        PreavisDecision.preavis_id == preavis_id,
        PreavisDecision.definitif == True
    ).order_by(PreavisDecision.id.asc()).all()

    liste_decisions = []
    for res in result:
        liste_decisions.append(
            {   
                'preavisDecision_id': res[0],
                'date': datetime.strftime(res[1], "%d.%m.%Y"),
                'version': res[2],
                'remarque': res[3],
                'decision': res[4],
                'operateur': ' '.join([res[5], res[6]]),
                'preavis_type_id': res[7]
            }
        )

    return liste_decisions


@view_config(route_name='service_externe_decision', request_method='GET', renderer='json')
def service_externe_decision_view(request):
    """
    GET decision of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None

    strongAuthentication(request, preavis_id)
    
    res = request.dbsession.query(
        PreavisDecision.preavis_type_id,
        PreavisDecision.remarque,
        PreavisDecision.date,
        Operateur.prenom,
        Operateur.nom,
        PreavisDecision.id,
        PreavisDecision.version,
    ).join(
        Operateur, Operateur.id == PreavisDecision.operateur_service_id
    ).filter(
        PreavisDecision.preavis_id == preavis_id,
        PreavisDecision.definitif.isnot(True)
    ).first()

    if res is not None:
        result = { 
            'preavis_type_id': res[0],
            'remarque': res[1],
            'date': datetime.strftime(res[2], "%d.%m.%Y"),
            "operateur": ' '.join([res[3], res[4]]),
            "definitif": False,
            "id": res[5],
            "version": res[6],
        }
    else:
       result = None

    return result


@view_config(route_name='service_externe_decision', request_method='POST', renderer='json')
def service_externe_decision_new_view(request):
    """
    POST decision of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    preavis_type_id = request.params['preavis_type_id'] if 'preavis_type_id' in request.params else None
    remarque = request.params['remarque'] if 'remarque' in request.params else None
    definitif = request.params['definitif'] == 'true' if 'definitif' in request.params else False
    operateur = strongAuthentication(request, preavis_id)
    
    rp = PreavisDecision()
    max_version = request.dbsession.query(func.max(PreavisDecision.version)).filter(PreavisDecision.preavis_id == preavis_id).scalar()
    max_version = 0 if max_version is None else max_version
    
    params = {
        'preavis_id': preavis_id,
        'preavis_type_id': preavis_type_id,
        'operateur_service_id': operateur.id,
        'remarque': remarque,
        'date': datetime.strftime(datetime.now(), "%Y-%m-%d"),
        'version': max_version + 1,
        'definitif': definitif
    }

    model = Utils.set_model_record(rp, params)

    preavis = request.dbsession.query(Preavis).filter(Preavis.id == preavis_id).first()
    preavis.operateur_service_id = operateur.id

    request.dbsession.add(model)

    # send mail to SGRF project managers
    if definitif is True:
        # update preavis etape and other infos
        preavis.etape = 'interne'
        preavis.date_reponse = datetime.strftime(datetime.now(), "%Y-%m-%d")
        preavis.preavis_type_id = preavis_type_id
        preavis.remarque = remarque

        MailTemplates.sendMailPreavisReponse(request, preavis_id)
        
        # log step
        service = request.dbsession.query(Service).filter(Service.id == preavis.service_id).first().abreviation
        params = {
            'affaire_id': preavis.affaire_id,
            'operateur_id': preavis.operateur_service_id,
            'etape_id': request.registry.settings['affaire_etape_preavis_id'],
            'remarque': service + ' - Retour ',
            'datetime': datetime.now(),
        }
        Utils.addNewRecord(request, AffaireEtape, params=params)


    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(PreavisDecision.__tablename__))


@view_config(route_name='service_externe_decision', request_method='PUT', renderer='json')
def service_externe_decision_update_view(request):
    """
    PUT decision of preavis_id for service externe
    """
    preavis_decision_id = request.params['preavis_decision_id'] if 'preavis_decision_id' in request.params else None
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    preavis_type_id = request.params['preavis_type_id'] if 'preavis_type_id' in request.params else None
    remarque = request.params['remarque'] if 'remarque' in request.params else None
    definitif = request.params['definitif'] == 'true' if 'definitif' in request.params else False
    operateur = strongAuthentication(request, preavis_id)
    
    result = request.dbsession.query(PreavisDecision).filter(PreavisDecision.id == preavis_decision_id).first()
    
    result.preavis_type_id = preavis_type_id
    result.operateur_id = operateur.id
    result.remarque = remarque
    result.date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    result.definitif = definitif

    preavis = request.dbsession.query(Preavis).filter(Preavis.id == preavis_id).first()
    preavis.operateur_service_id = operateur.id

    if definitif is True:
        # update preavis etape and other infos
        preavis.etape = 'interne'
        preavis.date_reponse = datetime.strftime(datetime.now(), "%Y-%m-%d")
        preavis.preavis_type_id = preavis_type_id
        preavis.remarque = remarque

        # send mail to SGRF project managers
        MailTemplates.sendMailPreavisReponse(request, preavis_id)
        
        # log step
        service = request.dbsession.query(Service).filter(Service.id == preavis.service_id).first().abreviation
        params = {
            'affaire_id': preavis.affaire_id,
            'operateur_id': preavis.operateur_service_id,
            'etape_id': request.registry.settings['affaire_etape_preavis_id'],
            'remarque': service + ' - Retour ',
            'datetime': datetime.now(),
        }
        Utils.addNewRecord(request, AffaireEtape, params=params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(PreavisDecision.__tablename__))


@view_config(route_name='service_externe_preavis_attribution', request_method='POST', renderer='json')
def service_externe_preavis_attribution_update_view(request):
    """
    POST attribution of preavis_id for service externe
    """
    preavis_id = request.params['preavis_id'] if 'preavis_id' in request.params else None
    operateur = strongAuthentication(request, preavis_id)
    
    preavis = request.dbsession.query(Preavis).filter(Preavis.id == preavis_id).first()

    preavis.operateur_service_id = operateur.id

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Preavis.__tablename__))


@view_config(route_name='service_externe_save_documents', request_method='POST', renderer='json')
def service_externe_save_documents_new_view(request):
    """
    POST preavis documents in affaire_id for service externe
    """
    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    operateur = strongAuthentication(request, affaire_id)
    
    service = request.dbsession.query(Service).filter(
        Service.id == operateur.service_id
    ).first()

    output_path = os.path.join(
        request.registry.settings['affaires_directory'],
        affaire_id,
        service.relpath
    )

    file_i = 0
    while 'files[' + str(file_i) + ']' in request.params:
        file = request.params['files[' + str(file_i) + ']']

        filename = file.filename
        input_file = file.file

        file_path = os.path.join(output_path, filename)
        file_path_tentative = file_path
        if os.path.exists(file_path_tentative):
            c = 1
            file_path_tentative = file_path.rsplit('.', 1)[0] + '_' + str(c) + '.' + file_path.rsplit('.', 1)[1]
            while os.path.exists(file_path_tentative):
                c += 1
                file_path_tentative = file_path.rsplit('.', 1)[0] + '_' + str(c) + '.' + file_path.rsplit('.', 1)[1]

        file_path = file_path_tentative
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # increment file_i
        file_i += 1

    return exc.HTTPOk(detail="Les fichiers ont bien été enregistrés")
