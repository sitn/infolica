create view infolica.v_envois as
select aff.id as affaire_id, aff.nom as affaire_nom, cl.id as client_id, cl.entreprise as client_entrprise, cl.titre as client_titre, cl.nom as client_nom,
cl.prenom as client_prenom, envt.nom as envoi_type, env.date as date
from infolica.envoi as env, infolica.affaire as aff, infolica.client as cl, infolica.envoi_type as envt
where env.affaire_id = aff.id
and env.client_id = cl.id
and env.type_id = envt.id
