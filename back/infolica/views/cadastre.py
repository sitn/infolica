# -*- coding: utf-8 -*--
from pyramid.view import view_config

from infolica.models.models import Cadastre
from infolica.scripts.utils import Utils

###########################################################
# Cadastre
###########################################################


@view_config(route_name='cadastres', request_method='GET', renderer='json')
@view_config(route_name='cadastres_s', request_method='GET', renderer='json')
def cadastre_view(request):
    """
    GET cadastre
    """
    # Check connected
    # if not Utils.check_connected(request):
    # raise exc.HTTPForbidden()

    records = request.dbsession.query(Cadastre).filter(Cadastre.id != request.registry.settings['cadastre_cantonal_id']).order_by(Cadastre.nom).all()

    return Utils.serialize_many(records)
