create view infolica.v_affaires as
select aff.id as id, aff.nom as nom, cl.entreprise as client_commande_entreprise, cl.titre as client_commande_titre, cl.nom as client_commande_nom, cl.prenom as client_commande_prenom, 
clp.entreprise as client_commande_par_entreprise, clp.titre as client_commande_par_titre, clp.nom as client_commande_par_nom, clp.prenom as client_commande_par_prenom, 
op.nom as responsable_nom, op.prenom as responsable_prenom, op2.nom as technicien_nom, op2.prenom as technicien_prenom, afft.nom as type_affaire, cad.nom as cadastre, 
aff.information as information, aff.date_ouverture as date_ouverture, aff.date_validation as date_validation, aff.date_cloture as date_cloture, 
aff."localisation_E" as localisation_e, aff."localisation_N" as localisation_n
from infolica.affaire as aff
left join infolica.client as cl on aff.client_commande_id = cl.id
left join infolica.client as clp on aff.client_commande_par_id = clp.id
left join infolica.operateur as op on aff.responsable_id = op.id
left join infolica.operateur as op2 on aff.technicien_id = op2.id
left join infolica.affaire_type as afft on aff.type_id = afft.id
left join infolica.cadastre as cad on aff.cadastre_id = cad.id