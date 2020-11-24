alter table infolica.affaire_etape
add column datetime timestamp without time zone
add column operateur_id Bigint
 add constraint fk_operateur_id_operateur
  foreign key(operateur_id)
   references infolica.operateur(id);