create view infolica.v_affaires as
select aff.id as id, aff.nom as nom, concat_ws(', ', cl.entreprise, concat_ws(' ', cl.titre, cl.nom, cl.prenom)) as client_commande, 
concat_ws(', ', clp.entreprise, concat_ws(' ', clp.titre, clp.nom, clp.prenom)) as client_commande_par, concat_ws(' ', op.nom, op.prenom) as responsable,
concat_ws(' ', op2.nom, op2.prenom) as technicien, afft.nom as type_affaire, cad.nom as cadastre, aff.information as information, aff.date_ouverture as date_ouverture, aff.date_validation as date_validation, aff.date_cloture as date_cloture, 
concat_ws(' / ', aff."localisation_E", aff."localisation_N") as localisation
from infolica.affaire as aff left join infolica.client as cl on aff.client_commande_id = cl.id
left join infolica.client as clp on aff.client_commande_par_id = clp.id
left join infolica.operateur as op on aff.responsable_id = op.id
left join infolica.operateur as op2 on aff.technicien_id = op2.id
left join infolica.affaire_type as afft on aff.type_id = afft.id
left join infolica.cadastre as cad on aff.cadastre_id = cad.id