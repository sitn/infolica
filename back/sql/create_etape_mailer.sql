CREATE SEQUENCE infolica.etape_mailer_id_seq;

ALTER SEQUENCE infolica.etape_mailer_id_seq
    OWNER TO infolica;

create table infolica.etape_mailer (
	id bigint default nextval('infolica.etape_mailer'::regclass),
	etape_id Bigint not null,
	operateur_id Bigint not null,
	sendmail Boolean,
	primary key(id),
	CONSTRAINT fk_etape_id
      FOREIGN KEY(etape_id) 
	    REFERENCES infolica.affaire_etape_index(id),
	CONSTRAINT fk_operateur_id
      FOREIGN KEY(operateur_id) 
	    REFERENCES infolica.operateur(id),
	constraint uq_etape_operateur
		unique(etape_id, operateur_id)
);

alter table infolica.etape_mailer
	owner to infolica;
