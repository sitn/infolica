create view infolica.v_numeros as 
select num.id as id, cad.nom as cadastre, num.numero as numero, num.suffixe as suffixe, nume.nom as etat, numt.nom as type_numero
from infolica.numero as num 
left join infolica.numero_etat as nume on num.etat_id = nume.id
left join infolica.numero_type as numt on num.type_id = numt.id 
left join infolica.cadastre as cad on num.cadastre_id = cad.id
