import logging
from infolica.models import AffaireNumero, ControleEtape, ControleEtapeTypeAffaire, ControleGeometre, ControleMutation
from infolica.models import Emolument, EmolumentAffaire, EmolumentAffaireRepartition, Facture, NumeroRelation
from infolica.models import Preavis, SuiviMandat
from infolica.models import NumeroDiffere, VAffaire

from infolica.scripts.utils import Utils
from sqlalchemy import func

LOGGER = logging.getLogger(__name__)

class ControleEtapeChecker():
    """
    Controls defined by step and affaire_type
    """

    @classmethod
    def controleEtape(cls, **kwargs):
        controles = cls._getControls(**kwargs)

        final_decision = True
        results = []
        for controle in controles:
            ctrl_nom = controle.nom.lower()
            if ctrl_nom.endswith('_2') or ctrl_nom.endswith('_3'):
                ctrl_nom = ctrl_nom[:-2]
            method_name = '_get_{}_controle'.format(ctrl_nom)
            method = getattr(cls, method_name, cls._get_undefined_controle)

            # Apply control
            actual_decision = method(controle_name=controle, **kwargs)

            if controle.force == "INFO":
                if actual_decision is True:
                    result = {
                        'nom': controle.nom,
                        'detail': controle.detail,
                        'force': controle.force,
                        'result': True
                    }

                else:
                    break

            else:
                result = {
                    'nom': controle.nom,
                    'detail': controle.detail,
                    'force': controle.force,
                    'result': actual_decision
                }

            results.append(result)
            
            if final_decision and not actual_decision and controle.force == "NOGO":
                final_decision = False


        final_decision = {
            'nom': 'DECISION_FINALE',
            'detail': None,
            'force': None,
            'result': final_decision
        }

        result = {
            'detail': results,
            'final_decision': final_decision
        }

        return result

    @classmethod
    def _get_undefined_controle(cls, **kwargs):
        controle_name = kwargs.get('controle_name')
        affaire_type_id = kwargs.get('affaire_type_id')
        etape_id = kwargs.get('etape_id')
        LOGGER.error('Control "{}" is not defined (affaire_type_id = {}, etape_id = {})'.format(controle_name.nom, affaire_type_id, etape_id))
        return None



    @staticmethod
    def _getControls(**kwargs):
        request = kwargs.get('request')
        affaire_type_id = kwargs.get('affaire_type_id')
        etape_id = kwargs.get('etape_id')

        controles = request.dbsession.query(
            ControleEtape
        ).join(
            ControleEtapeTypeAffaire
        ).filter(
            ControleEtapeTypeAffaire.affaire_type_id == affaire_type_id
        ).filter(
            ControleEtape.nom == ControleEtapeTypeAffaire.controle_etape_nom
        ).filter(
            ControleEtape.etape_id == etape_id
        ).all()

        return controles


    @staticmethod
    def _get_demande_preavis_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')
        
        query = request.dbsession.query(
            func.count(Preavis.affaire_id)
        ).filter(
            Preavis.affaire_id == affaire_id
        )

        nb_demandes = query.scalar() 
        nb_reponses = query.filter(Preavis.date_reponse != None).scalar()

        return nb_demandes == nb_reponses
    
    
    @staticmethod
    def _get_presence_facture_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')
        
        facture_type_facture_id = int(request.registry.settings['facture_type_facture_id'])

        test = request.dbsession.query(
            func.count(Facture.affaire_id)
        ).filter(
            Facture.affaire_id == affaire_id
        ).filter(
            Facture.type_id == facture_type_facture_id
        ).scalar()

        return test > 0
    
    
    @staticmethod
    def _get_presence_emolument_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')
        
        test = request.dbsession.query(
            func.count(Emolument.emolument_affaire_id)
        ).join(
            EmolumentAffaire
        ).filter(
            Emolument.emolument_affaire_id == EmolumentAffaire.id
        ).filter(
            EmolumentAffaire.affaire_id == affaire_id
        ).scalar()

        return test > 0
    

    @staticmethod
    def _get_numero_reserve_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        test = request.dbsession.query(
            func.count(AffaireNumero.affaire_id)
        ).filter(
            AffaireNumero.affaire_id == affaire_id
        ).filter(
            AffaireNumero.type_id == int(request.registry.settings['affaire_numero_type_nouveau_id'])
        ).scalar()

        return test > 0
    

    @staticmethod
    def _get_controle_chef_projet_mo_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        ctrl = request.dbsession.query(
            ControleMutation
        ).filter(
            ControleMutation.affaire_id == affaire_id
        ).first()

        ctrl = Utils.serialize_one(ctrl)

        if ctrl is None:
            return False
        
        if ctrl['visa'] is None:
            return False
        else:
            return True
    

    @staticmethod
    def _get_controle_coordinateur_projets_mo_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        ctrl = request.dbsession.query(
            SuiviMandat
        ).filter(
            SuiviMandat.affaire_id == affaire_id
        ).first()

        ctrl = Utils.serialize_one(ctrl)

        if ctrl is None:
            return False
        
        if ctrl['visa'] is None:
            return False
        else:
            return True


    @staticmethod
    def _get_controle_geometre_cantonal_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        ctrl = request.dbsession.query(
            ControleGeometre
        ).filter(
            ControleGeometre.affaire_id == affaire_id
        ).first()

        ctrl = Utils.serialize_one(ctrl)

        if ctrl is None:
            return False
        
        if ctrl['operateur_id'] is None:
            return False
        else:
            return True
    

    @staticmethod
    def _get_numero_reference_cadastration_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        test = request.dbsession.query(
            func.count(AffaireNumero.numero_id)
        ).filter(
            AffaireNumero.affaire_id == affaire_id
        ).filter(
            AffaireNumero.type_id == int(request.registry.settings['affaire_numero_type_ancien_id'])
        ).scalar()

        return test > 0
    

    @staticmethod
    def _get_emolument_inscription_rf_cadastration_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        emoluments = request.dbsession.query(
            Emolument
        ).join(
            EmolumentAffaire
        ).filter(
            Emolument.emolument_affaire_id == EmolumentAffaire.id
        ).filter(
            EmolumentAffaire.affaire_id == affaire_id
        ).filter(
            Emolument.tableau_emolument_id.in_([99, 100])
        ).all()

        if emoluments is None:
            return False

        somme = 0
        for emol in emoluments:
            somme += emol.montant

        return somme > 0
    

    @staticmethod
    def _get_emoluments_factures_repartition_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        facture_type_facture_id = int(request.registry.settings['facture_type_facture_id'])

        nb_emoluments = request.dbsession.query(
            func.count(Emolument.tableau_emolument_id)
        ).join(
            EmolumentAffaire, Emolument.emolument_affaire_id == EmolumentAffaire.id
        ).filter(
            EmolumentAffaire.affaire_id == affaire_id
        ).scalar()

        # Si les émoluments n'existent pas pour l'affaire, ne pas bloquer
        if nb_emoluments is None or nb_emoluments == 0:
            return True

        unlinked_emoluments = request.dbsession.query(
            func.count(EmolumentAffaire.id)
        ).outerjoin(
            EmolumentAffaireRepartition, EmolumentAffaire.id == EmolumentAffaireRepartition.emolument_affaire_id
        ).filter(
            EmolumentAffaire.affaire_id == affaire_id
        ).filter(
            EmolumentAffaire.facture_type_id == facture_type_facture_id
        ).filter(
            EmolumentAffaireRepartition.emolument_affaire_id == None
        ).scalar()

        return unlinked_emoluments == 0
    
    
    @staticmethod
    def _get_emoluments_rf_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        montant_rf = request.dbsession.query(
            func.sum(Emolument.montant)
        ).join(
            EmolumentAffaire, Emolument.emolument_affaire_id == EmolumentAffaire.id
        ).filter(
            EmolumentAffaire.affaire_id == affaire_id
        ).filter(
            Emolument.tableau_emolument_id.in_([96, 97, 98, 103])
        ).scalar()

        if montant_rf is None:
            return False

        return montant_rf > 0
    
    
    @staticmethod
    def _get_facture_no_sap_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')
        
        facture_type_facture_id = int(request.registry.settings['facture_type_facture_id'])

        factures = request.dbsession.query(
            Facture
        ).filter(
            Facture.affaire_id == affaire_id
        ).filter(
            Facture.type_id == facture_type_facture_id
        ).all()

        if factures is None:
            return True

        test = True
        for facture in factures:
            if facture.sap is None or facture.sap == "":
                test = False
                break

        return test
    

    @staticmethod
    def _get_presence_balance_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        test = request.dbsession.query(
            func.count(NumeroRelation.id)
        ).filter(
            NumeroRelation.affaire_id == affaire_id
        ).scalar()

        return test > 0
    

    @staticmethod
    def _get_mat_diff_observation_balance_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        nb_mat_diff = request.dbsession.query(
            func.count(NumeroDiffere.id)
        ).filter(
            NumeroDiffere.affaire_id == affaire_id,
            NumeroDiffere.date_entree != None,
            NumeroDiffere.date_sortie == None
        ).scalar()

        return nb_mat_diff > 0
    

    @staticmethod
    def _get_geos_retarder_validation_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')

        affaire = request.dbsession.query(VAffaire).filter(
            VAffaire.id == affaire_id
        ).first()

        return not affaire.geos_retarder_validation is True

