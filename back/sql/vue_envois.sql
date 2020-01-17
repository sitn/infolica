create view infolica.v_envois as
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as affaire_nom, concat_ws(' / ', cl.entreprise, concat_ws(', ', cl.titre, concat_ws(' ', cl.nom, cl.prenom))) as client,
doc.nom as document_nom, env.date as date
from infolica.envoi as env
left join infolica.affaire as aff on env.affaire_id = aff.id
left join infolica.client as cl on env.client_id = cl.id
join infolica.envoi_document as envd on env.id = envd.id
join infolica.document as doc on envd.document_id = doc.id