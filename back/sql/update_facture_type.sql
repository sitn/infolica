create sequence infolica.facture_type_id_seq;

create table infolica.facture_type (
	id bigint not null default nextval('infolica.facture_type_id_seq'),
	nom text not null,
	primary key(id)
);

alter table infolica.facture_type
owner to infolica;

alter table infolica.facture
add column type_id bigint;

alter table infolica.facture
add constraint fk_facture_type_id_facture_type
	FOREIGN KEY(type_id) 
		REFERENCES infolica.facture_type(id);

insert into infolica.facture_type (nom)
values ('Facture'), ('Devis');

update infolica.facture 
set type_id = 1;