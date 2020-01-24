create view infolica.v_envois as
select aff.id as affaire_id, aff.nom as affaire_nom, cl.entreprise as client_entreprise, cl.titre as client_titre, cl.nom as client_nom, cl.prenom as client_prenom,
doc.nom as document_nom, env.date as date
from infolica.envoi as env
left join infolica.affaire as aff on env.affaire_id = aff.id
left join infolica.client as cl on env.client_id = cl.id
join infolica.envoi_document as envd on env.id = envd.id
join infolica.document as doc on envd.document_id = doc.id