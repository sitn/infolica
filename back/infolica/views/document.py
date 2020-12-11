# -*- coding: utf-8 -*--
from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Service
from infolica.scripts.utils import Utils

import os
import json
from datetime import datetime
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
    affaire_id = request.params['affaire_id']
    template = request.params['template']
    values = request.params['values']
    service_id = request.params['service_id'] if 'service_id' in request.params else None

    # Set output file name
    output_file_name=template
    relPath = ""
    if service_id:
        service = request.dbsession.query(Service).filter(Service.id == service_id).first()
        output_file_name = service.abreviation
        relPath = service.relpath

    date_time = datetime.now().strftime("%Y%m%d")
    filename = output_file_name + "_" + date_time + '.docx'
    file_path = os.path.normpath(os.path.join(affaires_directory, affaire_id, relPath, filename))

    # Set context
    context = json.loads(values)
    for key in context.keys():
        context[key] = RichText(context[key])

    # Ouverture du document template
    doc = DocxTemplate(os.path.join(mails_templates_directory, template + ".docx"))

    # Replace values by keywords and save
    doc.render(context)
    doc.save(file_path)

    return {'filename': filename}

