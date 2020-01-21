create view infolica.v_affaires_balances as 
select aff.id as affaire_id, numb.id as numero_base_id, numa.id as numero_associe_id, bal.numero_relation_id as numero_relation_id, aff.nom as affaire_nom, numtb.nom as numero_base_type, numb.numero as numero_base, 
numb.suffixe as numero_base_suffixe, numeb.nom as numero_base_etat, numta.nom as numero_associe_type, numa.numero as numero_associe, numa.suffixe as numero_associe_suffixe, 
numea.nom as numero_associe_etat, numrelt.nom as numero_relation_type
from 
   (select src.affaire_id as affaire_id, src.numero_relation_id as numero_relation_id
	from 
	   (select affnum.affaire_id as affaire_id, numrel.id as numero_relation_id
		from infolica.numero_relation as numrel, infolica.affaire_numero as affnum
		where affnum.numero_id = numrel.numero_id_base
		group by numero_relation_id, affaire_id
	   ) as src,
	   (select affnum.affaire_id as affaire_id, numrel.id as numero_relation_id
		from infolica.numero_relation as numrel, infolica.affaire_numero as affnum
		where affnum.numero_id = numrel.numero_id_associe
		group by numero_relation_id, affaire_id
	   ) as dst
	where src.numero_relation_id = dst.numero_relation_id
	and src.affaire_id = dst.affaire_id
	order by affaire_id asc, numero_relation_id asc
	) as bal, infolica.numero_relation as numrel, infolica.numero_relation_type as numrelt, infolica.numero as numb, infolica.numero as numa, infolica.affaire as aff,
	infolica.numero_etat as numeb, infolica.numero_etat as numea, infolica.numero_type as numtb, infolica.numero_type as numta
where numrel.relation_type_id = numrelt.id
and numrel.id = bal.numero_relation_id
and numrel.numero_id_base = numb.id
and numb.etat_id = numeb.id
and numb.type_id = numtb.id 
and numrel.numero_id_associe = numa.id
and numa.etat_id = numea.id
and numa.type_id = numta.id 
and bal.affaire_id = aff.id
order by numero_base asc, numero_associe asc