from pyramid.view import view_config
import pyramid.httpexceptions as exc
from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils
# from distutils.dir_util import copy_tree
import os
import json
from weasyprint import HTML, default_url_fetcher
from pyramid.response import FileResponse
from datetime import datetime
from docxtpl import DocxTemplate, RichText


###########################################################
# AFFAIRE
###########################################################

""" 
Return all affaires
"""
@view_config(route_name='affaires', request_method='GET', renderer='json')
@view_config(route_name='affaires_s', request_method='GET', renderer='json')
def affaires_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    query = request.dbsession.query(models.VAffaire).all()
    return Utils.serialize_many(query)


""" 
Return affaires by id
"""
@view_config(route_name='affaire_by_id', request_method='GET', renderer='json')
def affaire_by_id_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    query = request.dbsession.query(models.VAffaire)
    one = query.filter(models.VAffaire.id == id).first()
    return Utils.serialize_one(one)


""" 
Search affaires
"""
@view_config(route_name='recherche_affaires', request_method='POST', renderer='json')
@view_config(route_name='recherche_affaires_s', request_method='POST', renderer='json')
def affaires_search_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])
    conditions = Utils.get_search_conditions(
        models.VAffaire, request.params)
    query = request.dbsession.query(models.VAffaire).filter(
        *conditions).order_by(models.VAffaire.date_ouverture.desc()).limit(search_limit).all()
    return Utils.serialize_many(query)


""" 
Return all types affaires
"""
@view_config(route_name='types_affaires', request_method='GET', renderer='json')
@view_config(route_name='types_affaires_s', request_method='GET', renderer='json')
def types_affaires_view(request):
    types_affaires = request.dbsession.query(models.AffaireType).all()

    types_affaires = Utils.serialize_many(types_affaires)
    return types_affaires

""" 
Return all types modification affaire
"""
@view_config(route_name='types_modification_affaire', request_method='GET', renderer='json')
@view_config(route_name='types_modification_affaire_s', request_method='GET', renderer='json')
def types_modification_affaire_view(request):
    records = request.dbsession.query(models.ModificationAffaireType).all()
    types_affaires = list()

    # Supprimer type d'affaire "NE PLUS UTILISER"
    for type_i in records:
        if not "NE PLUS UTILISER" in type_i.nom:
            types_affaires.append(type_i)

    types_affaires = Utils.serialize_many(types_affaires)
    return types_affaires


""" 
Add new affaire
"""
@view_config(route_name='affaires', request_method='POST', renderer='json')
@view_config(route_name='affaires_s', request_method='POST', renderer='json')
def affaires_new_view(request):
    # Get role depending on affaire type
    affaire_type = request.params['type_id'] if 'type_id' in request.params else None

    # Permission (fonction) par défaut
    permission = request.registry.settings['affaire_edition']

    # Affaire de cadastration
    if affaire_type == request.registry.settings['affaire_type_cadastration_id']:
        permission = request.registry.settings['affaire_cadastration_edition']
    # Affaire de PPE
    elif affaire_type == request.registry.settings['affaire_type_ppe_id']:
        permission = request.registry.settings['affaire_ppe_edition']
    # Affaire de révision d'abornement
    elif affaire_type == request.registry.settings['affaire_type_revision_abornement_id']:
        permission = request.registry.settings['affaire_revision_abornement_edition']

    # Check authorization
    if not Utils.has_permission(request, permission):
        raise exc.HTTPForbidden()

    model = models.Affaire()
    model = Utils.set_model_record(model, request.params)

    with transaction.manager:
        request.dbsession.add(model)
        # Récupèrer l'id de la nouvelle affaire
        request.dbsession.flush()

        # Créer le chemin du dossier de l'affaire
        model.chemin = os.path.join(request.registry.settings['affaires_directory'], str(model.id))

        # commit
        transaction.commit()

        # Copier le dossier __template pour une nouvelle affaire
        # copy_tree(request.registry.settings['affaireTemplateDir'], model.chemin)
        os.mkdir(model.chemin)
        return model.id



