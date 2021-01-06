do $$
begin
	for i in 1..(select max(aff.id) from infolica.affaire aff) loop
		
		update infolica.numero_relation
		set affaire_id = i
		where (
			numero_id_base in (
				select affnum.numero_id
				from infolica.affaire_numero affnum
				where affnum.affaire_id = i
			)
			and numero_id_associe in (
				select affnum.numero_id
				from infolica.affaire_numero affnum
				where affnum.affaire_id = i
			)
		);
				
	end loop;
end $$