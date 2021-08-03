# -*- coding: utf-8 -*--
from pyramid.view import view_config

from infolica.models.models import Affaire, Service
from infolica.scripts.utils import Utils

import os
import json
from docxtpl import DocxTemplate, RichText


@view_config(route_name='save_document', request_method='POST', renderer='json')
def save_document_view(request):
    """
    Save file (preavis)
    """
    settings = request.registry.settings
    mails_templates_directory = settings['mails_templates_directory']
    affaires_directory = settings['affaires_directory']

    # Get request params
    affaire_id = str(request.params['affaire_id'])
    template = request.params['template']
    values = request.params['values']
    service_id = request.params['service_id'] if 'service_id' in request.params else None
    relPath = request.params['relpath'].strip('/').strip('\\') if 'relpath' in request.params else ""
    filename = request.params['filename'] if 'filename' in request.params else None

    # Set output file name
    output_file_name = filename if filename is not None else template
    if service_id:
        service = request.dbsession.query(Service).filter(Service.id == service_id).first()
        output_file_name += "_" + service.abreviation
        relPath = service.relpath.strip('/').strip('\\')

    affaire_relpath = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin
    
    if affaire_relpath is None:
        affaire_relpath = affaire_id
        
    affaire_path = os.path.normcase(os.path.join(affaires_directory, affaire_relpath))
    
    filename = output_file_name + '.docx'
    file_path = os.path.normcase(os.path.join(affaire_path, relPath, filename))

    if not os.path.exists(affaire_path):
        Utils.create_affaire_folder(request, affaire_path)
        # update affaire chemin
        affaire = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first()
        affaire.chemin = affaire_relpath

    # Set context
    context = json.loads(values)
    for key in context.keys():
        context[key] = RichText(context[key])

    # Ouverture du document template
    doc = DocxTemplate(os.path.join(mails_templates_directory, template + ".docx"))

    # Replace values by keywords and save
    doc.render(context)
    doc.save(file_path)

    return {'filename': filename, "folderpath": relPath}

