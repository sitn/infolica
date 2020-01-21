--create view infolica.tableau_de_bord as
select aff.id as aff_id, aff.nom as nom, date(now())-aff.date_ouverture as delai, cl.entreprise as client_entreprise, cl.titre as client_titre, cl.nom as client_nom, 
cl.prenom as client_prenom, afft.nom as affaire_type, opc.nom as chef_nom, opc.prenom as chef_prenom, opt.nom as technicien_nom, opt.prenom as technicien_prenom
from infolica.affaire as aff, infolica.client as cl, infolica.affaire_type as afft, infolica.operateur as opc, infolica.operateur as opt
where aff.date_cloture is NULL
and aff.client_commande_id = cl.id
and aff.type_id = afft.id
and aff.responsable_id = opc.id
and aff.technicien_id = opt.id
order by delai asc