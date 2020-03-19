create view infolica.v_affaires_preavis as
select pr.affaire_id as affaire_id, ser.service as service, prt.nom as preavis , pr.date_demande as date_demande, pr.date_reponse as date_reponse
from infolica.preavis as pr, infolica.service as ser, infolica.preavis_type as prt
where pr.service_id = ser.id
and pr.preavis_type_id = prt.id
order by affaire_id 