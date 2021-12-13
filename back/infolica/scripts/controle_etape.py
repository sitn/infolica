import logging
from infolica.models import AffaireNumero, ControleEtape, ControleEtapeTypeAffaire, ControleMutation
from infolica.models import EmolumentAffaire, Emolument, Facture, Preavis

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
            method_name = '_get_{}_controle'.format(controle.nom.lower())
            method = getattr(cls, method_name, cls._get_undefined_controle)

            # Apply control
            actual_decision = method(controle_name=controle, **kwargs)

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
        results.append(final_decision)

        return results

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
        
        test = request.dbsession.query(
            func.count(Preavis.affaire_id)
        ).filter(
            Preavis.affaire_id == affaire_id
        ).scalar()

        return test > 0
    
    
    @staticmethod
    def _get_presence_facture_controle(**kwargs):
        request = kwargs.get('request')
        affaire_id = kwargs.get('affaire_id')
        
        test = request.dbsession.query(
            func.count(Facture.affaire_id)
        ).filter(
            Facture.affaire_id == affaire_id
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
        
        result = False
        for attr in ctrl:
            if ctrl[attr] is True:
                result = True
                break

        return result
    

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
