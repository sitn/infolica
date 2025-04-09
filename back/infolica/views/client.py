from pyramid.view import view_config
import pyramid.httpexceptions as exc

from infolica.exceptions.custom_error import CustomError
from infolica.models import Constant
from infolica.models.models import Client, ClientType, ClientMoralPersonne
from infolica.scripts.utils import Utils
from infolica.scripts.authentication import check_connected
import json
from datetime import datetime
from sqlalchemy import cast, or_, Text, func
import re
from unidecode import unidecode


def _set_client_aggregated_name(client, sep=', '):
    nom_ = sep.join(filter(None, [
        client.entreprise,
        ' '.join(filter(None, [client.titre, client.prenom, client.nom])),
        client.co,
        client.adresse,
        ' '.join(filter(None, [client.npa, client.localite])),
        'SAP: ' + (client.no_sap if client.no_sap is not None else '-'),
        'BDP/BDEE: ' + (client.no_bdp_bdee if client.no_bdp_bdee is not None else '-')
    ]))

    if client.sortie is not None:
        nom_ = '(ancien client) ' + nom_

    return nom_


def _multipleAttributesClientSearch(request, searchTerm, old_clients=False, search_limit='default', filter_type=[]):
    if search_limit == 'default':
        search_limit = int(request.registry.settings['search_limit'])

    # Découpage du searchTerm en mots-clés
    searchTerms = re.split(r'\s|\,|\:|\-|SAP|BDP/BDEE', searchTerm.strip())
    searchTerms = [term.strip().lower() for term in searchTerms if term and term.lower() != "null"]

    # Base query avec filtres globaux
    query = request.dbsession.query(Client)

    if not old_clients:
        query = query.filter(Client.sortie == None)

    if filter_type:
        query = query.filter(Client.type_client.in_(filter_type))

    # Si pas de mots-clés, retourne simplement la base query ordonnée
    if searchTerms:

        # Sous-requêtes pour chaque mot-clé
        subqueries = []
        for term in searchTerms:
            # Crée l'expression de recherche pour chaque terme
            term_expr = unidecode(str(term).lower())


            # Ajoute la sous-requête en calculant la similarité pour chaque champ
            q = query.filter(
                or_(
                    func.unaccent(func.lower(Client.entreprise)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(Client.titre)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(Client.nom)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(Client.prenom)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(Client.co)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(Client.adresse)).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(cast(Client.no_sap, Text))).like(f"%{term_expr}%"),
                    func.unaccent(func.lower(cast(Client.no_bdp_bdee, Text))).like(f"%{term_expr}%")
                )
            )
            subqueries.append(q)

        # Union de toutes les sous-requêtes
        query = subqueries[0]
        for q in subqueries[1:]:
            query = query.intersect(q)

    # Limiter les résultats et obtenir les objets Client
    client_results = query.order_by(Client.entreprise, Client.nom, Client.prenom).limit(search_limit).all()

    return client_results


@view_config(route_name='types_clients', request_method='GET', renderer='json')
@view_config(route_name='types_clients_s', request_method='GET', renderer='json')
def types_clients_view(request):
    """
    Return all types clients
    """
    query = request.dbsession.query(ClientType).all()
    return Utils.serialize_many(query)


@view_config(route_name='clients', request_method='GET', renderer='json')
@view_config(route_name='clients_s', request_method='GET', renderer='json')
def clients_view(request):
    """
    Return all clients
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    client_id = request.params['id'] if 'id' in request.params else None

    query = request.dbsession.query(Client)

    if client_id:
        query = query.filter(Client.id == client_id)

    query = query.filter(Client.sortie == None).all()
    return Utils.serialize_many(query)


@view_config(route_name='client_by_id', request_method='GET', renderer='json')
def client_by_id_view(request):
    """
    Return client by id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    query = request.dbsession.query(Client).filter(
        Client.id == id).first()
    return Utils.serialize_one(query)


