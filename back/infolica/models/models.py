from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Float,
    Text,
    String,
    Date,
    DateTime,
    Boolean,
    ARRAY,
    ForeignKey,
    UniqueConstraint,
)

from geoalchemy2 import Geometry

import datetime
from .constant import Constant
from .meta import Base


class Operateur(Base):
    __tablename__ = 'operateur'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)
    login = Column(Text)  # , nullable=False)
    responsable = Column(Boolean, default=False, nullable=False)
    entree = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    sortie = Column(Date)


class Cadastre(Base):
    __tablename__ = 'cadastre'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class ClientType(Base):
    __tablename__ = 'client_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Client(Base):
    __tablename__ = 'client'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_client = Column(BigInteger, ForeignKey(ClientType.id), nullable=False)
    entreprise = Column(Text)
    titre = Column(Text)
    nom = Column(Text)
    prenom = Column(Text)
    represente_par = Column(Text)
    co = Column(Text)
    adresse = Column(Text)
    npa = Column(Text)
    localite = Column(Text)
    case_postale = Column(Text)
    tel_fixe = Column(Text)
    fax = Column(Text)
    tel_portable = Column(Text)
    mail = Column(Text)
    entree = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    sortie = Column(Date)
    no_sap = Column(Text)
    no_bdp_bdee = Column(Text)


class ClientMoralPersonne(Base):
    __tablename__ = 'client_moral_personne'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_id = Column(BigInteger, ForeignKey(Client.id), nullable=False)
    titre = Column(Text)
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)


class Plan(Base):
    __tablename__ = 'mo_distr_plan'
    __table_args__ = {'schema': 'infolica'}
    idobj = Column(Text, primary_key=True)
    id_obj2 = Column(Text)
    planno = Column(Text)
    typlan = Column(Text)
    datmev = Column(Text)
    statut = Column(Text)
    echell = Column(Integer)
    idborplan = Column(Text)
    idrepplan = Column(Text)
    base = Column(Text)
    geom = Column(Geometry("POLYGON"))


class AffaireType(Base):
    __tablename__ = 'affaire_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger)
    reservation_numeros_types_id = Column(ARRAY(BigInteger))
    modif_affaire_type_id_vers = Column(ARRAY(BigInteger))
    logique_processus = Column(ARRAY(BigInteger))


class Affaire(Base):
    __tablename__ = 'affaire'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    no_access = Column(Text)
    nom = Column(Text)
    client_commande_id = Column(BigInteger, ForeignKey(Client.id))
    client_commande_complement = Column(Text)
    client_envoi_id = Column(BigInteger, ForeignKey(Client.id))
    client_envoi_complement = Column(Text)
    responsable_id = Column(BigInteger, ForeignKey(Operateur.id))
    technicien_id = Column(BigInteger, ForeignKey(
        Operateur.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(
        AffaireType.id), nullable=False)
    cadastre_id = Column(BigInteger, ForeignKey(Cadastre.id), nullable=False)
    information = Column(Text)
    date_ouverture = Column(
        Date, default=datetime.datetime.utcnow, nullable=False)
    date_validation = Column(Date)
    date_envoi = Column(Date)
    date_cloture = Column(Date)
    localisation_E = Column(Float, nullable=False)
    localisation_N = Column(Float, nullable=False)
    vref = Column(Text)
    chemin = Column(Text)
    abandon = Column(Boolean)


class AffaireEtapeIndex(Base):
    __tablename__ = 'affaire_etape_index'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger)


