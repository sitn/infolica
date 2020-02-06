create view infolica.v_envois as
select aff.id as affaire_id, aff.nom as affaire_nom, cl.id as client_id, cl.entreprise as client_entrprise, cl.titre as client_titre, cl.nom as client_nom,
cl.prenom as client_prenom, env.date as date, doc.nom as document_nom, doc.chemin as document_chemin
from infolica.envoi as env 
left join infolica.envoi_document as envd on envd.envoi_id = env.id
left join infolica.document as doc on envd.document_id = doc.id,
infolica.affaire as aff, infolica.client as cl
where cl.id = env.client_id
and env.affaire_id = aff.id
