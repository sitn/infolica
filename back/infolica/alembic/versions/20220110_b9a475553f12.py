"""nouveau controle geometre

Revision ID: b9a475553f12
Revises: 562661974c46
Create Date: 2022-01-10 16:58:54.481254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9a475553f12'
down_revision = '562661974c46'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('controle_geometre', 'controle_geometre_old', schema='infolica')
    op.execute("ALTER TABLE controle_geometre_old RENAME CONSTRAINT fk_controle_geometre_affaire_id_affaire TO fk_controle_geometre_old_affaire_id_affaire;")
    op.execute("ALTER TABLE controle_geometre_old RENAME CONSTRAINT fk_controle_geometre_operateur_id_operateur TO fk_controle_geometre_old_operateur_id_operateur;")
    op.execute("ALTER TABLE controle_geometre_old RENAME CONSTRAINT pk_controle_geometre TO pk_controle_geometre_old;")
    
    op.create_table('controle_geometre',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('affaire_id', sa.BigInteger(), nullable=False),
    sa.Column('operateur_id', sa.BigInteger(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('remarque', sa.Text(), nullable=True),
    sa.Column('info_gen_adresses', sa.Integer(), nullable=True),
    sa.Column('info_gen_referencement_affaire', sa.Integer(), nullable=True),
    sa.Column('info_gen_dossier_complet', sa.Integer(), nullable=True),
    sa.Column('info_gen_numeros_recuperes', sa.Integer(), nullable=True),
    sa.Column('asp_jur_respect_preavis', sa.Integer(), nullable=True),
    sa.Column('asp_jur_bf_existent_rf', sa.Integer(), nullable=True),
    sa.Column('asp_jur_no_reserves_no_utilises', sa.Integer(), nullable=True),
    sa.Column('asp_jur_acces_dp', sa.Integer(), nullable=True),
    sa.Column('asp_jur_servitudes', sa.Integer(), nullable=True),
    sa.Column('asp_jur_no_etat_juridique_bf_base', sa.Integer(), nullable=True),
    sa.Column('asp_jur_plan_sit_plan_etage', sa.Integer(), nullable=True),
    sa.Column('asp_jur_plan_mention_partiellement', sa.Integer(), nullable=True),
    sa.Column('asp_jur_nb_doc_legende', sa.Integer(), nullable=True),
    sa.Column('asp_jur_tampons_corrects', sa.Integer(), nullable=True),
    sa.Column('fact_repartition_destinataires', sa.Integer(), nullable=True),
    sa.Column('fact_montant_servitudes', sa.Integer(), nullable=True),
    sa.Column('fact_no_affaire', sa.Integer(), nullable=True),
    sa.Column('fact_libelles', sa.Integer(), nullable=True),
    sa.Column('fact_prix_unitaire_prix_total', sa.Integer(), nullable=True),
    sa.Column('fact_prix_pfp', sa.Integer(), nullable=True),
    sa.Column('fact_prix_pl', sa.Integer(), nullable=True),
    sa.Column('fact_destinataires_enveloppes_coherents', sa.Integer(), nullable=True),
    sa.Column('fact_lettre_a', sa.Integer(), nullable=True),
    sa.Column('fact_remarque_devis_facture', sa.Integer(), nullable=True),
    sa.Column('fact_contenu_emolument', sa.Integer(), nullable=True),
    sa.Column('coherence_doc_cadastre_bf_titre', sa.Integer(), nullable=True),
    sa.Column('coherence_doc_reunion_bat_egid', sa.Integer(), nullable=True),
    sa.Column('ctrl_juridique_coherence_doc_cadastre_bf_titre', sa.Integer(), nullable=True),
    sa.Column('coherence_doc_nb_pts_factues', sa.Integer(), nullable=True),
    sa.Column('coherence_doc_date', sa.Integer(), nullable=True),
    sa.Column('coherence_doc_bat_num', sa.Integer(), nullable=True),
    sa.Column('balance_avancement_saisie_servitudes', sa.Integer(), nullable=True),
    sa.Column('balance_surfaces_ancien_rf', sa.Integer(), nullable=True),
    sa.Column('balance_somme_surfaces', sa.Integer(), nullable=True),
    sa.Column('balance_surface_bf_base_creation_ddp', sa.Integer(), nullable=True),
    sa.Column('balance_surface_ddp', sa.Integer(), nullable=True),
    sa.Column('etat_desc_provenances', sa.Integer(), nullable=True),
    sa.Column('etat_desc_surface_totale_bf', sa.Integer(), nullable=True),
    sa.Column('etat_desc_somme_surfaces_natures', sa.Integer(), nullable=True),
    sa.Column('etat_desc_nom_rue', sa.Integer(), nullable=True),
    sa.Column('mat_diff_infos', sa.Integer(), nullable=True),
    sa.Column('courrier_destinataires_enveloppes_coherents', sa.Integer(), nullable=True),
    sa.Column('courrier_lettre_a', sa.Integer(), nullable=True),
    sa.Column('des_provenances', sa.Integer(), nullable=True),
    sa.Column('des_surface_totale_bf', sa.Integer(), nullable=True),
    sa.Column('des_somme_surfaces_natures', sa.Integer(), nullable=True),
    sa.Column('des_nb_documents', sa.Integer(), nullable=True),
    sa.Column('des_tampon_geom_date', sa.Integer(), nullable=True),
    sa.Column('des_tampon_duplicata_date', sa.Integer(), nullable=True),
    sa.Column('des_tampon_copie_geom_date', sa.Integer(), nullable=True),
    sa.Column('des_mention_sans_frais', sa.Integer(), nullable=True),
    sa.Column('des_nom_proprietaire', sa.Integer(), nullable=True),
    sa.Column('des_surface_bf_mo_rf', sa.Integer(), nullable=True),
    sa.Column('des_somme_surfaces_ed', sa.Integer(), nullable=True),
    sa.Column('des_designation_bat', sa.Integer(), nullable=True),
    sa.Column('des_tampon_geom_date_initiale', sa.Integer(), nullable=True),
    sa.Column('des_tampon_modifie_date', sa.Integer(), nullable=True),
    sa.Column('des_tampon_vise_date', sa.Integer(), nullable=True),
    sa.Column('plan_no_bf', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_geom_date', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_duplicata_date', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_copie_geom_date', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_geom_date_initiale', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_modifie_date', sa.Integer(), nullable=True),
    sa.Column('plan_servitudes', sa.Integer(), nullable=True),
    sa.Column('plan_tampon_vise_date', sa.Integer(), nullable=True),
    sa.Column('lettres_no_affaire', sa.Integer(), nullable=True),
    sa.Column('lettres_saisie_manuelle', sa.Integer(), nullable=True),
    sa.Column('lettres_paragraphe_ppe', sa.Integer(), nullable=True),
    sa.Column('lettres_lettre_cad_office', sa.Integer(), nullable=True),
    sa.Column('req_saisie_manuelle', sa.Integer(), nullable=True),
    sa.Column('devis_fact_remarques', sa.Integer(), nullable=True),
    sa.Column('devis_fact_no_emolument', sa.Integer(), nullable=True),
    sa.Column('devis_fact_montant_rf', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['affaire_id'], ['infolica.affaire.id'], name=op.f('fk_controle_geometre_affaire_id_affaire')),
    sa.ForeignKeyConstraint(['operateur_id'], ['infolica.operateur.id'], name=op.f('fk_controle_geometre_operateur_id_operateur')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_controle_geometre')),
    schema='infolica'
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('controle_geometre', schema='infolica')

    op.rename_table('controle_geometre_old', 'controle_geometre', schema='infolica')

    op.execute("ALTER TABLE controle_geometre RENAME CONSTRAINT fk_controle_geometre_old_affaire_id_affaire TO fk_controle_geometre_affaire_id_affaire;")
    op.execute("ALTER TABLE controle_geometre RENAME CONSTRAINT fk_controle_geometre_old_operateur_id_operateur TO fk_controle_geometre_operateur_id_operateur;")
    op.execute("ALTER TABLE controle_geometre RENAME CONSTRAINT pk_controle_geometre_old TO pk_controle_geometre;")
    # ### end Alembic commands ###