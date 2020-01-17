-- create view infolica.v_etape_affaire as
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, 'Ouverture' as etape, aff.date_ouverture as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee
from infolica.affaire as aff
union 
-- validation
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, 'Validation' as etape, aff.date_validation as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee
from infolica.affaire as aff
where aff.date_validation is not NULL
union 
-- cloture
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, 'Clôture' as etape, aff.date_cloture as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee
from infolica.affaire as aff
where aff.date_cloture is not NULL
union 
-- modification_globale
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, mafft.nom as etape, maff.date as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee
from infolica.affaire as aff
join infolica.modification_affaire as maff on aff.id = maff.affaire_id_mere, infolica.modification_affaire_type as mafft
where maff.type_id = mafft.id
and maff.affaire_id_mere = maff.affaire_id_fille
union 
-- modification_partielle
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, mafft.nom as etape, maff.date as date_etape, maff.affaire_id_fille as affaire_liee, concat_ws(' / ', aff2.id, aff2.nom) as nom_affaire_liee
from infolica.affaire as aff
join infolica.modification_affaire as maff on aff.id = maff.affaire_id_mere, infolica.modification_affaire_type as mafft, infolica.affaire as aff2
where maff.type_id = mafft.id
and maff.affaire_id_mere != maff.affaire_id_fille
and aff2.id = maff.affaire_id_fille
union
-- envoi de documents
select aff.id as affaire_id, concat_ws(' / ', aff.id, aff.nom) as nom, 'Envoi documents' as etape, env.date as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee
from infolica.envoi as env
left join infolica.affaire as aff on env.affaire_id = aff.id
-- envoi de facture
