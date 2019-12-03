def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    #Clients
    config.add_route('clients', '/infolica/api/clients')
    config.add_route('clients_s', '/infolica/api/clients/')
