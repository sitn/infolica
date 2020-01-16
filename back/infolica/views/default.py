from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from .. import models
from sqlalchemy import exc
from ..exceptions.custom_error import CustomError
from pyramid.httpexceptions import HTTPForbidden
from ..scripts.utils import Utils
import logging
log = logging.getLogger(__name__)

"""
@view_config(route_name='home', renderer='../templates/mytemplate.mako')
def my_view(request):
    try:
        query = request.dbsession.query(models.Affaire)
        one = query.filter(models.Affaire.id != 0).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'infolica'}
"""

########################################################
# Test (temp endpoint)
########################################################
@view_config(route_name='test', request_method='POST', renderer='json')
def test_error(exc, request):
    query = request.dbsession.query(models.Client).first()
    query = Utils.set_model_record(query, request.params)
    return Utils.serialize_one(query)

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


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
