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
    #Controle_mutation
    config.add_route('controles_mutations','/infolica/api/controles_mutations')
    config.add_route('controles_mutations_s','/infolica/api/controles_mutations/')
    config.add_route('controle_mutation_by_id', '/infolica/api/controles_mutations/{id}')
    #Controle_PPE
    config.add_route('controles_ppe','/infolica/api/controles_ppe')
    config.add_route('controles_ppe_s','/infolica/api/controles_ppe/')
    config.add_route('controle_ppe_by_id', '/infolica/api/controles_ppe/{id}')
    #Suivi_Mandat
    config.add_route('suivis_mandats','/infolica/api/suivis_mandats')
    config.add_route('suivis_mandats_s','/infolica/api/suivis_mandats/')
    config.add_route('suivi_mandat_by_id', '/infolica/api/suivi_mandat/{id}')

