from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction
from ..exceptions.custom_error import CustomError
from .. import models
import os
import shutil

########################################################
# Documents
########################################################

""" Return all documents types """
@view_config(route_name='types_documents', request_method='GET', renderer='json')
@view_config(route_name='types_documents_s', request_method='GET', renderer='json')
def types_documents_view(request):
    query = request.dbsession.query(models.DocumentType).all()
    return Utils.serialize_many(query)

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