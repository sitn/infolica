"""add plan in reservation_numeros_mo

Revision ID: aefafb13d2ce
Revises: d36235de99bc
Create Date: 2021-03-16 11:41:34.495793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aefafb13d2ce'
down_revision = 'd36235de99bc'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_affaire_technicien_id_operateur', 'affaire', type_='foreignkey')
    op.drop_constraint('fk_affaire_type_id_affaire_type', 'affaire', type_='foreignkey')
    op.drop_constraint('fk_affaire_cadastre_id_cadastre', 'affaire', type_='foreignkey')
    op.drop_constraint('fk_affaire_client_envoi_id_client', 'affaire', type_='foreignkey')
    op.drop_constraint('fk_affaire_client_commande_id_client', 'affaire', type_='foreignkey')
    op.create_foreign_key(op.f('fk_affaire_cadastre_id_cadastre'), 'affaire', 'cadastre', ['cadastre_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_client_commande_id_client'), 'affaire', 'client', ['client_commande_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_type_id_affaire_type'), 'affaire', 'affaire_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_technicien_id_operateur'), 'affaire', 'operateur', ['technicien_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_client_envoi_id_client'), 'affaire', 'client', ['client_envoi_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_affaire_etape_etape_id_affaire_etape_index', 'affaire_etape', type_='foreignkey')
    op.drop_constraint('fk_affaire_etape_operateur_id_operateur', 'affaire_etape', type_='foreignkey')
    op.drop_constraint('fk_affaire_etape_affaire_id_affaire', 'affaire_etape', type_='foreignkey')
    op.create_foreign_key(op.f('fk_affaire_etape_operateur_id_operateur'), 'affaire_etape', 'operateur', ['operateur_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_etape_etape_id_affaire_etape_index'), 'affaire_etape', 'affaire_etape_index', ['etape_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_etape_affaire_id_affaire'), 'affaire_etape', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_affaire_numero_affaire_destination_id_affaire', 'affaire_numero', type_='foreignkey')
    op.drop_constraint('fk_affaire_numero_numero_id_numero', 'affaire_numero', type_='foreignkey')
    op.drop_constraint('fk_affaire_numero_affaire_id_affaire', 'affaire_numero', type_='foreignkey')
    op.drop_constraint('fk_affaire_numero_type_id_affaire_numero_type', 'affaire_numero', type_='foreignkey')
    op.create_foreign_key(op.f('fk_affaire_numero_affaire_id_affaire'), 'affaire_numero', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_numero_type_id_affaire_numero_type'), 'affaire_numero', 'affaire_numero_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_numero_affaire_destination_id_affaire'), 'affaire_numero', 'affaire', ['affaire_destination_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_affaire_numero_numero_id_numero'), 'affaire_numero', 'numero', ['numero_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_client_type_client_client_type', 'client', type_='foreignkey')
    op.create_foreign_key(op.f('fk_client_type_client_client_type'), 'client', 'client_type', ['type_client'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_client_moral_personne_client_id_client', 'client_moral_personne', type_='foreignkey')
    op.create_foreign_key(op.f('fk_client_moral_personne_client_id_client'), 'client_moral_personne', 'client', ['client_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_controle_geometre_affaire_id_affaire', 'controle_geometre', type_='foreignkey')
    op.drop_constraint('fk_controle_geometre_operateur_id_operateur', 'controle_geometre', type_='foreignkey')
    op.create_foreign_key(op.f('fk_controle_geometre_operateur_id_operateur'), 'controle_geometre', 'operateur', ['operateur_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_controle_geometre_affaire_id_affaire'), 'controle_geometre', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_controle_mutation_affaire_id_affaire', 'controle_mutation', type_='foreignkey')
    op.drop_constraint('fk_controle_mutation_visa_operateur', 'controle_mutation', type_='foreignkey')
    op.create_foreign_key(op.f('fk_controle_mutation_affaire_id_affaire'), 'controle_mutation', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_controle_mutation_visa_operateur'), 'controle_mutation', 'operateur', ['visa'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_controle_ppe_affaire_id_affaire', 'controle_ppe', type_='foreignkey')
    op.drop_constraint('fk_controle_ppe_operateur_id_operateur', 'controle_ppe', type_='foreignkey')
    op.create_foreign_key(op.f('fk_controle_ppe_affaire_id_affaire'), 'controle_ppe', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_controle_ppe_operateur_id_operateur'), 'controle_ppe', 'operateur', ['operateur_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_emolument_facture_emolument_id_tableau_emoluments', 'emolument_facture', type_='foreignkey')
    op.drop_constraint('fk_emolument_facture_facture_id_facture', 'emolument_facture', type_='foreignkey')
    op.create_foreign_key(op.f('fk_emolument_facture_facture_id_facture'), 'emolument_facture', 'facture', ['facture_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_emolument_facture_emolument_id_tableau_emoluments'), 'emolument_facture', 'tableau_emoluments', ['emolument_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_etape_mailer_etape_id_affaire_etape_index', 'etape_mailer', type_='foreignkey')
    op.drop_constraint('fk_etape_mailer_operateur_id_operateur', 'etape_mailer', type_='foreignkey')
    op.create_foreign_key(op.f('fk_etape_mailer_etape_id_affaire_etape_index'), 'etape_mailer', 'affaire_etape_index', ['etape_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_etape_mailer_operateur_id_operateur'), 'etape_mailer', 'operateur', ['operateur_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_facture_affaire_id_affaire', 'facture', type_='foreignkey')
    op.drop_constraint('fk_facture_type_id_facture_type', 'facture', type_='foreignkey')
    op.drop_constraint('fk_facture_client_id_client', 'facture', type_='foreignkey')
    op.drop_constraint('fk_facture_client_co_id_client', 'facture', type_='foreignkey')
    op.create_foreign_key(op.f('fk_facture_type_id_facture_type'), 'facture', 'facture_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_facture_client_co_id_client'), 'facture', 'client', ['client_co_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_facture_affaire_id_affaire'), 'facture', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_facture_client_id_client'), 'facture', 'client', ['client_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_fonction_role_role_id_role', 'fonction_role', type_='foreignkey')
    op.drop_constraint('fk_fonction_role_fonction_id_fonction', 'fonction_role', type_='foreignkey')
    op.create_foreign_key(op.f('fk_fonction_role_role_id_role'), 'fonction_role', 'role', ['role_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_fonction_role_fonction_id_fonction'), 'fonction_role', 'fonction', ['fonction_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_modification_affaire_type_id_modification_affaire_type', 'modification_affaire', type_='foreignkey')
    op.drop_constraint('fk_modification_affaire_affaire_id_mere_affaire', 'modification_affaire', type_='foreignkey')
    op.drop_constraint('fk_modification_affaire_affaire_id_fille_affaire', 'modification_affaire', type_='foreignkey')
    op.create_foreign_key(op.f('fk_modification_affaire_type_id_modification_affaire_type'), 'modification_affaire', 'modification_affaire_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_modification_affaire_affaire_id_mere_affaire'), 'modification_affaire', 'affaire', ['affaire_id_mere'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_modification_affaire_affaire_id_fille_affaire'), 'modification_affaire', 'affaire', ['affaire_id_fille'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_modification_affaire_type_affaire_destination_type_i_65bc', 'modification_affaire_type', type_='foreignkey')
    op.create_foreign_key(op.f('fk_modification_affaire_type_affaire_destination_type_id_affaire_type'), 'modification_affaire_type', 'affaire_type', ['affaire_destination_type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_numero_etat_id_numero_etat', 'numero', type_='foreignkey')
    op.drop_constraint('fk_numero_cadastre_id_cadastre', 'numero', type_='foreignkey')
    op.drop_constraint('fk_numero_type_id_numero_type', 'numero', type_='foreignkey')
    op.create_foreign_key(op.f('fk_numero_cadastre_id_cadastre'), 'numero', 'cadastre', ['cadastre_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_type_id_numero_type'), 'numero', 'numero_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_etat_id_numero_etat'), 'numero', 'numero_etat', ['etat_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_numero_differe_affaire_id_affaire', 'numero_differe', type_='foreignkey')
    op.drop_constraint('fk_numero_differe_numero_id_numero', 'numero_differe', type_='foreignkey')
    op.create_foreign_key(op.f('fk_numero_differe_numero_id_numero'), 'numero_differe', 'numero', ['numero_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_differe_affaire_id_affaire'), 'numero_differe', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_numero_etat_histo_numero_id_numero', 'numero_etat_histo', type_='foreignkey')
    op.drop_constraint('fk_numero_etat_histo_numero_etat_id_numero_etat', 'numero_etat_histo', type_='foreignkey')
    op.create_foreign_key(op.f('fk_numero_etat_histo_numero_id_numero'), 'numero_etat_histo', 'numero', ['numero_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_etat_histo_numero_etat_id_numero_etat'), 'numero_etat_histo', 'numero_etat', ['numero_etat_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_numero_relation_affaire_id_affaire', 'numero_relation', type_='foreignkey')
    op.drop_constraint('fk_numero_relation_relation_type_id_numero_relation_type', 'numero_relation', type_='foreignkey')
    op.drop_constraint('fk_numero_relation_numero_id_base_numero', 'numero_relation', type_='foreignkey')
    op.drop_constraint('fk_numero_relation_numero_id_associe_numero', 'numero_relation', type_='foreignkey')
    op.create_foreign_key(op.f('fk_numero_relation_affaire_id_affaire'), 'numero_relation', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_relation_relation_type_id_numero_relation_type'), 'numero_relation', 'numero_relation_type', ['relation_type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_relation_numero_id_base_numero'), 'numero_relation', 'numero', ['numero_id_base'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_numero_relation_numero_id_associe_numero'), 'numero_relation', 'numero', ['numero_id_associe'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_preavis_affaire_id_affaire', 'preavis', type_='foreignkey')
    op.drop_constraint('fk_preavis_service_id_service', 'preavis', type_='foreignkey')
    op.drop_constraint('fk_preavis_preavis_type_id_preavis_type', 'preavis', type_='foreignkey')
    op.create_foreign_key(op.f('fk_preavis_affaire_id_affaire'), 'preavis', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_preavis_service_id_service'), 'preavis', 'service', ['service_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_preavis_preavis_type_id_preavis_type'), 'preavis', 'preavis_type', ['preavis_type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.add_column('reservation_numeros', sa.Column('plan', sa.Integer(), nullable=True))
    op.drop_constraint('fk_reservation_numeros_affaire_id_affaire', 'reservation_numeros', type_='foreignkey')
    op.drop_constraint('fk_reservation_numeros_cadastre_id_cadastre', 'reservation_numeros', type_='foreignkey')
    op.drop_constraint('fk_reservation_numeros_type_id_numero_type', 'reservation_numeros', type_='foreignkey')
    op.drop_constraint('fk_reservation_numeros_operateur_id_operateur', 'reservation_numeros', type_='foreignkey')
    op.create_foreign_key(op.f('fk_reservation_numeros_operateur_id_operateur'), 'reservation_numeros', 'operateur', ['operateur_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_reservation_numeros_cadastre_id_cadastre'), 'reservation_numeros', 'cadastre', ['cadastre_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_reservation_numeros_affaire_id_affaire'), 'reservation_numeros', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_reservation_numeros_type_id_numero_type'), 'reservation_numeros', 'numero_type', ['type_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.drop_constraint('fk_suivi_mandat_affaire_id_affaire', 'suivi_mandat', type_='foreignkey')
    op.drop_constraint('fk_suivi_mandat_ap_32_operateur', 'suivi_mandat', type_='foreignkey')
    op.drop_constraint('fk_suivi_mandat_av_32_operateur', 'suivi_mandat', type_='foreignkey')
    op.drop_constraint('fk_suivi_mandat_visa_operateur', 'suivi_mandat', type_='foreignkey')
    op.create_foreign_key(op.f('fk_suivi_mandat_ap_32_operateur'), 'suivi_mandat', 'operateur', ['ap_32'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_suivi_mandat_av_32_operateur'), 'suivi_mandat', 'operateur', ['av_32'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_suivi_mandat_visa_operateur'), 'suivi_mandat', 'operateur', ['visa'], ['id'], source_schema='infolica', referent_schema='infolica')
    op.create_foreign_key(op.f('fk_suivi_mandat_affaire_id_affaire'), 'suivi_mandat', 'affaire', ['affaire_id'], ['id'], source_schema='infolica', referent_schema='infolica')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_suivi_mandat_affaire_id_affaire'), 'suivi_mandat', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_suivi_mandat_visa_operateur'), 'suivi_mandat', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_suivi_mandat_av_32_operateur'), 'suivi_mandat', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_suivi_mandat_ap_32_operateur'), 'suivi_mandat', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_suivi_mandat_visa_operateur', 'suivi_mandat', 'operateur', ['visa'], ['id'])
    op.create_foreign_key('fk_suivi_mandat_av_32_operateur', 'suivi_mandat', 'operateur', ['av_32'], ['id'])
    op.create_foreign_key('fk_suivi_mandat_ap_32_operateur', 'suivi_mandat', 'operateur', ['ap_32'], ['id'])
    op.create_foreign_key('fk_suivi_mandat_affaire_id_affaire', 'suivi_mandat', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_reservation_numeros_type_id_numero_type'), 'reservation_numeros', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_reservation_numeros_affaire_id_affaire'), 'reservation_numeros', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_reservation_numeros_cadastre_id_cadastre'), 'reservation_numeros', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_reservation_numeros_operateur_id_operateur'), 'reservation_numeros', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_reservation_numeros_operateur_id_operateur', 'reservation_numeros', 'operateur', ['operateur_id'], ['id'])
    op.create_foreign_key('fk_reservation_numeros_type_id_numero_type', 'reservation_numeros', 'numero_type', ['type_id'], ['id'])
    op.create_foreign_key('fk_reservation_numeros_cadastre_id_cadastre', 'reservation_numeros', 'cadastre', ['cadastre_id'], ['id'])
    op.create_foreign_key('fk_reservation_numeros_affaire_id_affaire', 'reservation_numeros', 'affaire', ['affaire_id'], ['id'])
    op.drop_column('reservation_numeros', 'plan')
    op.drop_constraint(op.f('fk_preavis_preavis_type_id_preavis_type'), 'preavis', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_preavis_service_id_service'), 'preavis', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_preavis_affaire_id_affaire'), 'preavis', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_preavis_preavis_type_id_preavis_type', 'preavis', 'preavis_type', ['preavis_type_id'], ['id'])
    op.create_foreign_key('fk_preavis_service_id_service', 'preavis', 'service', ['service_id'], ['id'])
    op.create_foreign_key('fk_preavis_affaire_id_affaire', 'preavis', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_numero_relation_numero_id_associe_numero'), 'numero_relation', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_relation_numero_id_base_numero'), 'numero_relation', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_relation_relation_type_id_numero_relation_type'), 'numero_relation', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_relation_affaire_id_affaire'), 'numero_relation', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_numero_relation_numero_id_associe_numero', 'numero_relation', 'numero', ['numero_id_associe'], ['id'])
    op.create_foreign_key('fk_numero_relation_numero_id_base_numero', 'numero_relation', 'numero', ['numero_id_base'], ['id'])
    op.create_foreign_key('fk_numero_relation_relation_type_id_numero_relation_type', 'numero_relation', 'numero_relation_type', ['relation_type_id'], ['id'])
    op.create_foreign_key('fk_numero_relation_affaire_id_affaire', 'numero_relation', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_numero_etat_histo_numero_etat_id_numero_etat'), 'numero_etat_histo', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_etat_histo_numero_id_numero'), 'numero_etat_histo', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_numero_etat_histo_numero_etat_id_numero_etat', 'numero_etat_histo', 'numero_etat', ['numero_etat_id'], ['id'])
    op.create_foreign_key('fk_numero_etat_histo_numero_id_numero', 'numero_etat_histo', 'numero', ['numero_id'], ['id'])
    op.drop_constraint(op.f('fk_numero_differe_affaire_id_affaire'), 'numero_differe', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_differe_numero_id_numero'), 'numero_differe', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_numero_differe_numero_id_numero', 'numero_differe', 'numero', ['numero_id'], ['id'])
    op.create_foreign_key('fk_numero_differe_affaire_id_affaire', 'numero_differe', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_numero_etat_id_numero_etat'), 'numero', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_type_id_numero_type'), 'numero', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_numero_cadastre_id_cadastre'), 'numero', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_numero_type_id_numero_type', 'numero', 'numero_type', ['type_id'], ['id'])
    op.create_foreign_key('fk_numero_cadastre_id_cadastre', 'numero', 'cadastre', ['cadastre_id'], ['id'])
    op.create_foreign_key('fk_numero_etat_id_numero_etat', 'numero', 'numero_etat', ['etat_id'], ['id'])
    op.drop_constraint(op.f('fk_modification_affaire_type_affaire_destination_type_id_affaire_type'), 'modification_affaire_type', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_modification_affaire_type_affaire_destination_type_i_65bc', 'modification_affaire_type', 'affaire_type', ['affaire_destination_type_id'], ['id'])
    op.drop_constraint(op.f('fk_modification_affaire_affaire_id_fille_affaire'), 'modification_affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_modification_affaire_affaire_id_mere_affaire'), 'modification_affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_modification_affaire_type_id_modification_affaire_type'), 'modification_affaire', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_modification_affaire_affaire_id_fille_affaire', 'modification_affaire', 'affaire', ['affaire_id_fille'], ['id'])
    op.create_foreign_key('fk_modification_affaire_affaire_id_mere_affaire', 'modification_affaire', 'affaire', ['affaire_id_mere'], ['id'])
    op.create_foreign_key('fk_modification_affaire_type_id_modification_affaire_type', 'modification_affaire', 'modification_affaire_type', ['type_id'], ['id'])
    op.drop_constraint(op.f('fk_fonction_role_fonction_id_fonction'), 'fonction_role', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_fonction_role_role_id_role'), 'fonction_role', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_fonction_role_fonction_id_fonction', 'fonction_role', 'fonction', ['fonction_id'], ['id'])
    op.create_foreign_key('fk_fonction_role_role_id_role', 'fonction_role', 'role', ['role_id'], ['id'])
    op.drop_constraint(op.f('fk_facture_client_id_client'), 'facture', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_facture_affaire_id_affaire'), 'facture', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_facture_client_co_id_client'), 'facture', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_facture_type_id_facture_type'), 'facture', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_facture_client_co_id_client', 'facture', 'client', ['client_co_id'], ['id'])
    op.create_foreign_key('fk_facture_client_id_client', 'facture', 'client', ['client_id'], ['id'])
    op.create_foreign_key('fk_facture_type_id_facture_type', 'facture', 'facture_type', ['type_id'], ['id'])
    op.create_foreign_key('fk_facture_affaire_id_affaire', 'facture', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_etape_mailer_operateur_id_operateur'), 'etape_mailer', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_etape_mailer_etape_id_affaire_etape_index'), 'etape_mailer', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_etape_mailer_operateur_id_operateur', 'etape_mailer', 'operateur', ['operateur_id'], ['id'])
    op.create_foreign_key('fk_etape_mailer_etape_id_affaire_etape_index', 'etape_mailer', 'affaire_etape_index', ['etape_id'], ['id'])
    op.drop_constraint(op.f('fk_emolument_facture_emolument_id_tableau_emoluments'), 'emolument_facture', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_emolument_facture_facture_id_facture'), 'emolument_facture', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_emolument_facture_facture_id_facture', 'emolument_facture', 'facture', ['facture_id'], ['id'])
    op.create_foreign_key('fk_emolument_facture_emolument_id_tableau_emoluments', 'emolument_facture', 'tableau_emoluments', ['emolument_id'], ['id'])
    op.drop_constraint(op.f('fk_controle_ppe_operateur_id_operateur'), 'controle_ppe', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_controle_ppe_affaire_id_affaire'), 'controle_ppe', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_controle_ppe_operateur_id_operateur', 'controle_ppe', 'operateur', ['operateur_id'], ['id'])
    op.create_foreign_key('fk_controle_ppe_affaire_id_affaire', 'controle_ppe', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_controle_mutation_visa_operateur'), 'controle_mutation', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_controle_mutation_affaire_id_affaire'), 'controle_mutation', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_controle_mutation_visa_operateur', 'controle_mutation', 'operateur', ['visa'], ['id'])
    op.create_foreign_key('fk_controle_mutation_affaire_id_affaire', 'controle_mutation', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_controle_geometre_affaire_id_affaire'), 'controle_geometre', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_controle_geometre_operateur_id_operateur'), 'controle_geometre', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_controle_geometre_operateur_id_operateur', 'controle_geometre', 'operateur', ['operateur_id'], ['id'])
    op.create_foreign_key('fk_controle_geometre_affaire_id_affaire', 'controle_geometre', 'affaire', ['affaire_id'], ['id'])
    op.drop_constraint(op.f('fk_client_moral_personne_client_id_client'), 'client_moral_personne', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_client_moral_personne_client_id_client', 'client_moral_personne', 'client', ['client_id'], ['id'])
    op.drop_constraint(op.f('fk_client_type_client_client_type'), 'client', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_client_type_client_client_type', 'client', 'client_type', ['type_client'], ['id'])
    op.drop_constraint(op.f('fk_affaire_numero_numero_id_numero'), 'affaire_numero', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_numero_affaire_destination_id_affaire'), 'affaire_numero', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_numero_type_id_affaire_numero_type'), 'affaire_numero', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_numero_affaire_id_affaire'), 'affaire_numero', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_affaire_numero_type_id_affaire_numero_type', 'affaire_numero', 'affaire_numero_type', ['type_id'], ['id'])
    op.create_foreign_key('fk_affaire_numero_affaire_id_affaire', 'affaire_numero', 'affaire', ['affaire_id'], ['id'])
    op.create_foreign_key('fk_affaire_numero_numero_id_numero', 'affaire_numero', 'numero', ['numero_id'], ['id'])
    op.create_foreign_key('fk_affaire_numero_affaire_destination_id_affaire', 'affaire_numero', 'affaire', ['affaire_destination_id'], ['id'])
    op.drop_constraint(op.f('fk_affaire_etape_affaire_id_affaire'), 'affaire_etape', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_etape_etape_id_affaire_etape_index'), 'affaire_etape', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_etape_operateur_id_operateur'), 'affaire_etape', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_affaire_etape_affaire_id_affaire', 'affaire_etape', 'affaire', ['affaire_id'], ['id'])
    op.create_foreign_key('fk_affaire_etape_operateur_id_operateur', 'affaire_etape', 'operateur', ['operateur_id'], ['id'])
    op.create_foreign_key('fk_affaire_etape_etape_id_affaire_etape_index', 'affaire_etape', 'affaire_etape_index', ['etape_id'], ['id'])
    op.drop_constraint(op.f('fk_affaire_client_envoi_id_client'), 'affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_technicien_id_operateur'), 'affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_type_id_affaire_type'), 'affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_client_commande_id_client'), 'affaire', schema='infolica', type_='foreignkey')
    op.drop_constraint(op.f('fk_affaire_cadastre_id_cadastre'), 'affaire', schema='infolica', type_='foreignkey')
    op.create_foreign_key('fk_affaire_client_commande_id_client', 'affaire', 'client', ['client_commande_id'], ['id'])
    op.create_foreign_key('fk_affaire_client_envoi_id_client', 'affaire', 'client', ['client_envoi_id'], ['id'])
    op.create_foreign_key('fk_affaire_cadastre_id_cadastre', 'affaire', 'cadastre', ['cadastre_id'], ['id'])
    op.create_foreign_key('fk_affaire_type_id_affaire_type', 'affaire', 'affaire_type', ['type_id'], ['id'])
    op.create_foreign_key('fk_affaire_technicien_id_operateur', 'affaire', 'operateur', ['technicien_id'], ['id'])
    # ### end Alembic commands ###
