from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from sqlalchemy import exc, func
from .. import models
from ..scripts.ldap_query import LDAPQuery
from ..models import Constant
import logging
log = logging.getLogger(__name__)


########################################################
# Login
########################################################
@view_config(route_name='login', request_method='POST', renderer='json')
@view_config(route_name='login_s', request_method='POST', renderer='json')
def login_view(request):
    response = None
    try:
        login = None
        password = None

        if 'login' in request.params:
            login = request.params['login']

        if 'password' in request.params:
            password = request.params['password']

        #Check if user exists in DB
        query = request.dbsession.query(models.Client)
        client = query.filter(func.lower(models.Client.login) == func.lower(login)).first()

        if not client:
            raise Exception(Constant.user_not_found_exception)

        response = LDAPQuery.do_login(request, login, password, client)

    except Exception as error:
        #log.error(str(error))
        request.response.status = 403
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response


########################################################
# Logout
########################################################
@view_config(route_name='logout', request_method='GET', renderer='json')
def logout_view(request):
    response = None
    try:
        response = LDAPQuery.do_logout(request)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response



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
