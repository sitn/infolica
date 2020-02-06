from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy import func, and_
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import os
from datetime import datetime

import logging
log = logging.getLogger(__name__)


###########################################################
# DOCUMENTS (LISTE) AFFAIRE
###########################################################

""" GET documents affaire"""
@view_config(route_name='affaire_documents_by_affaire_id', request_method='GET', renderer='json')
def affaire_documents_view(request):
    affaire_id = request.matchdict['id']

    doc_path = os.path.join(Constant.AFFAIRE_DIRECTORY, affaire_id)
    documents = list()
    for root, dirs, files in os.walk(doc_path):
        for file_i in files:
            file_path = os.path.join(root, file_i)
            documents.append(Utils._params(nom=file_i, dossier=os.path.relpath(root, doc_path), chemin=file_path,
                                           creation=datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d.%m.%Y")))
    return documents
