create view infolica.v_tableau_de_bord as
select aff.id as aff_id, aff.nom as affaire_nom, date(now())-aff.date_ouverture as delai, cl.entreprise as client_entreprise, cl.titre as client_titre, cl.nom as client_nom, 
cl.prenom as client_prenom, afft.nom as affaire_type, opc.nom as chef_nom, opc.prenom as chef_prenom, opt.nom as technicien_nom, opt.prenom as technicien_prenom, 
aff.information as information, cad.nom as cadastre, vetaff.etape
from infolica.affaire as aff, infolica.client as cl, infolica.affaire_type as afft, infolica.operateur as opc, infolica.operateur as opt, infolica.cadastre as cad, 
	(select vea.affaire_id as affaire_id, vea.etape as etape, max(vea.date_etape) as date_etape
	from infolica.v_etapes_affaires as vea
	group by vea.affaire_id, vea.etape
	) as vetaff
where aff.date_cloture is NULL
and aff.client_commande_id = cl.id
and aff.type_id = afft.id
and aff.responsable_id = opc.id
and aff.technicien_id = opt.id
and aff.cadastre_id = cad.id
and aff.id = vetaff.affaire_id