class AffaireEtape(Base):
    __tablename__ = 'affaire_etape'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    etape_id = Column(BigInteger, ForeignKey(AffaireEtapeIndex.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow(), nullable=False)
    remarque = Column(Text)


class ModificationAffaireType(Base):
    __tablename__ = 'modification_affaire_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger)
    reservation_numeros_types_id = Column(ARRAY(BigInteger))
    affaire_source_type_id = Column(ARRAY(BigInteger))


class ModificationAffaire(Base):
    __tablename__ = 'modification_affaire'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id_mere = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    affaire_id_fille = Column(Integer, ForeignKey(Affaire.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(
        ModificationAffaireType.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class Facture(Base):
    __tablename__ = 'facture'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sap = Column(Text)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    client_id = Column(BigInteger, ForeignKey(Client.id), nullable=False)
    client_co_id = Column(BigInteger, ForeignKey(Client.id))
    client_complement = Column(Text)
    client_premiere_ligne = Column(Text)
    indice_application_mo = Column(Float, default=1.2)
    indice_tva = Column(Float, default=7.7)
    montant_mo = Column(Float, default=0.0, nullable=False)
    montant_rf = Column(Float, default=0.0, nullable=False)
    montant_mat_diff = Column(Float, default=0.0, nullable=False)
    montant_tva = Column(Float, default=0.0, nullable=False)
    montant_total = Column(Float, default=0.0, nullable=False)
    date = Column(Date)
    remarque = Column(Text)
    numeros = Column(ARRAY(BigInteger))


class TableauEmoluments(Base):
    __tablename__ = 'tableau_emoluments'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    domaine = Column(Text, nullable=False)
    categorie = Column(Text, nullable=False)
    sous_categorie = Column(Text, nullable=False)
    nom = Column(Text, nullable=False)
    unite = Column(Text, nullable=False)
    montant = Column(Float, default=0.0, nullable=False)


class EmolumentFacture(Base):
    __tablename__ = 'emolument_facture'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    facture_id = Column(BigInteger, ForeignKey(Facture.id), nullable=False)
    emolument_id = Column(BigInteger, ForeignKey(
        TableauEmoluments.id), nullable=False)
    nombre = Column(Integer, nullable=False)
    facteur_correctif = Column(Float, default=1.0, nullable=False)
    batiment = Column(Text)
    montant = Column(Float, default=0.0, nullable=False)


class RemarqueAffaire(Base):
    __tablename__ = 'remarque_affaire'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    remarque = Column(Text, nullable=False)
    operateur_id = Column(BigInteger, ForeignKey(Operateur.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class DocumentType(Base):
    __tablename__ = 'document_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    chemin = Column(Text, nullable=False)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(DocumentType.id), nullable=False)

class EnvoiType(Base):
    __tablename__ = 'envoi_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Envoi(Base):
    __tablename__ = 'envoi'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    client_id = Column(BigInteger, ForeignKey(Client.id), nullable=False)
    client_complement = Column(Text)
    type_id = Column(BigInteger, ForeignKey(EnvoiType.id))
    date = Column(Date, default=datetime.datetime.utcnow)


class EnvoiDocument(Base):
    __tablename__ = 'envoi_document'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    envoi_id = Column(BigInteger, ForeignKey(Envoi.id), nullable=False)
    document_id = Column(BigInteger, ForeignKey(Document.id), nullable=False)


class SuiviMandatStatut(Base):
    __tablename__ = 'suivi_mandat_statut'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class SuiviMandat(Base):
    __tablename__ = 'suivi_mandat'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id))
    av_11 = Column(Boolean)  # CREATION DE L’AFFAIRE DANS INFOLICA
    av_12 = Column(Date)  # DATE CREATION DE L’AFFAIRE DANS INFOLICA
    av_21 = Column(Boolean)  # CREATION DE L’AFFAIRE DANSTIMELEAD
    av_31 = Column(Boolean)  # VERIFICATION PAR LE CHEF DE PROJET DE LA MENSURATION OFFICIELLE
    av_32 = Column(BigInteger, ForeignKey(Operateur.id))  # LE CHEF DE PROJET
    av_33 = Column(Date)  # DATE DE LA VERIFICATION PAR LE CHEF DE PROJET
    av_41 = Column(Boolean)  # REPORT DATE PREAVIS SAT OU SEA
    av_51 = Column(Text)  # INFORMATIONS COMPLEMENTAIRES
    pdt_11 = Column(Boolean)  # CONTROLE DES DESIGNATIONS ET DE LA BALANCE
    pdt_12 = Column(Text)  # REMARQUE CONTROLE DES DESIGNATIONS ET DE LA BALANCE
    pdt_21 = Column(Boolean)  # CONTROLE DU TABLEAU DES EMOLUMENTS ET REPORT SUR LA DEMANDE
    pdt_22 = Column(Text)  # REMARQUE CONTROLE DU TABLEAU DES EMOLUMENTS ET REPORT SUR LA DEMANDE
    pdt_31 = Column(Boolean)  # MATERIALISATION DIFFEREE (COPIE DU PLAN DE MUTATION)
    pdt_41 = Column(Boolean)  # CONTROLE DE L'ENREGISTREMENT DE TOUS LES DOCUMENTS (COURRIEL, COURRIER, PREAVIS, PLAN, ETC…)
    pdt_42 = Column(
        Text)  # REMARQUE CONTROLE DE L'ENREGISTREMENT DE TOUS LES DOCUMENTS (COURRIEL, COURRIER, PREAVIS, PLAN, ETC…)
    ap_11 = Column(Boolean)  # RESPECT DES DIRECTIVES DU SCAT, SAGR OU SERVICE URBANISME
    ap_12 = Column(Text)  # REMARQUE RESPECT DES DIRECTIVES DU SCAT, SAGR OU SERVICE URBANISME
    ap_21 = Column(Boolean)  # STRUCTURE DES REPERTOIRES ET CONTENU
    ap_22 = Column(Text)  # REMARQUE STRUCTURE DES REPERTOIRES ET CONTENU
    ap_31 = Column(Boolean)  # GENERATION DE L’ETAT DESCRIPTIF POUR TERRIS
    ap_32 = Column(BigInteger, ForeignKey(Operateur.id))  # CHEF DE PROJET
    ap_33 = Column(Date)  # DATE GENERATION DE L’ETAT DESCRIPTIF POUR TERRIS
    ap_41 = Column(Boolean)  # CONTROLE DE LA BASE DE DONNEES
    ap_42 = Column(Text)  # REMARQUE CONTROLE DE LA BASE DE DONNEES
    visa = Column(BigInteger, ForeignKey(Operateur.id))
    date = Column(Date)


class ControleMutation(Base):
    __tablename__ = 'controle_mutation'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id))
    terrain_1 = Column(Date)  # Terrain - Levés préliminaires
    terrain_2 = Column(Date)  # Terrain - Matérialisations
    terrain_3 = Column(Date)  # Terrain - Levés
    bureau_1 = Column(Date)  # Bureau - Calculs préliminaires
    bureau_2 = Column(Date)  # Bureau - Calculs définitifs
    bureau_3 = Column(Date)  # Bureau - Calculs spéciaux
    envoi_cl_1 = Column(Date)  # Situation_affaire - Envoi au client
    retour_cl_2 = Column(Date)  # Sitation_affaire - Retour du client
    suivi_1 = Column(Date)  # Suivi - Création de la mutation dans la BD
    suivi_2 = Column(Date)  # Suivi - Contrôles de cohérences e.o.
    suivi_3 = Column(Date)  # Suivi - Production des désignations
    suivi_4 = Column(Date)  # Suivi - Production plan de mutation (papier)
    suivi_5 = Column(Date)  # Suivi - Production plan de mutation (PDF)
    suivi_6 = Column(Date)  # Suivi - Enregistrement de la documentation
    suivi_7 = Column(Date)  # Suivi - État de la mutation "En cours / Libérée"
    suivi_8 = Column(Date)  # Suivi - Tableau des émoluments
    suivi_9 = Column(Date)  # Suivi - Transmission au géomètre cantonal
    suivi_10 = Column(Date)  # Suivi - Transmission au secrétariat
    suivi_11 = Column(Date)  # Suivi - Validation technique de la mutation
    suivi_12 = Column(Date)  # Suivi - Annulation de la mutation
    bf_1 = Column(Boolean)  # Contrôler les numéros des points limites ainsi que la valeur, la prévision et la fiabilité des points sont en adéquation avec le niveau de tolérence de la zone de travail
    bf_2 = Column(Boolean)  # Contrôler dans la table « Bien_fonds => Mise_a_jourBF » qu’il y que les nouveaux biens-fonds créés dans votre affaire et qu'il n'y a pas de biens-fonds sans géométrie
    bf_3 = Column(Boolean)  # Contrôler dans la table « Bien_fonds » que l’attribut « Validation_juridique » est non pour les nouveaux biens-fonds sauf pour les nouveaux DP.
    bf_4 = Column(Boolean)  # Contrôler dans la table « Biens_fonds.PosImmeuble » que les éléments suivants sont corrects (Hali=Center, Vali=Half, Grandeur=Petite.petite).
    cs_1 = Column(Boolean)  # Contrôler les numéros des points particuliers "660" ainsi que la valeur, la précision et la fiabilité des points sont en adéquations avec le niveau de tolérance de la zone de travail.
    cs_2 = Column(Boolean)  # Contrôler dans la table « Couverture_du_sol => Mise_a_jourCS » qu’il y a que les nouvelles surfaces créées dans votre affaire qu'il n'y a pas de surfaces sans géométrie.
    cs_3 = Column(Boolean)  # Contrôler dans la table « Couverture_du_sol => PosNumero_de_batiment » que les éléments suivants sont corrects (Hali=Center, Vali=Base, Grandeur=Petite.tres_petite).
    cs_4 = Column(Boolean)  # Insérer les points dans la base Acces des bâtiments projets (voir Processus)
    cs_5 = Column(Boolean)  # Contrôler la géométrie des EGID (01.01.2012).
    od_1 = Column(Boolean)  # Tous les points de constructions "760" sont supprimés.
    od_2 = Column(Boolean)  # Contrôler les nouveaux éléments créés dans votre affaire et qu'il n'y a pas d'objets divers sans géométrie.
    od_3 = Column(Boolean)  # Contrôler que les bâtiments souterrains ont les bons numéros et une désignation.
    od_4 = Column(Boolean)  # Insérer les points dans la base Acces des bâtiments projets (voir Processus)
    od_5 = Column(Boolean)  # Contrôler que l'attribut « Objets_divers => SymboleElement_surfacique » est rempli pour les piscines.
    bat_1 = Column(Boolean)  # Contrôler dans la table « Adresses_des_batiments => Mise_a_jourBAT » qu’il y a bien que les nouveaux éléments que vous avez créés dans votre affaire.
    bat_2 = Column(Boolean)  # Contrôler dans la table « Adresses_des_batiments => PosNumero_maison » que les éléments suivants sont corrects (Hali=Center, Vali=Half, Grandeur=Petite.assez_petite).
    bat_3 = Column(Boolean)  # Contrôler que les points adresses sont dans les géométries.
    serv_1 = Column(Boolean)  # Contrôler dans la table « Servitudes => Mise_a_jourSE » qu’il y a bien que les nouveaux éléments que vous avez créés dans votre affaire.
    serv_2 = Column(Boolean)  # Contrôler dans la table « Servitudes => Servitude_surface » ou « Servitudes => Servitude_ligne » ou « Servitudes => Servitude_point » que l’attribut « Validite » est en_projet pour les nouvelles servitudes.
    serv_3 = Column(Boolean)  # Contrôler dans la table « Servitudes => PosNumero_de_servitude » que les éléments suivants sont corrects (Hali=Left, Vali=Base, Grandeur= -).
    nom_1 = Column(Boolean)  # A partir de deux noms locaux pour un bien-fonds vérifier si cela est exact.
    suiv_mut_1 = Column(Boolean)  # Supprimer dans la gestion des mutations les « Topic » qui ne sont pas utilisés.
    suiv_mut_2 = Column(Boolean)  # Mutation "En cours/Libérée".
    div_1 = Column(Boolean)  # Épurations des fichiers dans le répertoire de l’affaire.
    div_2 = Column(Boolean)  # Contrôler que vous avez bien saisi le dernier numéro de point de l’affaire concernée dans le programme « Réservation des numéros ».
    div_3 = Column(Boolean)  # Contrôler rigoureusement les désignations, la balance ainsi que les observations pour le registre foncier.
    visa = Column(BigInteger, ForeignKey(Operateur.id))
    date = Column(Date)


class ControlePPE(Base):
    __tablename__ = 'controle_ppe'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    operateur_id = Column(BigInteger, ForeignKey(Operateur.id), nullable=False)
    date = Column(Date)
    gen_1 = Column(Boolean)
    gen_2 = Column(Boolean)
    gen_3 = Column(Boolean)
    gen_4 = Column(Boolean)
    gen_5 = Column(Boolean)
    gen_6 = Column(Boolean)
    gen_7 = Column(Boolean)
    gen_8 = Column(Boolean)
    gen_9 = Column(Boolean)
    gen_remarque = Column(Text)
    dos_a = Column(Boolean)
    dos_b = Column(Boolean)
    dos_c = Column(Boolean)
    dos_d = Column(Boolean)
    dos_e = Column(Boolean)
    dos_f = Column(Boolean)
    dos_g = Column(Boolean)
    dos_h = Column(Boolean)
    dos_remarque = Column(Text)
    jur_a = Column(Boolean)
    jur_b = Column(Boolean)
    jur_c = Column(Boolean)
    jur_d = Column(Boolean)
    jur_remarque = Column(Text)
    psit_a = Column(Boolean)
    psit_b = Column(Boolean)
    psit_c = Column(Boolean)
    psit_d = Column(Boolean)
    psit_e = Column(Boolean)
    psit_f = Column(Boolean)
    psit_g = Column(Boolean)
    psit_h = Column(Boolean)
    psit_i = Column(Boolean)
    psit_j = Column(Boolean)
    psit_k = Column(Boolean)
    psit_l = Column(Boolean)
    psit_m = Column(Boolean)
    psit_n = Column(Boolean)
    psit_o = Column(Boolean)
    psit_p = Column(Boolean)
    psit_q = Column(Boolean)
    psit_r = Column(Boolean)
    psit_s = Column(Boolean)
    psit_t = Column(Boolean)
    psit_u = Column(Boolean)
    psit_v = Column(Boolean)
    psit_w = Column(Boolean)
    psit_x = Column(Boolean)
    psit_y = Column(Boolean)
    psit_z = Column(Boolean)
    psit_remarque = Column(Text)
    pet_a = Column(Boolean)
    pet_b = Column(Boolean)
    pet_c = Column(Boolean)
    pet_d = Column(Boolean)
    pet_e = Column(Boolean)
    pet_f = Column(Boolean)
    pet_g = Column(Boolean)
    pet_h = Column(Boolean)
    pet_i = Column(Boolean)
    pet_j = Column(Boolean)
    pet_k = Column(Boolean)
    pet_l = Column(Boolean)
    pet_m = Column(Boolean)
    pet_n = Column(Boolean)
    pet_o = Column(Boolean)
    pet_p = Column(Boolean)
    pet_q = Column(Boolean)
    pet_r = Column(Boolean)
    pet_remarque = Column(Text)
    cart_a = Column(Boolean)
    cart_b = Column(Boolean)
    cart_c = Column(Boolean)
    cart_d = Column(Boolean)
    cart_e = Column(Boolean)
    cart_f = Column(Boolean)
    cart_g = Column(Boolean)
    cart_h = Column(Boolean)
    cart_i = Column(Boolean)
    cart_j = Column(Boolean)
    cart_remarque = Column(Text)
    uet_a = Column(Boolean)
    uet_b = Column(Boolean)
    uet_c = Column(Boolean)
    uet_d = Column(Boolean)
    uet_e = Column(Boolean)
    uet_f = Column(Boolean)
    uet_g = Column(Boolean)
    uet_h = Column(Boolean)
    uet_i = Column(Boolean)
    uet_j = Column(Boolean)
    uet_k = Column(Boolean)
    uet_l = Column(Boolean)
    uet_m = Column(Boolean)
    uet_n = Column(Boolean)
    uet_o = Column(Boolean)
    uet_p = Column(Boolean)
    uet_q = Column(Boolean)
    uet_r = Column(Boolean)
    uet_s = Column(Boolean)
    uet_t = Column(Boolean)
    uet_u = Column(Boolean)
    uet_v = Column(Boolean)
    uet_w = Column(Boolean)
    uet_x = Column(Boolean)
    uet_y = Column(Boolean)
    uet_z = Column(Boolean)
    uet_aa = Column(Boolean)
    uet_ab = Column(Boolean)
    uet_ac = Column(Boolean)
    uet_ad = Column(Boolean)
    uet_ae = Column(Boolean)
    uet_remarque = Column(Text)
    dup_a = Column(Boolean)
    dup_b = Column(Boolean)
    dup_c = Column(Boolean)
    dup_d = Column(Boolean)
    dup_e = Column(Boolean)
    dup_f = Column(Boolean)
    dup_g = Column(Boolean)
    dup_h = Column(Boolean)
    dup_i = Column(Boolean)
    dup_remarque = Column(Text)
    leg_a = Column(Boolean)
    leg_b = Column(Boolean)
    leg_c = Column(Boolean)
    leg_d = Column(Boolean)
    leg_e = Column(Boolean)
    leg_f = Column(Boolean)
    leg_g = Column(Boolean)
    leg_h = Column(Boolean)
    leg_i = Column(Boolean)
    leg_j = Column(Boolean)
    leg_k = Column(Boolean)
    leg_l = Column(Boolean)
    leg_m = Column(Boolean)
    leg_n = Column(Boolean)
    leg_o = Column(Boolean)
    leg_p = Column(Boolean)
    leg_q = Column(Boolean)
    leg_r = Column(Boolean)
    leg_s = Column(Boolean)
    leg_t = Column(Boolean)
    leg_u = Column(Boolean)
    leg_v = Column(Boolean)
    leg_w = Column(Boolean)
    leg_x = Column(Boolean)
    leg_y = Column(Boolean)
    leg_remarque = Column(Text)
    balsurf_a = Column(Boolean)
    balsurf_b = Column(Boolean)
    balsurf_c = Column(Boolean)
    balsurf_d = Column(Boolean)
    balsurf_remarque = Column(Text)


class ControleGeometre(Base):
    __tablename__ = 'controle_geometre'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = (BigInteger, ForeignKey(Affaire.id))
    check_1 = Column(Boolean)  # Nom du cadastre et n° de bien-fonds corrects (cf extrait RF) et identiques sur tous les documents
    check_2 = Column(Boolean)  # Tous les biens-fonds concernés existent au registre foncier (d’après l’extrait RF), sinon ajouter une observation concernant l’ordre de dépôt des dossiers au RF
    check_3 = Column(Boolean)  # Vérifier le bien-fondé des servitudes ainsi que leur faisabilité
    check_4 = Column(Boolean)  # Sommes des surfaces de l’état descriptif
    check_5 = Column(Boolean)  # Les surfaces « ancien état » de la balance correspondent aux surfaces RF
    check_6 = Column(Boolean)  # Sommes des surfaces de la balance
    check_7 = Column(Boolean)  # Les éventuelles différences de m2 sont bien expliquées (a priori, pas de correction des surfaces des nouveaux biens-fonds)
    check_8 = Column(Boolean)  # Les provenances sont cohérentes
    check_9 = Column(Boolean)  # La surface des DDP ne change pas entre l’ancien état et le nouvel état, sinon mettre un commentaire concernant le changement de surface du DDP
    check_10 = Column(Boolean)  # BB a inscrit le montant pour le report des servitudes dans le fichier excel
    check_11 = Column(Boolean)  # Les titres sont cohérents sur tous les documents
    check_12 = Column(Boolean)  # Le dossier respecte les indications du SCAT / SAGR / SENE
    check_13 = Column(Boolean)  # BB a pris en compte les indications du SCAT / SAGR / SENE
    check_14 = Column(Boolean)  # Chaque nouveau BF ait un accès au DP
    check_15 = Column(Boolean)  # Nom du cadastre et n° de bien-fonds corrects (cf extrait RF) et identiques sur tous les documents
    check_16 = Column(Boolean)  # Les titres sont cohérents sur tous les documents
    check_17 = Column(Boolean)  # Cohérence des provenances
    check_18 = Column(Boolean)  # Nombre de documents: « fait en x plans, x désignations et x formules de report des servitude »
    check_19 = Column(Boolean)  # Tampon(s) et date(s) sur la dernière feuille
    check_20 = Column(Boolean)  # Mention « sans frais » indiquée le cas échéant (surtout changement dans ses natures)
    check_21 = Column(Boolean)  # Le n° du BF est visible sur le plan
    check_22 = Column(Boolean)  # Tampon(s) et date(s)
    check_23 = Column(Boolean)  # Titre de la facture
    check_24 = Column(Boolean)  # Quantité et désignation (n° BF + cadastre) des articles facturés
    check_25 = Column(Boolean)  # Prix unitaire des articles facturés (cf fichier excel)
    check_26 = Column(Boolean)  # Si le destinataire de la facture est différent de celui des documents, vérifier que l’enveloppe contenant les documents porte la bonne adresse et qu’il y a 2 enveloppes
    check_27 = Column(Boolean)  # Lettre A sur l’enveloppe (quand pour acte notarié)
    check_28 = Column(Boolean)  # Présence de la lettre d’information à propos de la cadastration d’office
    check_29 = Column(Boolean)  # Eléments saisis manuellement (cf exemples)
    check_30 = Column(Boolean)  # Eléments issus d’Infolica (cf exemples)
    check_31 = Column(Boolean)  # Paragraphes spécifiques si une PPE et constituée sur le fond de base ou si une mention de « Constitution de PPE avant la construction du bâtiment » figure
    check_32 = Column(Boolean)  # Eléments saisis manuellement (cf exemples)
    check_33 = Column(Boolean)  # Chaque bâtiment a un numéro
    check_34 = Column(Boolean)  # Vérifier que le nom du propriétaire est entier
    check_35 = Column(Boolean)  # La surface du bien-fonds est la même que celle inscrite au RF
    check_36 = Column(Boolean)  # Vérifier les sommes des surfaces de l’état descriptif
    check_37 = Column(Boolean)  # Chaque bâtiment a un numéro
    check_38 = Column(Boolean)  # Pertinence de la désignation de bâtiment
    check_39 = Column(Boolean)  # Phrase « DUPLICATA du plan du … »
    check_40 = Column(Boolean)  # Phrase « DUPLICATA du plan du … »
    check_41 = Column(Boolean)  # Contrôle de l’indication « Visa » ou « Modification »
    check_42 = Column(Boolean)  # Contrôle de l’indication « Visa » ou « Modification »
    check_43 = Column(Boolean)  # contrôler si la servitude telle qu’elle est prévue est pertinente et possible. Il est possible qu’il faille diviser les géométries des servitudes pour représenter les différentes utilisations.
    check_44 = Column(Boolean)  # Le nombre de points est le même que sur le plan
    check_45 = Column(Boolean)  # Le montant est correct (~300.- par PL)
    check_46 = Column(Boolean)  # Le nombre de points est le même que sur le plan
    check_47 = Column(Boolean)  # Le montant est correct (~ 380.- par PFP)
    remarque = Column(Text)



class NumeroType(Base):
    __tablename__ = 'numero_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger)
    
    
class NumeroEtat(Base):
    __tablename__ = 'numero_etat'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Numero(Base):
    __tablename__ = 'numero'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cadastre_id = Column(BigInteger, ForeignKey(Cadastre.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(NumeroType.id), nullable=False)
    numero = Column(BigInteger, nullable=False)
    suffixe = Column(Text)
    etat_id = Column(BigInteger, ForeignKey(NumeroEtat.id), nullable=False)
    # plan_id = Column(BigInteger, ForeignKey(Plan.id))

    UniqueConstraint(cadastre_id, type_id, numero)


class ReservationNumerosMO(Base):
    __tablename__ = 'reservation_numeros'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    cadastre_id = Column(BigInteger, ForeignKey(Cadastre.id), nullable=False)
    plan_id = Column(Text, ForeignKey(Plan.idobj))
    type_id = Column(BigInteger, ForeignKey(NumeroType.id), nullable=False)
    numero_de = Column(BigInteger)
    numero_a = Column(BigInteger)
    date = Column(Date, default=datetime.datetime.utcnow)
    remarque = Column(Text)
    operateur_id = Column(BigInteger, ForeignKey(Operateur.id), nullable=False)


class NumeroEtatHisto(Base):
    __tablename__ = 'numero_etat_histo'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    numero_id = Column(BigInteger, ForeignKey(Numero.id), nullable=False)
    numero_etat_id = Column(BigInteger, ForeignKey(
        NumeroEtat.id), nullable=False)
    date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class NumeroDiffere(Base):
    __tablename__ = 'numero_differe'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    numero_id = Column(BigInteger, ForeignKey(Numero.id), nullable=False)
    date_entree = Column(
        Date, default=datetime.datetime.utcnow, nullable=False)
    date_sortie = Column(Date)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id))


class NumeroRelationType(Base):
    __tablename__ = 'numero_relation_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class NumeroRelation(Base):
    __tablename__ = 'numero_relation'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    numero_id_base = Column(Integer, ForeignKey(Numero.id), nullable=False)
    numero_id_associe = Column(Integer, ForeignKey(Numero.id), nullable=False)
    relation_type_id = Column(BigInteger, ForeignKey(
        NumeroRelationType.id), nullable=False)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id))


