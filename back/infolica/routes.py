def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    #Clients
    config.add_route('types_clients', '/infolica/api/types_clients')
    config.add_route('types_clients_s', '/infolica/api/types_clients/')
    config.add_route('clients', '/infolica/api/clients')
    config.add_route('clients_s', '/infolica/api/clients/')
    config.add_route('client_by_id', '/infolica/api/clients/{id}')
    config.add_route('recherche_clients', '/infolica/api/recherche_clients')
    config.add_route('recherche_clients_s', '/infolica/api/recherche_clients/')
    #Affaires
    config.add_route('affaires', '/infolica/api/affaires')
    config.add_route('affaires_s', '/infolica/api/affaires/')
    config.add_route('types_affaires', '/infolica/api/types_affaires')
    config.add_route('types_affaires_s', '/infolica/api/types_affaires/')
    config.add_route('affaire_by_id', '/infolica/api/affaires/{id}')
    config.add_route('recherche_affaires', '/infolica/api/recherche_affaires')
    config.add_route('recherche_affaires_s', '/infolica/api/recherche_affaires/')
    #Factures
    config.add_route('factures', '/infolica/api/factures')
    config.add_route('factures_s', '/infolica/api/factures/')
    config.add_route('facture_by_id', '/infolica/api/factures/{id}')
    #Login
    config.add_route('login', '/infolica/api/login')
    config.add_route('login_s', '/infolica/api/login/')
    config.add_route('logout', '/infolica/api/logout')
    #Operateur
    config.add_route('operateurs', '/infolica/api/operateurs')
    config.add_route('operateurs_s', '/infolica/api/operateurs/')
    config.add_route('operateur_by_id', '/infolica/api/operateurs/{id}')
    #Test (temp endpoint)
    config.add_route('test', '/infolica/api/test')

