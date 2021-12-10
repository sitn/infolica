import logging
from infolica.models import ControleEtape, ControleEtapeTypeAffaire
from infolica.models import Preavis

from sqlalchemy import func

LOGGER = logging.getLogger(__name__)

class ControleEtapeChecker():
    """
    Controls defined by step and affaire_type
    """

    @classmethod
    def controleEtape(cls, **kwargs):
        controles = cls._getControls(**kwargs)

        results = []
        for controle in controles:
            method_name = '_get_{}_controle'.format(controle.nom.lower())
            method = getattr(cls, method_name, cls._get_undefined_controle)

            result = {
                'nom': controle.nom,
                'detail': controle.detail,
                'force': controle.force,
                'result': method(controle_name=controle, **kwargs)
            }

            results.append(result)

        return results

    @classmethod
    def _get_undefined_controle(cls, **kwargs):
        controle_name = kwargs.get('controle_name')
        affaire_type_id = kwargs.get('affaire_type_id')
        etape_id = kwargs.get('etape_id')
        LOGGER.error('Control "{}" si not defined (affaire_type_id = {}, etape_id = {})'.format(controle_name, affaire_type_id, etape_id))



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



