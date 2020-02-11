-- DELETE HISTORY OF DP
delete from infolica.numero_etat_histo
where infolica.numero_etat_histo.id in (select numeh.id
										from infolica.numero_etat_histo as numeh, infolica.numero as num
										where numeh.numero_id = num.id
										and num.numero >= 1000000);

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.affaire_numero
set numero_id = 39992
where infolica.affaire_numero.id in (select affnum.id
										from infolica.affaire_numero as affnum, infolica.numero as num
										where affnum.numero_id = num.id
										and num.numero >= 1000000);

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.numero_relation
set numero_id_base = 39992
where infolica.numero_relation.id in (select numr.id
										from infolica.numero_relation as numr, infolica.numero as num
										where numr.numero_id_base = num.id
										and num.numero >= 1000000);

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.numero_relation
set numero_id_associe = 39992
where infolica.numero_relation.id in (select numr.id
									  from infolica.numero_relation as numr, infolica.numero as num
									  where numr.numero_id_associe = num.id
									  and num.numero >= 1000000);
									  
-- DELETE NUMEROS
delete from infolica.numero
where numero.numero >= 1000000;