@view_config(route_name='search_client_aggregated_by_id', request_method='GET', renderer='json')
def client_aggregated_by_id_view(request):
    """
    Return client aggregated by id
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    id = request.matchdict['id']
    checkers = json.loads(request.params["checkers"]) if "checkers" in request.params else []

    result = request.dbsession.query(Client).filter(
        Client.id == id).first()

    remarque = []
    if "ask-facture-reference" in checkers and result.besoin_vref_facture is True:
        remarque.append("Le client demande une référence dans la facture.")
    if "ask-other-client-facture" in checkers and result.besoin_client_facture is True:
        remarque.append("Le client demande une adresse de facturation différente.")

    client = {
        'id': result.id,
        'nom': _set_client_aggregated_name(result),
        'type_client': result.type_client,
        'remarque': "\n".join(remarque),
    }

    return client


@view_config(route_name='recherche_clients', request_method='POST', renderer='json')
@view_config(route_name='recherche_clients_s', request_method='POST', renderer='json')
def clients_search_view(request):
    """
    Search clients
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    settings = request.registry.settings
    search_limit = int(settings['search_limit'])
    old_clients = request.params['old_clients'] == 'true' if 'old_clients' in request.params else False
    conditions = Utils.get_search_conditions(Client, request.params)

    # Check date_sortie is null
    conditions = [] if not conditions or len(
        conditions) == 0 else conditions

    # conditions.append(Client.sortie == None)

    query = request.dbsession.query(
        Client
    ).filter(
        *conditions
    )

    if not old_clients:
        query = query.filter(Client.sortie == None)

    query = query.order_by(Client.entreprise, Client.nom, Client.prenom).limit(search_limit).all()
    return Utils.serialize_many(query)


@view_config(route_name='search_clients_by_term', request_method='GET', renderer='json')
def clients_search_by_term_view(request):
    """
    Search clients by term
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    searchTerm = request.params["searchTerm"] if "searchTerm" in request.params else None
    old_clients = request.params['old_clients'] == 'true' if 'old_clients' in request.params else False

    clients = _multipleAttributesClientSearch(request, searchTerm, old_clients=old_clients)

    return Utils.serialize_many(clients)


@view_config(route_name='search_clients_aggregated_by_term', request_method='GET', renderer='json')
def clients_aggregated_search_by_term_view(request):
    """
    Search clients aggregated
    """
    # Check connected
    if not check_connected(request):
        raise exc.HTTPForbidden()

    searchTerm = request.params["searchTerm"] if "searchTerm" in request.params else None
    old_clients = request.params['old_clients'] == 'true' if 'old_clients' in request.params else False
    filter_type = json.loads(request.params['filter_type']) if 'filter_type' in request.params else []

    query = _multipleAttributesClientSearch(request, searchTerm, old_clients=old_clients, filter_type=filter_type)

    liste_clients = []
    for client in query:
        nom_ = _set_client_aggregated_name(client)
        type_client_nom = request.dbsession.query(ClientType).filter(ClientType.id==client.type_client).first()
        type_client_nom = type_client_nom.nom if type_client_nom else ""

        # if client.type_client not in liste_clients.keys():
        #     liste_clients[type_client_nom] = []

        # liste_clients[type_client_nom].append({
        #     'id': client.id,
        #     'nom': nom_,
        #     'type_client': client.type_client,
        #     # 'type_client_nom':type_client_nom
        # })

        liste_clients.append({
            'id': client.id,
            'nom': nom_,
            'type_client': client.type_client,
            'type_client_nom': type_client_nom,
            'active': True if client.sortie is None else False,
        })

    liste_clients.sort(key=lambda x: x["type_client"])

    return liste_clients


@view_config(route_name='clients', request_method='POST', renderer='json')
@view_config(route_name='clients_s', request_method='POST', renderer='json')
def clients_new_view(request):
    """
    Add new client
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    # Get client instance
    model = Utils.set_model_record(Client(), request.params)

    request.dbsession.add(model)
    request.dbsession.flush()

    return json.dumps({'client_id': model.id})


@view_config(route_name='clients', request_method='PUT', renderer='json')
@view_config(route_name='clients_s', request_method='PUT', renderer='json')
def clients_update_view(request):
    """
    Update client
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    # Get client_id
    id_client = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(Client).filter(
        Client.id == id_client).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            Client.__tablename__, id_client))

    # Read params client
    model = Utils.set_model_record(model, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Client.__tablename__))


# @view_config(route_name='clients', request_method='DELETE', renderer='json')
# @view_config(route_name='clients_s', request_method='DELETE', renderer='json')
# def clients_delete_view(request):
#     """
#     Delete client
#     """
#     # Check authorization
#     if not Utils.has_permission(request, request.registry.settings['client_edition']):
#         raise exc.HTTPForbidden()

#     # Get client_id
#     id_client = request.params['id'] if 'id' in request.params else None

