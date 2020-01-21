create view infolica.v_numeros as 
select num.id as id, cad.nom as cadastre, num.numero as numero, num.suffixe as suffixe, nume.nom as etat, numt.nom as type_numero
from infolica.numero as num, infolica.numero_etat as nume, infolica.numero_type as numt, infolica.cadastre as cad
where num.etat_id = nume.id
and num.type_id = numt.id 
and num.cadastre_id = cad.id
