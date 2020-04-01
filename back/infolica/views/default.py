from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy.exc import DBAPIError
from .. import models
from sqlalchemy import exc
from ..exceptions.custom_error import CustomError
from pyramid.httpexceptions import HTTPForbidden
from ..scripts.utils import Utils
import logging
log = logging.getLogger(__name__)


########################################################
# Test (temp endpoint)
########################################################
@view_config(route_name='test', request_method='POST', renderer='json')
def test_error(exc, request):
    query = request.dbsession.query(models.Client).first()
    query = Utils.set_model_record(query, request.params)
    return Utils.serialize_one(query)


########################################################
# Common OPTION RESPONSE
########################################################
@view_config(route_name='login', request_method='OPTIONS', renderer='json')
@view_config(route_name='login_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='logout', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_clients', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_clients_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_affaires', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_affaires_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_numeros', request_method='OPTIONS', renderer='json')
@view_config(route_name='recherche_numeros_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='clients', request_method='OPTIONS', renderer='json')
@view_config(route_name='clients_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='operateurs', request_method='OPTIONS', renderer='json')
@view_config(route_name='operateurs_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='factures', request_method='OPTIONS', renderer='json')
@view_config(route_name='factures_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='numero_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='reference_numeros', request_method='OPTIONS', renderer='json')
@view_config(route_name='reference_numeros_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='preavis', request_method='OPTIONS', renderer='json')
@view_config(route_name='preavis_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='suivi_mandats', request_method='OPTIONS', renderer='json')
@view_config(route_name='suivi_mandats_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='controles_mutations', request_method='OPTIONS', renderer='json')
@view_config(route_name='controles_mutations_s', request_method='OPTIONS', renderer='json')
@view_config(route_name='controles_ppe', request_method='OPTIONS', renderer='json')
@view_config(route_name='controles_ppe_s', request_method='OPTIONS', renderer='json')
def options_response_view(request):
    return ''


########################################################
# Common IntegrityError return message
########################################################
@view_config(context=exc.IntegrityError, renderer='json')
def integrity_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common StatementError return message
########################################################
@view_config(context=exc.StatementError, renderer='json')
def statement_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common ResourceClosedError return message
########################################################
@view_config(context=exc.ResourceClosedError, renderer='json')
def resource_closed_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common InternalError return message
########################################################
@view_config(context=exc.InternalError, renderer='json')
def internal_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common NoReferenceError return message
########################################################
@view_config(context=exc.NoReferenceError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common InvalidRequestError, return message
########################################################
@view_config(context=exc.InvalidRequestError, renderer='json')
def invalidrequest_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common DBAPIError return message
########################################################
@view_config(context=exc.DBAPIError, renderer='json')
def dbaapi_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common SQLAlchemyError return message
########################################################
@view_config(context=exc.SQLAlchemyError, renderer='json')
def sqlalchemy_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.GENERAL_EXCEPTION}


########################################################
# Common HTTPForbidden return message
########################################################
@view_config(context=HTTPForbidden, renderer='json')
def http_forbidden_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 403
    return {'error': 'true', 'code': 403, 'message': CustomError.NOT_AUTHORIZED_EXCEPTION}
