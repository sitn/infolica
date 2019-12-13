from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)

from pyramid.security import remember, forget
from pyramid.response import Response
import json

class Utils():

    """ Serialize one query item"""
    @classmethod
    def serialize_one(cls, _query):
        d = _query.__dict__
        item = {}
        for n in d.keys():
            if n != '_sa_instance_state':
                item[n] = d[n]

        return item

    """ Serialize many query items"""
    @classmethod
    def serialize_many(cls, _query):
        master = []
        item = {}
        x = 0
        for u in _query:
            d = u.__dict__
            item = {}
            for n in d.keys():
                if n != '_sa_instance_state':
                    item[n] = d[n]
            master.append(item)
        return master
