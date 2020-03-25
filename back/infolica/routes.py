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
    config.add_route('affaires_factures_by_affaire_id', '/infolica/api/affaires_factures/{id}')
    #Login
    config.add_route('login', '/infolica/api/login')
    config.add_route('login_s', '/infolica/api/login/')
    config.add_route('logout', '/infolica/api/logout')
    #Operateur
    config.add_route('operateurs', '/infolica/api/operateurs')
    config.add_route('operateurs_s', '/infolica/api/operateurs/')
    config.add_route('operateur_by_id', '/infolica/api/operateurs/{id}')
    config.add_route('recherche_operateurs', '/infolica/api/recherche_operateurs')
    config.add_route('recherche_operateurs_s', '/infolica/api/recherche_operateurs/')
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
    #Numéros
    config.add_route('numeros','/infolica/api/numeros')
    config.add_route('numeros_s','/infolica/api/numeros/')
    config.add_route('types_numeros','/infolica/api/types_numeros')
    config.add_route('types_numeros_s','/infolica/api/types_numeros/')
    config.add_route('etats_numeros','/infolica/api/etats_numeros')
    config.add_route('etats_numeros_s','/infolica/api/etats_numeros/')
    config.add_route('recherche_numeros','/infolica/api/recherche_numeros')
    config.add_route('recherche_numeros_s','/infolica/api/recherche_numeros/')
    config.add_route('numero_by_id', '/infolica/api/numeros/{id}')
    config.add_route('numero_base_relations_by_id', '/infolica/api/numero_base_relations/{id}')
    config.add_route('numero_associe_relations_by_id', '/infolica/api/numero_associe_relations/{id}')
    #Réservation de numéros
    config.add_route('reservation_numeros','/infolica/api/reservation_numeros')
    config.add_route('reservation_numeros_s','/infolica/api/reservation_numeros/')
    #AffairesNuméros
    config.add_route('affaire_numeros','/infolica/api/affaire_numeros')
    config.add_route('affaire_numeros_s','/infolica/api/affaire_numeros/')
    config.add_route('affaire_numeros_by_affaire_id','/infolica/api/affaire_numeros/{id}')
    #Historique numéros
    config.add_route('numeros_etat_histo','/infolica/api/numeros_etat_histo')
    config.add_route('numeros_etat_histo_s','/infolica/api/numeros_etat_histo/')
    #Remarque affaire
    config.add_route('remarques_affaires_by_id','/infolica/api/remarques_affaires/{id}')
    config.add_route('remarques_affaires','/infolica/api/remarques_affaires')
    config.add_route('remarques_affaires_s','/infolica/api/remarques_affaires/')
    config.add_route('affaires_remarques_by_affaire_id','/infolica/api/affaire_remarques_affaires/{id}')
    #Etapes affaire
    config.add_route('etapes_by_id','/infolica/api/etapes/{id}')
    config.add_route('etapes','/infolica/api/etapes')
    config.add_route('etapes_s','/infolica/api/etapes/')
    config.add_route('etapes_index','/infolica/api/etapes_index')
    config.add_route('etapes_index_s','/infolica/api/etapes_index/')
    config.add_route('affaire_etapes_by_affaire_id','/infolica/api/affaire_etapes/{id}')
    #Numeros affaires
    config.add_route('numero_affaires_by_numero_id','/infolica/api/numero_affaires/{id}')
    #Preavis affaire
    config.add_route('preavis_by_id','/infolica/api/preavis/{id}')
    config.add_route('preavis','/infolica/api/preavis')
    config.add_route('preavis_s','/infolica/api/preavis/')
    config.add_route('preavis_type','/infolica/api/preavis_type')
    config.add_route('preavis_type_s','/infolica/api/preavis_type/')
    config.add_route('affaire_preavis_by_affaire_id','/infolica/api/affaire_preavis/{id}')
    #Documents affaire
    config.add_route('affaire_documents_by_affaire_id','/infolica/api/affaire_documents/{id}')
    #Emoluments facture
    config.add_route('emolument_facture_by_id','/infolica/api/emolument_facture/{id}')
    config.add_route('emolument_facture','/infolica/api/emolument_facture')
    config.add_route('emolument_facture_s','/infolica/api/emolument_facture/')
    config.add_route('facture_emoluments_by_facture_id','/infolica/api/facture_emoluments/{id}')
    #Envois
    config.add_route('envois_by_id','/infolica/api/envois/{id}')
    config.add_route('envois','/infolica/api/envois')
    config.add_route('envois_s','/infolica/api/envois/')
    config.add_route('envois_types','/infolica/api/envois_type')
    config.add_route('envois_types_s','/infolica/api/envois_type/')
    config.add_route('affaire_envois_by_affaire_id','/infolica/api/affaire_envois/{id}')
    #Suivi Mandat
    config.add_route('suivi_mandat_by_id','/infolica/api/suivi_mandats/{id}')
    config.add_route('suivi_mandats','/infolica/api/suivi_mandats')
    config.add_route('suivi_mandats_s','/infolica/api/suivi_mandats/')
    config.add_route('affaire_suivi_mandats_by_affaire_id','/infolica/api/affaire_suivi_mandats/{id}')
    #Cadastres
    config.add_route('cadastres','/infolica/api/cadastres')
    config.add_route('cadastres_s','/infolica/api/cadastres/')
    # Fonctions & roles
    config.add_route('fonctions', '/infolica/api/fonctions')
    config.add_route('fonctions_s', '/infolica/api/fonctions/')
    config.add_route('roles', '/infolica/api/roles')
    config.add_route('roles_s', '/infolica/api/roles/')
    config.add_route('fonctions_roles_by_id', '/infolica/api/fonctions_roles/{id}')
    #Services
    config.add_route('service_by_id','/infolica/api/services/{id}')
    config.add_route('services','/infolica/api/services')
    config.add_route('services_s','/infolica/api/services/')

