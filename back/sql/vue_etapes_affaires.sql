create view infolica.v_etapes_affaires as
select aff.id as affaire_id, aff.nom as affaire_nom, 'Ouverture' as etape, aff.date_ouverture as date_etape, cast(null as integer) as affaire_liee_id, 
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.affaire as aff
-- validation
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Validation' as etape, aff.date_validation as date_etape, cast(null as integer) as affaire_liee_id, 
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.affaire as aff
where aff.date_validation is not NULL
-- cloture
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Clôture' as etape, aff.date_cloture as date_etape, cast(null as integer) as affaire_liee_id, 
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.affaire as aff
where aff.date_cloture is not NULL
-- modification_globale
union 
select aff.id as affaire_id, aff.nom as affaire_nom, mafft.nom as etape, maff.date as date_etape, cast(null as integer) as affaire_liee_id,
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.affaire as aff, infolica.modification_affaire as maff, infolica.modification_affaire_type as mafft
where aff.id = maff.affaire_id_mere
and maff.type_id = mafft.id
and maff.affaire_id_mere = maff.affaire_id_fille
-- modification_partielle
union 
select aff.id as affaire_id, aff.nom as affaire_nom, mafft.nom as etape, maff.date as date_etape, maff.affaire_id_fille as affaire_liee_id, 
aff2.nom as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.affaire as aff, infolica.modification_affaire as maff, infolica.modification_affaire_type as mafft, infolica.affaire as aff2
where aff.id = maff.affaire_id_mere
and maff.type_id = mafft.id
and maff.affaire_id_mere != maff.affaire_id_fille
and aff2.id = maff.affaire_id_fille
-- envoi de documents
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Envoi documents' as etape, env.date as date_etape, cast(null as integer) as affaire_liee_id, 
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.envoi as env, infolica.affaire as aff 
where env.affaire_id = aff.id
-- envoi de facture
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Facture' as etape, env.date as date_etape, cast(null as integer) as affaire_liee_id,
NULL as affaire_liee_nom, NULL as service_nom, NULL as remarque
from infolica.envoi as env, infolica.affaire as aff
where env.affaire_id = aff.id
-- préavis demande
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Préavis - demande' as etape, pre.date_demande as date_etape, cast(null as integer) as affaire_liee_id,
NULL as affaire_liee_nom, ser.service as service_nom, NULL as remarque
from infolica.preavis as pre, infolica.affaire as aff, infolica.service as ser
where pre.affaire_id = aff.id
and pre.service_id = ser.id
-- préavis retour
union 
select aff.id as affaire_id, aff.nom as affaire_nom, 'Préavis - réponse' as etape, pre.date_reponse as date_etape, cast(null as integer) as affaire_liee_id,
NULL as affaire_liee_nom, ser.service as service_nom, NULL as remarque
from infolica.preavis as pre, infolica.affaire as aff, infolica.service as ser
where pre.affaire_id = aff.id
and pre.service_id = ser.id
-- etapes_affaire
union 
select aff.id as affaire_id, aff.nom as affaire_nom, affeti.nom as etape, affet.date as date_etape, cast(null as integer) as affaire_liee_id,
NULL as affaire_liee_nom, NULL as service_nom, affet.remarque as remarque
from infolica.affaire_etape as affet, infolica.affaire_etape_index as affeti, infolica.affaire as aff
where affet.affaire_id = aff.id
and affet.etape_id = affeti.id

order by affaire_id asc, date_etape desc