""" 
Update affaire
"""
@view_config(route_name='affaires', request_method='PUT', renderer='json')
@view_config(route_name='affaires_s', request_method='PUT', renderer='json')
def affaires_update_view(request):
    # id_affaire
    id_affaire = request.params['id_affaire'] if 'id_affaire' in request.params else None

    # Get the affaire
    record = request.dbsession.query(models.Affaire).filter(
        models.Affaire.id == id_affaire).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Affaire.__tablename__, id_affaire))

    # Get role depending on affaire type
    affaire_type = request.params['type_id'] if 'type_id' in request.params else record.type_id

    # Permission (fonction) par défaut
    permission = request.registry.settings['affaire_edition']

    # Affaire de cadastration
    if affaire_type == request.registry.settings['affaire_type_cadastration_id']:
        permission = request.registry.settings['affaire_cadastration_edition']
    # Affaire de PPE
    elif affaire_type == request.registry.settings['affaire_type_ppe_id']:
        permission = request.registry.settings['affaire_ppe_edition']
    # Affaire de révision d'abornement
    elif affaire_type == request.registry.settings['affaire_type_revision_abornement_id']:
        permission = request.registry.settings['affaire_revision_abornement_edition']

    # Check authorization
    if not Utils.has_permission(request, permission):
        raise exc.HTTPForbidden()

    record = Utils.set_model_record(record, request.params)

    with transaction.manager:
        # Commit transaction
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Affaire.__tablename__))


"""
Create  file 
"""
@view_config(route_name='courrier_affaire', request_method='POST', renderer='json')
@view_config(route_name='courrier_affaire_s', request_method='POST', renderer='json')
def courrier_affaire_view(request):
    settings = request.registry.settings
    mails_templates_directory = settings['mails_templates_directory']
    temporary_directory = settings['temporary_directory']
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = 'PCOP_' + date_time + '.docx'
    file_path = os.path.join(temporary_directory, filename)

    # Get request params
    # template = request.params['template']
    values = request.params['values']
    context = json.loads(values)
    context["ADRESSE_"] = RichText(context["ADRESSE_"])

    # Ouverture du document template
    doc = DocxTemplate(os.path.join(mails_templates_directory, "ParCop.docx"))

    # Replace values by keywords and save
    doc.render(context)
    doc.save(file_path)

    return {'filename': filename}


"""
Send file
"""
@view_config(route_name='courrier_affaire', request_method='GET')
@view_config(route_name='courrier_affaire_s', request_method='GET')
def download_courrier_affaire_view(request):
    settings = request.registry.settings
    filename = request.params['filename']
    temporary_directory = settings["temporary_directory"]
    file_path = os.path.join(temporary_directory, filename)

    if os.path.exists(file_path):
        response = FileResponse(file_path, request=request, cache_max_age=86400)
        headers = response.headers
        headers['Content-Type'] = 'application/download'
        headers['Accept-Ranges'] = 'bite'
        headers['Content-Disposition'] = 'attachment;filename=' + filename

        return response

    else:
        raise exc.HTTPNotFound("Le fichier est indisponible")


"""
Supprimer le fichier une fois téléchargé
"""
@view_config(route_name='courrier_affaire', request_method='DELETE', renderer='string')
@view_config(route_name='courrier_affaire_s', request_method='DELETE', renderer='string')
def delete_courrier_affaire_view(request):
    settings = request.registry.settings
    filename = request.params['filename']
    temporary_directory = settings["temporary_directory"]
    file_path = os.path.join(temporary_directory, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        response = True

        return "ok"

    else:
        raise exc.HTTPNotFound("Le fichier est indisponible")

"""
Modification affaire
"""
@view_config(route_name='modification_affaires', request_method='POST', renderer='json')
@view_config(route_name='modification_affaires_s', request_method='POST', renderer='json')
def modification_affaires_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_edition']):
        raise exc.HTTPForbidden()

    # Get client instance
    model = Utils.set_model_record(models.ModificationAffaire(), request.params)

    with transaction.manager:
        request.dbsession.add(model)
        transaction.commit()
        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.ModificationAffaire.__tablename__))


"""Get modification affaire by affaire_mère"""
@view_config(route_name="modification_affaire_by_affaire_mere", request_method="GET", renderer="json")
def modification_affaire_by_affaire_mere_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_mere_id = request.matchdict["id"]

    records = request.dbsession.query(models.ModificationAffaire).filter(models.ModificationAffaire.affaire_id_fille == affaire_mere_id).all()

    return Utils.serialize_many(records)


"""Get modification affaire by affaire_fille"""
@view_config(route_name="modification_affaire_by_affaire_fille", request_method="GET", renderer="json")
def modification_affaire_by_affaire_fille_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_fille_id = request.matchdict["id"]

    records = request.dbsession.query(models.ModificationAffaire).filter(models.ModificationAffaire.affaire_id_mere == affaire_fille_id).all()

    return Utils.serialize_many(records)
