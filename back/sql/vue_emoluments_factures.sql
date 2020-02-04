create view infolica.v_emoluments_factures as 
select emof.facture_id as facture_id, emot.domaine as domaine, emot.categorie as categorie, emot.sous_categorie as sous_categorie, emot.nom as nom,
emot.unite as unite, emot.montant as prix_unitaire, emof.nombre as nombre, emof.facteur_correctif as facteur_correctif, emof.batiment as batiment,
emof.montant as montant
from infolica.tableau_emoluments as emot, infolica.emolument_facture as emof
where emot.id = emof.emolument_id