# class NumeroPlan(Base):
#     __tablename__ = 'numero_plan'
#     __table_args__ = {'schema': 'infolica'}
#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     numero_id = Column(BigInteger, ForeignKey(Numero.id), nullable=False)
#     plan_id = Column(BigInteger, ForeignKey(Plan.id), nullable=False)


class AffaireNumeroType(Base):
    __tablename__ = 'affaire_numero_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class AffaireNumero(Base):
    __tablename__ = 'affaire_numero'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    numero_id = Column(BigInteger, ForeignKey(Numero.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(AffaireNumeroType.id))  # , nullable=False)
    actif = Column(Boolean, default=True, nullable=False)
    affaire_destination_id = Column(BigInteger, ForeignKey(Affaire.id))


class Service(Base):
    __tablename__ = 'service'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service = Column(Text, nullable=False)
    abreviation = Column(Text, nullable=False)
    titre = Column(Text)
    nom = Column(Text)
    prenom = Column(Text)
    adresse = Column(Text)
    case_postale = Column(Text)
    npa = Column(Text)
    localite = Column(Text)
    telephone = Column(Text)
    mail = Column(Text)
    ordre = Column(BigInteger)


class PreavisType(Base):
    __tablename__ = 'preavis_type'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Preavis(Base):
    __tablename__ = 'preavis'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    affaire_id = Column(BigInteger, ForeignKey(Affaire.id), nullable=False)
    service_id = Column(BigInteger, ForeignKey(Service.id), nullable=False)
    preavis_type_id = Column(BigInteger, ForeignKey(PreavisType.id))
    date_demande = Column(
        Date, default=datetime.datetime.utcnow, nullable=False)
    date_reponse = Column(Date)
    remarque = Column(Text)


# class RemarquePreavis(Base):  # currently not used, replaced by attribute Remarque in table Preavis
#     __tablename__ = 'remarque_preavis'
#     __table_args__ = {'schema': 'infolica'}
#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     preavis_id = Column(BigInteger, ForeignKey(Preavis.id), nullable=False)
#     remarque = Column(Text, nullable=False)
#     date = Column(Date, default=datetime.datetime.utcnow, nullable=False)


class Fonction(Base):
    __tablename__ = 'fonction'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)


