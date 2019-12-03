from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


""" Return all clients"""
@view_config(route_name='clients', renderer='json')
@view_config(route_name='clients_s', renderer='json')
def my_view(request):
    try:
        query = request.dbsession.query(models.Client).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return query




db_err_msg = ''
