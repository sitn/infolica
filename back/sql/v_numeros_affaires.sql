create view infolica.v_numeros_affaires as
select affnum.numero_id as numero_id, aff.id as affaire_id, affnum.type_id as affaire_numero_type_id, aff.nom as affaire_nom, afft.nom as affaire_type, aff.date_ouverture as affaire_date, aff.information as affaire_information,
cad.nom as numero_cadastre, numt.nom as numero_type, num.numero as numero, num.suffixe as numero_suffixe, nume.nom as numero_etat, affnumt.nom as affaire_numero_type
from infolica.affaire_numero as affnum, infolica.affaire as aff, infolica.affaire_type as afft, infolica.numero as num, infolica.cadastre as cad, infolica.numero_type as numt,
infolica.numero_etat as nume, infolica.affaire_numero_type as affnumt
where affnum.affaire_id = aff.id
and afft.id = aff.type_id
and affnum.numero_id = num.id
and num.cadastre_id = cad.id
and num.type_id = numt.id
and num.etat_id = nume.id
and affnum.type_id = affnumt.id
order by numero_id asc, affaire_date desc
