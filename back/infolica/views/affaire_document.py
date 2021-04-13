# -*- coding: utf-8 -*--
from pyramid.view import view_config
from pyramid.response import FileResponse
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.scripts.utils import Utils
from infolica.models.models import Affaire

import os
import shutil
import subprocess
from datetime import datetime


###########################################################
# DOCUMENTS (LISTE) AFFAIRE
###########################################################

@view_config(route_name='affaire_dossier_by_affaire_id', request_method='GET', renderer='json')
def affaire_dossier_view(request):
    """
    GET documents folder
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_dossier = request.registry.settings["affaires_directory_full_path"]
    affaire_id = request.matchdict['id']
    affaire_chemin = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin

    chemin = "Unknown path"
    if affaire_chemin:
        chemin = os.path.normcase(os.path.join(affaire_dossier, affaire_chemin))

    return chemin


@view_config(route_name='affaire_documents_by_affaire_id', request_method='GET', renderer='json')
def affaire_documents_view(request):
    """
    GET documents affaire
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']
    affaire_chemin = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin

    documents = []
    if not affaire_chemin:
        return documents


    affaire_path = os.path.join(request.registry.settings['affaires_directory'], affaire_chemin).replace('\\', '/')
    for root, dirs, files in os.walk(affaire_path, topdown=False):
        for name in files:
            if name.startswith(".") or name.startswith("~"):
                continue
            file_i = {}
            file_i['relpath'] = os.path.relpath(root, affaire_path).replace('\\', '/')
            file_i['filename'] = name
            file_i['creation'] = datetime.fromtimestamp(os.path.getctime(os.path.join(root, name))).strftime("%d.%m.%Y")
            file_i['modification'] = datetime.fromtimestamp(os.path.getmtime(os.path.join(root, name))).strftime("%d.%m.%Y")
            documents.append(file_i)

    return documents


@view_config(route_name='download_affaire_document', request_method='GET')
@view_config(route_name='download_affaire_document_s', request_method='GET')
def download_affaire_document_view(request):
    """
    Download document
    """
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaires_directory = request.registry.settings['affaires_directory']
    affaire_id = request.params['affaire_id']
    relpath = request.params['relpath']
    filename = request.params['filename']
    affaire_chemin = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin

    file_path = os.path.normcase(os.path.join(affaires_directory, affaire_chemin, relpath, filename))
    folder_path = os.path.exists(os.path.dirname(file_path))

    if not folder_path:
        Utils.create_affaire_folder(request, folder_path)

    import urllib
    response = FileResponse(file_path, request=request, cache_max_age=86400)
    headers = response.headers
    headers['Content-Type'] = 'application/download'
    headers['Accept-Ranges'] = 'bite'
    headers['Content-Disposition'] = 'attachment;filename=' + urllib.parse.quote(filename)
    return response


@view_config(route_name='open_folder', request_method='GET', renderer='json')
def save_document_view(request):
    """
    open folder (affaire)
    """
    basepath = request.registry.settings['affaires_directory_full_path']

    affaire_id = request.params['affaire_id'] if 'affaire_id' in request.params else None
    relpath = request.dbsession.query(Affaire).filter(Affaire.id == affaire_id).first().chemin
    
    path = os.path.join(basepath, relpath)

    if os.path.exists(path):
        subprocess.Popen('explorer ' + path)
    
    return
