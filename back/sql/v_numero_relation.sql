create view infolica.v_numeros_relations as
select 
numb.id as numero_base_id, cadb.nom as numero_base_cadastre, numtb.nom as numero_base_type, numb.numero as numero_base_numero, numb.suffixe as numero_base_suffixe, numeb.nom as numero_base_etat, numb.plan_id as numero_base_plan_id,
numa.id as numero_associe_id, cada.nom as numero_associe_cadastre, numta.nom as numero_associe_type, numa.numero as numero_associe_numero, numa.suffixe as numero_associe_suffixe, numea.nom as numero_associe_etat, numa.plan_id as numero_associe_plan_id,
numrt.nom as relation_type
from infolica.numero as numb, infolica.numero as numa, infolica.numero_relation as numr, infolica.numero_relation_type as numrt, infolica.cadastre as cadb,
infolica.cadastre as cada, infolica.numero_type as numta, infolica.numero_type as numtb, infolica.numero_etat as numeb, infolica.numero_etat as numea
where numr.numero_id_base = numb.id
and numr.numero_id_associe = numa.id
and numr.relation_type_id = numrt.id
and numb.cadastre_id = cadb.id
and numa.cadastre_id = cada.id
and numb.type_id = numtb.id
and numa.type_id = numta.id
and numb.etat_id = numeb.id
and numa.etat_id = numea.id
