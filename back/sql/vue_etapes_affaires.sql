create view infolica.v_etape_affaire as
select aff.id as affaire_id, aff.nom as nom, 'Ouverture' as etape, aff.date_ouverture as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.affaire as aff
-- validation
union 
select aff.id as affaire_id, aff.nom as nom, 'Validation' as etape, aff.date_validation as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.affaire as aff
where aff.date_validation is not NULL
-- cloture
union 
select aff.id as affaire_id, aff.nom as nom, 'Clôture' as etape, aff.date_cloture as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.affaire as aff
where aff.date_cloture is not NULL
-- modification_globale
union 
select aff.id as affaire_id, aff.nom as nom, mafft.nom as etape, maff.date as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.affaire as aff, infolica.modification_affaire as maff, infolica.modification_affaire_type as mafft
where aff.id = maff.affaire_id_mere
and maff.type_id = mafft.id
and maff.affaire_id_mere = maff.affaire_id_fille
-- modification_partielle
union 
select aff.id as affaire_id, aff.nom as nom, mafft.nom as etape, maff.date as date_etape, maff.affaire_id_fille as affaire_liee, concat_ws(' / ', aff2.id, aff2.nom) as nom_affaire_liee, NULL as service_nom
from infolica.affaire as aff, infolica.modification_affaire as maff, infolica.modification_affaire_type as mafft, infolica.affaire as aff2
where aff.id = maff.affaire_id_mere
and maff.type_id = mafft.id
and maff.affaire_id_mere != maff.affaire_id_fille
and aff2.id = maff.affaire_id_fille
-- envoi de documents
union 
select aff.id as affaire_id, aff.nom as nom, 'Envoi documents' as etape, env.date as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.envoi as env, infolica.affaire as aff 
where env.affaire_id = aff.id
-- envoi de facture
union 
select aff.id as affaire_id, aff.nom as nom, 'Facture' as etape, env.date as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, NULL as service_nom
from infolica.envoi as env, infolica.affaire as aff
where env.affaire_id = aff.id
-- préavis demande
union 
select aff.id as affaire_id, aff.nom as nom, 'Préavis - demande' as etape, pre.date_demande as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, ser.service as service_nom
from infolica.preavis as pre, infolica.affaire as aff, infolica.service as ser
where pre.affaire_id = aff.id
and pre.service_id = ser.id
-- préavis retour
union 
select aff.id as affaire_id, aff.nom as nom, 'Préavis - réponse' as etape, pre.date_reponse as date_etape, cast(null as integer) as affaire_liee, NULL as nom_affaire_liee, ser.service as service_nom
from infolica.preavis as pre, infolica.affaire as aff, infolica.service as ser
where pre.affaire_id = aff.id
and pre.service_id = ser.id