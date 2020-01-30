create view infolica.v_numeros as 
select num.id as id, cad.nom as cadastre, num.numero as numero, num.suffixe as suffixe, nume.nom as etat, numt.nom as type_numero, 
numdiff.date_entree as diff_entree, numdiff.date_sortie as diff_sortie, num.plan_id as plan_id
from infolica.numero as num
	left join infolica.numero_differe as numdiff on num.id = numdiff.numero_id,
	infolica.numero_etat as nume, infolica.numero_type as numt, infolica.cadastre as cad
where num.etat_id = nume.id
and num.type_id = numt.id 
and num.cadastre_id = cad.id
