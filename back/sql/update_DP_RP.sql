-- add cadastre cantonal
insert into infolica.cadastre (id, nom) values (0, 'Cadastre cantonal');

-- CREATE NUMERO DP
select max (id) + 1 into dp from infolica.numero;
select max (id) + 2 into rp from infolica.numero;

insert into infolica.numero (id, cadastre_id, type_id, numero, etat_id) values ((select * from dp), 0, 1, 1, 2);
insert into infolica.numero (id, cadastre_id, type_id, numero, etat_id) values ((select * from rp), 0, 1, 2, 2);

-- DELETE HISTORY OF DP and RP
delete from infolica.numero_etat_histo
where infolica.numero_etat_histo.id in (select numeh.id
										from infolica.numero_etat_histo as numeh, infolica.numero as num
										where numeh.numero_id = num.id
										and num.numero >= 1000000);


--================================= DP START =================================

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.affaire_numero
set numero_id = (select * from dp)
where infolica.affaire_numero.id in (select affnum.id
										from infolica.affaire_numero as affnum, infolica.numero as num
										where affnum.numero_id = num.id
										and num.numero >= 1000000 and num.numero <8000000);

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.numero_relation
set numero_id_base = (select * from dp)
where infolica.numero_relation.id in (select numr.id
										from infolica.numero_relation as numr, infolica.numero as num
										where numr.numero_id_base = num.id
										and num.numero >= 1000000 and num.numero <8000000);

-- REFER TO NUMERO.ID=39992 (DP)
update infolica.numero_relation
set numero_id_associe = (select * from dp)
where infolica.numero_relation.id in (select numr.id
									  from infolica.numero_relation as numr, infolica.numero as num
									  where numr.numero_id_associe = num.id
									  and num.numero >= 1000000 and num.numero <8000000);
									  

--================================= DP END =================================
--================================= RP START =================================

-- REFER TO NUMERO.ID=39992 (RP)
update infolica.affaire_numero
set numero_id = (select * from rp)
where infolica.affaire_numero.id in (select affnum.id
										from infolica.affaire_numero as affnum, infolica.numero as num
										where affnum.numero_id = num.id
										and num.numero >= 8000000);

-- REFER TO NUMERO.ID=39992 (RP)
update infolica.numero_relation
set numero_id_base = (select * from rp)
where infolica.numero_relation.id in (select numr.id
										from infolica.numero_relation as numr, infolica.numero as num
										where numr.numero_id_base = num.id
										and num.numero >= 8000000);

-- REFER TO NUMERO.ID=39992 (RP)
update infolica.numero_relation
set numero_id_associe = (select * from rp)
where infolica.numero_relation.id in (select numr.id
									  from infolica.numero_relation as numr, infolica.numero as num
									  where numr.numero_id_associe = num.id
    								  and num.numero >= 8000000);

--================================= RP END =================================

-- DELETE NUMEROS
delete from infolica.numero
where numero.numero >= 1000000;


drop table dp;
drop table rp;
