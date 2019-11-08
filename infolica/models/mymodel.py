from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    Date,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)

import datetime

from .meta import Base


class Operateur(Base):
    __tablename__ = 'operateur'
    __table_args__ = {'schema': 'general'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)
    entree = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    sortie = Column(Date)


class Cadastre(Base):
    __tablename__ = 'cadastre'
    __table_args__ = {'schema': 'general'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class Plan(Base):
    __tablename__ = 'plan'
    __table_args__ = {'schema': 'general'}
    id = Column(Integer, primary_key=True)
    cadastre_id = Column(Integer, ForeignKey(Cadastre.id), nullable=False)
    nom = Column(Text, nullable=False)


class AffaireType(Base):
    __tablename__ = 'affaire_type'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class Affaire(Base):
    __tablename__ = 'affaire'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    responsable_id = Column(Integer, ForeignKey(Operateur.id), nullable=False)
    technicien_id = Column(Integer, ForeignKey(Operateur.id), nullable=False)
    type_id = Column(Integer, ForeignKey(
        AffaireType.id), nullable=False)
    cadastre_id = Column(Integer, ForeignKey(Cadastre.id), nullable=False)
    information = Column(Text)
    date_ouverture = Column(
        Date, default=datetime.datetime.utcnow, nullable=False)
    date_cloture = Column(Date)
    localisation_E = Column(Integer, nullable=False)
    localisation_N = Column(Integer, nullable=False)


class StatutAffaire(Base):
    __tablename__ = 'statut_affaire'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class EtapeAffaire(Base):
    __tablename__ = 'etape_affaire'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    statut_id = Column(Integer, ForeignKey(StatutAffaire.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class ModificationAffaireType(Base):
    __tablename__ = 'modification_affaire_type'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class ModificationAffaire(Base):
    __tablename__ = 'modification_affaire'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    affaire_id_mere = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    affaire_id_fille = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    type_id = Column(Integer, ForeignKey(
        ModificationAffaireType.id), nullable=False)


class Client(Base):
    __tablename__ = 'client'
    __table_args__ = {'schema': 'client'}
    id = Column(Integer, primary_key=True)
    adresse = Column(Text)
    npa = Column(Text)
    localite = Column(Text)
    tel_fixe = Column(Text)
    mail = Column(Text)
    entree = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    sortie = Column(Date)
    type = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'client',
        'polymorphic_on': type
    }


class ClientEntreprise(Client):
    __tablename__ = 'client_entreprise'
    __table_args__ = {'schema': 'client'}
    nom = Column(Text, nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'client_entreprise'}


class ClientPersonne(Client):
    __tablename__ = 'client_personne'
    __table_args__ = {'schema': 'client'}
    titre = Column(Text)
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)
    tel_portable = Column(Text, nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'client_personne'}


class RelationClientAffaireType(Base):
    __tablename__ = 'relation_affaire_client_type'
    __table_args__ = {'schema': 'client'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class RelationAffaireClient(Base):
    __tablename__ = 'relation_affaire_client'
    __table_args__ = {'schema': 'client'}
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    affaire_id = Column(Integer, ForeignKey(affaire.id), nullable=False)
    relation_type_id = Column(Integer, ForeignKey(
        RelationClientAffaireType.id), nullable=False)


class Facture(Base):
    __tablename__ = 'facture'
    __table_args__ = {'schema': 'facture'}
    sap = Column(Text, primary_key=True)
    client_id = Column(Integer, ForeignKey(client.id))
    montant_mo = Column(Float, default=0.0, nullable=False)
    montant_rf = Column(Float, default=0.0, nullable=False)
    montant_mat_diff = Column(Float, default=0.0, nullable=False)
    total = Column(Float, default=0.0, nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    type = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'facture',
        'polymorphic_on': type
    }

    def __init__(self, montant_mo, montant_rf, montant_mat_diff):
        self.montant_mo = montant_mo
        self.montant_rf = montant_rf
        self.montant_matdiff = montant_mat_diff

    def tva(self):
        self.tva = constant.tva * \
            (self.montant_mo + self.montant_matdiff)  # TVA MO

    def total(self):
        self.total = self.montant_mo + self.montant_rf + self.montant_matdiff


class FacturePartielle(Facture):
    __tablename__ = 'facture_partielle'
    __table_args__ = {'schema': 'facture'}
    immeuble = Column(Text, default='Tous', nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'facture_partielle'}


class EmolumentsMO(Base):
    __tablename__ = 'emoluments_mo'
    __table_args__ = {'schema': 'facture'}
    id = Column(Integer, primary_key=True)
    ...


class EmolumentsMOParametres(Base):
    __tablename__ = 'emoluments_mo_parametres'
    __table_args__ = {'schema': 'facture'}
    id = Column(Integer, primary_key=True)
    indice = Column(Float, default=0.0, nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class EmolumentsRF(Base):
    __tablename__ = 'emoluments_rf'
    __table_args__ = {'schema': 'facture'}
    id = Column(Integer, primary_key=True)
    affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    ...


class EmolumentsRFParametres(Base):
    __tablename__ = 'emoluments_rf_parametres'
    __table_args__ = {'schema': 'facture'}
    id = Column(Integer, primary_key=True)
    tarif_servitude_principale = Column(Float, default=0.0, nullable=False)
    tarif_servitude_secondaire = Column(Float, default=0.0, nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class RemarqueAffaire(Base):
    __tablename__ = 'remarque_affaire'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    remarque = Column(text, nullable=False)
    operateur_id = Column(Integer, ForeignKey(Operateur.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = {'schema': 'document'}
    id = Column(Integer, primary_key=True)
    chemin = Column(text, nullable=False)


class EnvoiDocument(Base):
    __tablename__ = 'envoi_document'
    __table_args__ = {'schema': 'document'}
    id = Column(Integer, primary_key=True)
    destinataire_id = Column(Integer, ForeignKey(Client.id) nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


# class SuiviMandat(Base):
#     __tablename__ = 'suivi_mandat'
#     __table_args__ = {'schema': 'controle'}
#     id = Column(Integer, primary_key=True)
#     affaire_id = Column(Integer, ForeignKey(Affaire.id) nullable=False)
#     ...


# class ControleMutation(Base):
#     __tablename__ = 'controle_mutation'
#     __table_args__ = {'schema': 'controle'}
#     id = Column(Integer, primary_key=True)
#     affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
#     ...


# class ControleMutation(Base):
#     __tablename__ = 'controle_mutation'
#     __table_args__ = {'schema': 'controle'}
#     id = Column(Integer, primary_key=True)
#     affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
#     ...


class NumeroType(Base):
    __tablename__ = 'numero_type'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class NumeroEtat(Base):
    __tablename__ = 'numero_etat'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class Numero(Base):
    __tablename__ = 'numero'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    cadastre_id = Column(Integer, ForeignKey(Cadastre.id), nullable=False)
    type_id = Column(Integer, ForeignKey(NumeroType.id), nullable=False)
    numero = Column(Integer, nullable=False)
    suffixe = Column(Text)
    etat_id = Column(Integer, ForeignKey(NumeroEtat.id), nullable=False)


class RelationType(Base):
    __tablename__ = 'relation_type'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class NumeroRelation(Base):
    __tablename__ = 'numero_relation'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    numero_id_base = Column(Integer, ForeignKey(Numero.id), nullable=False)
    numero_id_associe = Column(Integer, ForeignKey(Numero.id), nullable=False)
    relation_type_id = Column(Integer, ForeignKey(
        RelationType.id), nullable=False)


class NumeroPlan(Base):
    __tablename__ = 'numero_plan'
    __table_args__ = {'schema': 'numero'}
    id = Column(Integer, primary_key=True)
    numero_id = Column(Integer, ForeignKey(Numero.id), nullable=False)
    plan_id = Column(Integer, ForeignKey(Plan.id), nullable=False)


class AffaireNumero(Base):
    __tablename__ = 'affaire_numero'
    __table_args__ = {'schema': 'affaire'}
    id = Column(Integer, primary_key=True)
    affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    numero_id = Column(Integer, ForeignKey(Numero.id), nullable=False)
    modifie = Column(Boolean, default=False, nullable=False)


class Services(Base):
    __tablename__ = 'service'
    __table_args__ = {'schema': 'preavis'}
    id = Column(Integer, primary_key=True)
    service = Column(Text, nullable=False)
    nom = Column(Text)
    prenom = Column(Text)
    adresse = Column(Text)
    npa = Column(Text)
    localite = Column(Text)
    telephone = Column(Text)
    mail = Column(Text)


class RemarquePreavis(Base):
    __tablename__ = 'remarque_preavis'
    __table_args__ = {'schema': 'preavis'}
    id = Column(Integer, primary_key=True)
    remarque = Column(Text, nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class PreavisType(Base):
    __tablename__ = 'preavis_type'
    __table_args__ = {'schema': 'preavis'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class PreavisDecision(Base):
    __tablename__ = 'preavis_decision'
    __table_args__ = {'schema': 'preavis'}
    id = Column(Integer, primary_key=True)
    nom = Column(Text, nullable=False)


class Preavis(Base):
    __tablename__ = 'preavis'
    __table_args__ = {'schema': 'preavis'}
    id = Column(Integer, primary_key=True)
    affaire_id = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    service_id = Column(Integer, ForeignKey(Service.id), nullable=False)
    preavis_id = Column(Text, ForeignKey(Preavis_type.id) nullable=False)
    decision = Column(Text, ForeignKey(PreavisDecision.id), nullable=False)
    date_demande = Column(
        Date, default=datetime.datetime.utcnow, nullable=False)
    date_reponse = Column(Date)
