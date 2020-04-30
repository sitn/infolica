from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..models import Constant
from .. import models
from ..scripts.utils import Utils
import os
import shutil
from datetime import datetime


###########################################################
# DOCUMENTS (LISTE) AFFAIRE
###########################################################

""" GET documents affaire"""
@view_config(route_name='affaire_documents_by_affaire_id', request_method='GET', renderer='json')
def affaire_documents_view(request):
    # Check connected
    if not Utils.check_connected(request):
        raise exc.HTTPForbidden()

    affaire_id = request.matchdict['id']

    doc_path = os.path.join(Constant.AFFAIRE_DIRECTORY, affaire_id)
    documents = list()
    for root, dirs, files in os.walk(doc_path):
        for file_i in files:
            file_path = os.path.join(root, file_i)
            documents.append(Utils._params(nom=file_i, dossier=os.path.relpath(root, doc_path), chemin=file_path,
                                           creation=datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d.%m.%Y")))
    return documents


""" Return all documents types """
@view_config(route_name='types_documents', request_method='GET', renderer='json')
@view_config(route_name='types_documents_s', request_method='GET', renderer='json')
def types_documents_view(request):
    query = request.dbsession.query(models.DocumentType).all()
    return Utils.serialize_many(query)

"""Upload document"""
@view_config(route_name='upload_document', request_method='POST', renderer='json')
def upload_document_view(request):
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['affaire_edition']):
        raise exc.HTTPForbidden()

    # Get client instance
    model = Utils.set_model_record(models.Document(), request.params)

    with transaction.manager:
        request.dbsession.add(model)
        request.dbsession.flush()
        transaction.commit()

        # Create affaire folder if does not exist
        affaire_folder = request.registry.settings['upload_files_directory'] + '/' + request.params['affaire_id']
        Utils.create_affaire_folder(affaire_folder)

        filename = request.POST['affaire_doc_file'].filename
        input_file = request.POST['affaire_doc_file'].file
        file_path = os.path.join(affaire_folder, filename)
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)


        return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Document.__tablename__))
