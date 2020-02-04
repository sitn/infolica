create view infolica.v_numeros_affaires as
select affnum.numero_id as numero_id, aff.id as affaire_id, affnum.type_id as affaire_numero_type, aff.nom as affaire_nom, afft.nom as affaire_type, aff.date_ouverture as affaire_date, aff.information as affaire_information
from infolica.affaire_numero as affnum, infolica.affaire as aff, infolica.affaire_type as afft
where affnum.affaire_id = aff.id
and afft.id = aff.type_id
order by numero_id asc, affaire_date desc
