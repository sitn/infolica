# -*- coding: utf-8 -*--
from pyramid.view import view_config

from infolica.exceptions.custom_error import CustomError
from infolica.models.constant import Constant
from infolica.models.models import Affaire, AffaireNumero, ModificationAffaire
from infolica.models.models import AffaireEtape 
from infolica.scripts.utils import Utils

from datetime import datetime


###########################################################
# ABANDON AFFAIRE
###########################################################

@view_config(route_name='abandon_affaire_reopen_parent_affaire', request_method='POST', renderer='json')
def abandonAffaire_reopenParentAffaire_view(request):
    """
    Abandon child_affaire, reopen parent child_affaire and reattribute numbers to parent child_affaire.
    """

    settings = request.registry.settings
    etape_abandon_id = settings['affaire_etape_abandon_id']
    etape_reactivation_id = settings['affaire_etape_reactivation_id']

    child_affaire_id = request.params['affaire_id']
    operateur_id = request.params['operateur_id']

    # get child_affaire
    child_affaire = request.dbsession.query(ModificationAffaire).filter(Affaire.id == child_affaire_id).first()


    # get parent_affaire
    parent_affaire_id = request.dbsession.query(ModificationAffaire).filter(
        ModificationAffaire.affaire_id_fille == child_affaire_id).first().affaire_id_mere

    parent_affaire = request.dbsession.query(Affaire).filter(Affaire.id == parent_affaire_id).first()

    # reactivate parent-child_affaire if exists and abandon child_affaire
    if parent_affaire is not None:
        parent_affaire.date_cloture = None
        parent_affaire.abandon = False
    
        child_affaire.date_cloture = datetime.now().date()
        child_affaire.abandon = True

        # get numeros_affaire
        numeros_affaire = request.dbsession.query(AffaireNumero).filter(AffaireNumero.affaire_id == child_affaire_id).all()

        for numaff_child in numeros_affaire:
            # deactivate affaire_numero in child_affaire
            numaff_child.actif = False
            numaff_child.affaire_destination_id = parent_affaire_id

            # reactivate affaire-numero in parent_affaire
            numaff_parent = request.dbsession.query(AffaireNumero).filter(AffaireNumero.affaire_id == parent_affaire_id).first()
            if numaff_parent is not None:
                numaff_parent.actif = True
                numaff_parent.affaire_destination_id = None
            else:
                # Create it if it doesn't exists
                numaff_parent = AffaireNumero()
                numaff_parent.affaire_id = parent_affaire_id
                numaff_parent.numero_id = numaff_child.numero_id
                numaff_parent.type_id = numaff_child.type_id
                numaff_parent.actif = True
                request.dbsession.add(numaff_parent)

    else:
        raise CustomError(CustomError.RECORD_WITH_ID_NOT_FOUND.format(Affaire.__tablename__, parent_affaire_id))

    # Update etapes
    child_affaire_etape = AffaireEtape()
    child_affaire_etape.affaire_id = child_affaire_id
    child_affaire_etape.operateur_id = operateur_id
    child_affaire_etape.etape_id = etape_abandon_id
    child_affaire_etape.datetime = datetime.now()
    child_affaire_etape.remarque = "Affaire ouverte par erreur. Les numéros sont accessibles dans l'affaire " + str(parent_affaire_id) + "."
    request.dbsession.add(child_affaire_etape)

    parent_affaire_etape = AffaireEtape()
    parent_affaire_etape.affaire_id = parent_affaire_id
    parent_affaire_etape.operateur_id = operateur_id
    parent_affaire_etape.etape_id = etape_reactivation_id
    parent_affaire_etape.datetime = datetime.now()
    parent_affaire_etape.remarque = "Récupération des données de l'affaire " + str(parent_affaire_id) + ", ouverte par erreur."
    request.dbsession.add(parent_affaire_etape)

    return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(Affaire.__tablename__))