class FonctionRole(Base):
    __tablename__ = 'fonction_role'
    __table_args__ = {'schema': 'infolica'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fonction_id = Column(BigInteger, ForeignKey(Fonction.id), nullable=False)
    role_id = Column(BigInteger, ForeignKey(Role.id), nullable=False)


class GeosBalance(Base):
    __tablename__ = 'geos_balance'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    idobj = Column(String(40), primary_key=True)
    base = Column(String(50))
    numero_new = Column(String(50))
    cad_new = Column(Integer)
    parcel_new = Column(String(20))
    superficie_new = Column(Integer)
    numero_old = Column(String(50))
    cad_old = Column(Integer)
    parcel_old = Column(String(20))
    superficie_old = Column(Integer)
    superficie_partie = Column(Integer)
    mutation = Column(String(50))
    mutation_desc = Column(String(200))
    egrid_old = Column(String(50))
    gid_geom_new = Column(String(50))
    gid_numero_new = Column(String(50))
    gid_geom_old = Column(String(50))
    gid_numero_old = Column(String(50))
    gid_mutation = Column(String(50))
    geom = Column(Geometry('POINT'))


# ======================== VUES ========================
# Ajouter l'information 'info': dict(is_view=True) aux vues 
# pour qu'elles ne soient pas prises en compte dans les migrations par Alembic


class VNumeros(Base):
    __tablename__ = 'v_numeros'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    cadastre = Column(Text)
    cadastre_id = Column(BigInteger)
    numero = Column(BigInteger)
    suffixe = Column(Text)
    etat = Column(Text)
    etat_id = Column(BigInteger)
    type_numero = Column(Text)
    type_numero_id = Column(BigInteger)
    diff_id = Column(Date)
    diff_entree = Column(Date)
    diff_sortie = Column(Date)
    diff_affaire_id = Column(BigInteger)
    # plan_id = Column(BigInteger)


class VNumerosAffaires(Base):
    __tablename__ = 'v_numeros_affaires'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    numero_id = Column(BigInteger)
    affaire_id = Column(BigInteger)
    affaire_numero_type_id = Column(BigInteger)
    affaire_numero_actif = Column(Boolean)
    affaire_destination_id = Column(BigInteger)
    affaire_nom = Column(Text)
    affaire_type = Column(Text)
    affaire_date = Column(Date)
    affaire_information = Column(Text)
    numero_cadastre = Column(Text)
    numero_cadastre_id = Column(BigInteger)
    numero_type = Column(Text)
    numero_type_id = Column(BigInteger)
    numero = Column(BigInteger)
    numero_suffixe = Column(Text)
    numero_etat = Column(Text)
    numero_etat_id = Column(BigInteger)
    numero_diff_id = Column(Date)
    numero_diff_entree = Column(Date)
    numero_diff_sortie = Column(Date)
    numero_plan_id = Column(BigInteger)
    numero_base_id = Column(BigInteger)
    numero_base_type = Column(Text)
    numero_base = Column(BigInteger)
    numero_base_suffixe = Column(Text)
    numero_base_etat = Column(Text)
    affaire_numero_type = Column(Text)


class VAffaire(Base):
    __tablename__ = 'v_affaires'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    no_access = Column(Text)
    nom = Column(Text)
    client_commande_id = Column(BigInteger)
    client_commande_entreprise = Column(Text)
    client_commande_titre = Column(Text)
    client_commande_nom = Column(Text)
    client_commande_prenom = Column(Text)
    client_commande_complement = Column(Text)
    client_commande_adresse = Column(Text)
    client_commande_co = Column(Text)
    client_commande_npa = Column(Text)
    client_commande_localite = Column(Text)
    client_commande_tel_fixe = Column(Text)
    client_commande_tel_portable = Column(Text)
    client_commande_fax = Column(Text)
    client_commande_mail = Column(Text)
    client_commande_no_sap = Column(Text)
    client_commande_no_bdp_bdee = Column(Text)
    client_envoi_id = Column(BigInteger)
    client_envoi_entreprise = Column(Text)
    client_envoi_titre = Column(Text)
    client_envoi_nom = Column(Text)
    client_envoi_prenom = Column(Text)
    client_envoi_complement = Column(Text)
    client_envoi_co = Column(Text)
    client_envoi_adresse = Column(Text)
    client_envoi_npa = Column(Text)
    client_envoi_localite = Column(Text)
    client_envoi_tel_fixe = Column(Text)
    client_envoi_tel_portable = Column(Text)
    client_envoi_fax = Column(Text)
    client_envoi_mail = Column(Text)
    client_envoi_no_sap = Column(Text)
    client_envoi_no_bdp_bdee = Column(Text)
    responsable_id = Column(BigInteger)
    responsable_nom = Column(Text)
    responsable_prenom = Column(Text)
    technicien_id = Column(BigInteger)
    technicien_nom = Column(Text)
    technicien_prenom = Column(Text)
    type_affaire = Column(Text)
    cadastre = Column(Text)
    information = Column(Text)
    date_ouverture = Column(Date)
    date_validation = Column(Date)
    date_envoi = Column(Date)
    date_cloture = Column(Date)
    localisation_e = Column(Float)
    localisation_n = Column(Float)
    cadastre_id = Column(BigInteger)
    type_id = Column(BigInteger)
    vref = Column(Text)
    chemin = Column(Text)
    reservation_numeros_types_id = Column(ARRAY(BigInteger))
    modif_affaire_type_id_vers = Column(ARRAY(BigInteger))
    modification_type_id = Column(BigInteger)
    modification_type = Column(Text)
    modification_affaire_id_mere = Column(BigInteger)
    preavis_scat_date_demande = Column(Date)
    preavis_scat_date_reponse = Column(Date)
    preavis_sagr_date_demande = Column(Date)
    preavis_sagr_date_reponse = Column(Date)
    preavis_sene_date_demande = Column(Date)
    preavis_sene_date_reponse = Column(Date)
    preavis_rf_date_demande = Column(Date)
    preavis_rf_date_reponse = Column(Date)
    etape_id = Column(BigInteger)
    etape = Column(Text)
    etape_date = Column(Date)
    etape_remarque = Column(Text)
    abandon = Column(Boolean)


class VEnvois(Base):
    __tablename__ = 'v_envois'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    affaire_id = Column(BigInteger)
    affaire_nom = Column(Text)
    client_id = Column(BigInteger)
    client_entreprise = Column(Text)
    client_titre = Column(Text)
    client_nom = Column(Text)
    client_prenom = Column(Text)
    client_complement = Column(Text)
    envoi_type_id = Column(BigInteger)
    envoi_type = Column(Text)
    date = Column(Date)


class VEtapesAffaires(Base):
    __tablename__ = 'v_etapes_affaires'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    affaire_id = Column(BigInteger, primary_key=True)
    affaire_nom = Column(Text)
    etape = Column(Text, primary_key=True)
    date_etape = Column(Date, primary_key=True)
    affaire_liee_id = Column(BigInteger)
    affaire_liee_nom = Column(Text)
    service_nom = Column(Text, primary_key=True)
    remarque = Column(Text)


class VAffairesPreavis(Base):
    __tablename__ = 'v_affaires_preavis'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    affaire_id = Column(BigInteger)
    service = Column(Text)
    service_id = Column(BigInteger)
    preavis = Column(Text)
    preavis_type_id = Column(BigInteger)
    date_demande = Column(Date)
    date_reponse = Column(Date)
    remarque = Column(Text)
    

class VTableauBord(Base):
    __tablename__ = 'v_tableau_de_bord'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    affaire_id = Column(BigInteger, primary_key=True)
    affaire_nom = Column(Text)
    delai = Column(Integer)
    client_entreprise = Column(Text)
    client_titre = Column(Text)
    client_nom = Column(Text)
    client_prenom = Column(Text)
    affaire_type = Column(Text)
    chef_nom = Column(Text)
    chef_prenom = Column(Text)
    technicien_nom = Column(Text)
    technicien_prenom = Column(Text)
    information = Column(Text)
    cadastre = Column(Text)
    etape = Column(Text)


class VEmolumentsFactures(Base):
    __tablename__ = 'v_emoluments_factures'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    facture_id = Column(BigInteger, primary_key=True)
    domaine = Column(Text)
    categorie = Column(Text)
    sous_categorie = Column(Text)
    nom = Column(Text, primary_key=True)
    unite = Column(Text)
    prix_unitaire = Column(Text)
    nombre = Column(Integer, primary_key=True)
    facteur_correctif = Column(Float)
    batiment = Column(Text, primary_key=True)
    montant = Column(Float)


class VNumerosRelations(Base):
    __tablename__ = 'v_numeros_relations'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    affaire_id = Column(BigInteger)
    numero_relation_id = Column(BigInteger, primary_key=True)
    numero_base_id = Column(BigInteger)
    numero_base_cadastre_id = Column(BigInteger)
    numero_base_cadastre = Column(Text)
    numero_base_type_id = Column(BigInteger)
    numero_base_type = Column(Text)
    numero_base = Column(BigInteger)
    numero_base_suffixe = Column(Text)
    numero_base_etat_id = Column(BigInteger)
    numero_base_etat = Column(Text)
    numero_base_plan_id = Column(BigInteger)
    numero_associe_id = Column(BigInteger)
    numero_associe_cadastre_id = Column(BigInteger)
    numero_associe_cadastre = Column(Text)
    numero_associe_type_id = Column(BigInteger)
    numero_associe_type = Column(Text)
    numero_associe = Column(BigInteger)
    numero_associe_suffixe = Column(Text)
    numero_associe_etat_id = Column(BigInteger)
    numero_associe_etat = Column(Text)
    numero_associe_plan_id = Column(BigInteger)
    numero_relation_type_id = Column(BigInteger)
    numero_relation_type = Column(Text)


class VDocumentsAffaires(Base):
    __tablename__ = 'v_documents_affaires'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    nom = Column(Text)
    chemin = Column(Text)
    affaire_id = Column(BigInteger)
    type_id = Column(BigInteger)
    type_doc = Column(Text)


class VFactures(Base):
    __tablename__ = 'v_factures'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    affaire_id = Column(BigInteger)
    affaire_vref = Column(Text)
    sap = Column(Text)
    client_id = Column(BigInteger)
    client_entreprise = Column(Text)
    client_titre = Column(Text)
    client_nom = Column(Text)
    client_prenom = Column(Text)
    client_co = Column(Text)
    client_adresse = Column(Text)
    client_npa = Column(Text)
    client_localite = Column(Text)
    client_case_postale = Column(Text)
    client_tel_fixe = Column(Text)
    client_fax = Column(Text)
    client_tel_portable = Column(Text)
    client_mail = Column(Text)
    client_entree = Column(Date)
    client_sortie = Column(Date)
    client_no_sap = Column(Text)
    client_no_bdp_bdee = Column(Text)
    client_complement = Column(Text)
    client_premiere_ligne = Column(Text)
    client_co_id = Column(BigInteger)
    client_co_entreprise = Column(Text)
    client_co_titre = Column(Text)
    client_co_nom = Column(Text)
    client_co_prenom = Column(Text)
    client_co_co = Column(Text)
    client_co_adresse = Column(Text)
    client_co_npa = Column(Text)
    client_co_localite = Column(Text)
    client_co_case_postale = Column(Text)
    client_co_tel_fixe = Column(Text)
    client_co_fax = Column(Text)
    client_co_tel_portable = Column(Text)
    client_co_mail = Column(Text)
    client_co_entree = Column(Date)
    client_co_sortie = Column(Date)
    client_co_no_sap = Column(Text)
    client_co_no_bdp_bdee = Column(Text)
    indice_application_mo = Column(Float)
    indice_tva = Column(Float)
    montant_mo = Column(Float)
    montant_mat_diff = Column(Float)
    montant_rf = Column(Float)
    montant_tva = Column(Float)
    montant_total = Column(Float)
    date = Column(Date)
    remarque = Column(Text)
    numeros = Column(ARRAY(BigInteger))


class VReservationNumerosMO(Base):
    __tablename__ = "v_reservation_numeros_mo"
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    id = Column(BigInteger, primary_key=True)
    affaire_id = Column(BigInteger)
    cadastre_id = Column(BigInteger)
    cadastre = Column(Text)
    type_id = Column(BigInteger)
    type_numero = Column(Text)
    numero_de = Column(BigInteger)
    numero_a = Column(BigInteger)
    date = Column(Date)
    remarque = Column(Text)
    operateur_id = Column(BigInteger)
    operateur_nom = Column(Text)
    operateur_prenom = Column(Text)
    plan_id = Column(String(length=40))
    plan_id2 = Column(String(length=20))
    plan_no = Column(String(length=5))
    plan_type = Column(String(length=15))
    plan_datemev = Column(String(length=25))
    plan_statut = Column(String(length=40))
    plan_echelle = Column(Integer)
    plan_idorplan = Column(String(length=40))
    plan_idrepplan = Column(String(length=40))
    plan_base = Column(String(length=50))

class VPlan(Base):
    __tablename__ = 'v_plans_mo'
    __table_args__ = {'schema': 'infolica',
                      'info': dict(is_view=True)}
    idobj = Column(Text, primary_key=True)
    id_obj2 = Column(Text)
    cadastre_id = Column(BigInteger)
    cadastre = Column(Text)
    planno = Column(Integer)
    typlan = Column(Text)
    datmev = Column(Text)
    statut = Column(Text)
    echell = Column(Integer)
    idborplan = Column(Text)
    idrepplan = Column(Text)
    base = Column(Text)


# ========================================================
#               TELETRAVAIL COVID-19
# ========================================================

class Etape_tele(Base):
    __tablename__ = "etape"
    __table_args__ = {'schema': 'teletravail'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger)

class AffaireType_tele(Base):
    __tablename__ = "affaire_type"
    __table_args__ = {'schema': 'teletravail'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    ordre = Column(BigInteger, nullable=False)
    logique_etapes = Column(ARRAY(BigInteger))

class Affaire_tele(Base):
    __tablename__ = "affaire"
    __table_args__ = {'schema': 'teletravail'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_id = Column(BigInteger, ForeignKey(AffaireType_tele.id), nullable=False)
    nom = Column(Text, nullable=False)
    actuelle_etape_id = Column(BigInteger, ForeignKey(Etape_tele.id), nullable=False)
    datetime_ouverture = Column(DateTime, nullable=False)
    datetime_cloture = Column(DateTime)
    remarque = Column(Text)

class SuiviAffaire_tele(Base):
    __tablename__ = "suivi_affaire"
    __table_args__ = {'schema': 'teletravail'}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    operateur_id = Column(BigInteger, ForeignKey(Operateur.id), nullable=False)
    affaire_id = Column(BigInteger, ForeignKey(Affaire_tele.id), nullable=False)
    datetime = Column(DateTime, nullable=False)
    etape_id = Column(BigInteger, ForeignKey(Etape_tele.id), nullable=False)
    remarque = Column(Text)

class VSuiviAffaire_tele(Base):
    __tablename__ = "v_suivi_affaires"
    __table_args__ = {'schema': 'teletravail',
                      'info': dict(is_view=True)}
    suivi_affaire_id = Column(BigInteger, primary_key=True)
    operateur_id = Column(BigInteger)
    operateur_nom = Column(Text)
    operateur_prenom = Column(Text)
    affaire_id = Column(BigInteger)
    affaire_nom = Column(Text)
    affaire_type_id = Column(BigInteger)
    affaire_type = Column(Text)
    affaire_type_logique_etapes = Column(ARRAY(BigInteger))
    datetime = Column(DateTime)
    etape_id = Column(BigInteger)
    etape = Column(Text)
    remarque = Column(Text)

class VAffaire_tele(Base):
    __tablename__ = "v_affaires"
    __table_args__ = {'schema': 'teletravail',
                      'info': dict(is_view=True)}
    affaire_id = Column(BigInteger, primary_key=True)
    affaire_nom = Column(Text)
    affaire_type_id = Column(BigInteger)
    affaire_type = Column(Text)
    affaire_type_logique_etapes = Column(ARRAY(BigInteger))
    etape_id = Column(BigInteger)
    etape = Column(Text)
    affaire_remarque = Column(Text)
    datetime_ouverture = Column(DateTime)
    datetime_cloture = Column(DateTime)