def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    #Clients
    config.add_route('clients', '/infolica/api/clients')
    config.add_route('clients_s', '/infolica/api/clients/')
    config.add_route('client_by_id', '/infolica/api/clients/{id}')
    #Affaires
    config.add_route('affaires', '/infolica/api/affaires')
    config.add_route('affaires_s', '/infolica/api/affaires/')
    config.add_route('types_affaires', '/infolica/api/types_affaires')
    config.add_route('types_affaires_s', '/infolica/api/types_affaires/')
    config.add_route('affaire_by_id', '/infolica/api/affaires/{id}')
    #Login
    config.add_route('login', '/infolica/api/login')
    config.add_route('login_s', '/infolica/api/login/')
    config.add_route('logout', '/infolica/api/logout')