#     model = request.dbsession.query(Client).filter(
#         Client.id == id_client).first()

#     # If result is empty
#     if not model:
#         raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
#             Client.__tablename__, id_client))

#     model.sortie = datetime.utcnow()

#     return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Client.__tablename__))


# ClientMoralPersonnes
@view_config(route_name='client_moral_personnes_by_client_id', request_method='GET', renderer='json')
def types_client_moral_personnes_by_client_id_view(request):
    """
    Return all people in client_moral
    """
    client_id = request.matchdict['client_id'] if 'client_id' in request.matchdict else None

    query = request.dbsession.query(ClientMoralPersonne).filter(ClientMoralPersonne.client_id == client_id).all()
    return Utils.serialize_many(query)


@view_config(route_name='client_moral_personnes', request_method='POST', renderer='json')
@view_config(route_name='client_moral_personnes_s', request_method='POST', renderer='json')
def clients_moral_personne_new_view(request):
    """
    Add new contact in entreprise
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    # Get clientMoralPersonne instance
    model = Utils.set_model_record(ClientMoralPersonne(), request.params)

    request.dbsession.add(model)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(ClientMoralPersonne.__tablename__))


@view_config(route_name='client_moral_personnes', request_method='PUT', renderer='json')
@view_config(route_name='client_moral_personnes_s', request_method='PUT', renderer='json')
def clients_moral_personne_update_view(request):
    """
    Update contact in entreprise
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    client_moral_personne_id = request.params["id"] if "id" in request.params else None

    model = request.dbsession.query(ClientMoralPersonne).filter(
        ClientMoralPersonne.id == client_moral_personne_id).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            ClientMoralPersonne.__tablename__, client_moral_personne_id))

    # Read params client
    model = Utils.set_model_record(model, request.params)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(ClientMoralPersonne.__tablename__))


@view_config(route_name='client_moral_personnes', request_method='DELETE', renderer='json')
@view_config(route_name='client_moral_personnes_s', request_method='DELETE', renderer='json')
def client_moral_personnes_delete_view(request):
    """
    Delete client_moral_personnes
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    # Get client_id
    client_moral_personne_id = request.params['id'] if 'id' in request.params else None

    model = request.dbsession.query(ClientMoralPersonne).filter(
        ClientMoralPersonne.id == client_moral_personne_id).first()

    # If result is empty
    if not model:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(
            ClientMoralPersonne.__tablename__, client_moral_personne_id))

    request.dbsession.delete(model)

    return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(Client.__tablename__))


@view_config(route_name='client_check_existing', request_method='GET', renderer='json')
def client_check_existing_view(request):
    """
    Check if client already exists
    """
    # Check authorization
    if not Utils.has_permission(request, request.registry.settings['client_edition']):
        raise exc.HTTPForbidden()

    entreprise = request.params['entreprise'] if 'entreprise' in request.params else None
    firstname = request.params['firstname'] if 'firstname' in request.params else None
    lastname = request.params['lastname'] if 'lastname' in request.params else None
    client_id = request.params['client_id'] if 'client_id' in request.params else None

    clients = request.dbsession.query(Client)

    if entreprise is not None:
        normalized_entreprise = cast(func.unaccent(func.lower(Client.entreprise)), Text)
        normalized_entreprise_search = unidecode(str(entreprise).lower())

        clients = clients.filter(
            normalized_entreprise.like(f"{normalized_entreprise_search}%"),
        )
    else:
        normalized_firstname = func.unaccent(func.lower(Client.prenom))
        normalized_lastname = func.unaccent(func.lower(Client.nom))
        normalized_firstname_search = unidecode(str(firstname).lower())
        normalized_lastname_search = unidecode(str(lastname).lower())

        clients = clients.filter(
            normalized_firstname.like(f"{normalized_firstname_search}%"),
            normalized_lastname.like(f"{normalized_lastname_search}%")
        )

    if client_id is not None:
        clients = clients.filter(Client.id != client_id)

    clients = clients.all()

    nom = []
    nom.append(entreprise) if entreprise is not None else ''
    nom.append(f'{lastname} {firstname}') if lastname is not None and firstname is not None else ''
    nom = ' - '.join(nom)
    response = {
        'error': len(clients) > 0,
        'message': f'{nom} semble déjà exister dans la base de données.' if len(clients) > 0 else '',
        'clients': Utils.serialize_many(clients)
    }

    return response
