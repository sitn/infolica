 SELECT aff.id,
    aff.no_access,
    aff.nom,
    cl.id AS client_commande_id,
    cl.entreprise AS client_commande_entreprise,
    cl.titre AS client_commande_titre,
    cl.nom AS client_commande_nom,
    cl.prenom AS client_commande_prenom,
    cl.adresse AS client_commande_adresse,
    cl.co AS client_commande_co,
    cl.npa AS client_commande_npa,
    cl.localite AS client_commande_localite,
    cl.tel_fixe AS client_commande_tel_fixe,
    cl.tel_portable AS client_commande_tel_portable,
    cl.fax AS client_commande_fax,
    cl.mail AS client_commande_mail,
    cl.no_sap AS client_commande_no_sap,
    cl.no_bdp_bdee AS client_commande_no_bdp_bdee,
    aff.client_commande_complement,
    cle.id AS client_envoi_id,
    cle.entreprise AS client_envoi_entreprise,
    cle.titre AS client_envoi_titre,
    cle.nom AS client_envoi_nom,
    cle.prenom AS client_envoi_prenom,
    cle.co AS client_envoi_co,
    cle.adresse AS client_envoi_adresse,
    cle.npa AS client_envoi_npa,
    cle.localite AS client_envoi_localite,
    cle.tel_fixe AS client_envoi_tel_fixe,
    cle.tel_portable AS client_envoi_tel_portable,
    cle.fax AS client_envoi_fax,
    cle.mail AS client_envoi_mail,
    cle.no_sap AS client_envoi_no_sap,
    cle.no_bdp_bdee AS client_envoi_no_bdp_bdee,
    aff.client_envoi_complement,
    op.id AS responsable_id,
    op.nom AS responsable_nom,
    op.prenom AS responsable_prenom,
    op2.id AS technicien_id,
    op2.nom AS technicien_nom,
    op2.prenom AS technicien_prenom,
    afft.nom AS type_affaire,
    cad.nom AS cadastre,
    aff.information,
    aff.date_ouverture,
    aff.date_validation,
    aff.date_envoi,
    aff.date_cloture,
    aff."localisation_E" AS localisation_e,
    aff."localisation_N" AS localisation_n,
    aff.cadastre_id,
    aff.type_id,
    aff.vref,
    aff.chemin,
    afft.reservation_numeros_types_id,
    afft.modif_affaire_type_id_vers,
    modaff.type_id AS modification_type_id,
    modaff.affaire_id_mere AS modification_affaire_id_mere,
    modafft.nom AS modification_type,
    prv_scat.date_demande AS preavis_scat_date_demande,
    prv_scat.date_reponse AS preavis_scat_date_reponse,
    prv_sagr.date_demande AS preavis_sagr_date_demande,
    prv_sagr.date_reponse AS preavis_sagr_date_reponse,
    prv_sene.date_demande AS preavis_sene_date_demande,
    prv_sene.date_reponse AS preavis_sene_date_reponse,
    prv_rf.date_demande AS preavis_rf_date_demande,
    prv_rf.date_reponse AS preavis_rf_date_reponse,
    aff.abandon,
    etape.etape_id,
    etape.etape,
    etape.datetime AS etape_datetime,
    etape.remarque AS etape_remarque,
    etape.priorite AS etape_priorite,
    etape.operateur_id AS etape_operateur_id,
    etape.operateur_nom AS etape_operateur_nom,
    etape.operateur_prenom AS etape_operateur_prenom
   FROM infolica.affaire aff
     LEFT JOIN infolica.client cl ON aff.client_commande_id = cl.id
     LEFT JOIN infolica.client cle ON aff.client_envoi_id = cle.id
     LEFT JOIN infolica.operateur op ON aff.responsable_id = op.id
     LEFT JOIN infolica.operateur op2 ON aff.technicien_id = op2.id
     LEFT JOIN infolica.affaire_type afft ON aff.type_id = afft.id
     LEFT JOIN infolica.cadastre cad ON aff.cadastre_id = cad.id
     LEFT JOIN infolica.modification_affaire modaff ON aff.id = modaff.affaire_id_fille
     LEFT JOIN infolica.modification_affaire_type modafft ON modaff.type_id = modafft.id
     LEFT JOIN ( SELECT prv.affaire_id,
            prv.date_demande,
            prv.date_reponse
           FROM infolica.preavis prv
          WHERE prv.service_id = 1) prv_scat ON prv_scat.affaire_id = aff.id
     LEFT JOIN ( SELECT prv.affaire_id,
            prv.date_demande,
            prv.date_reponse
           FROM infolica.preavis prv
          WHERE prv.service_id = 2) prv_sagr ON prv_sagr.affaire_id = aff.id
     LEFT JOIN ( SELECT prv.affaire_id,
            prv.date_demande,
            prv.date_reponse
           FROM infolica.preavis prv
          WHERE prv.service_id = 3) prv_sene ON prv_sene.affaire_id = aff.id
     LEFT JOIN ( SELECT prv.affaire_id,
            prv.date_demande,
            prv.date_reponse
           FROM infolica.preavis prv
          WHERE prv.service_id = 4) prv_rf ON prv_rf.affaire_id = aff.id
     LEFT JOIN ( SELECT et.id,
            et.affaire_id,
            et.etape_id,
            et.remarque,
            et.datetime,
            et.operateur_id,
            etidx.nom AS etape,
            etidx.priorite,
            op3_1.nom AS operateur_nom,
            op3_1.prenom AS operateur_prenom
           FROM infolica.affaire_etape et,
            infolica.affaire_etape_index etidx,
            infolica.operateur op3_1,
            ( SELECT max(affaire_etape.id) AS id,
                    affaire_etape.affaire_id
                   FROM infolica.affaire_etape,
                    infolica.affaire_etape_index
                  WHERE affaire_etape.etape_id = affaire_etape_index.id AND affaire_etape_index.ordre IS NOT NULL
                  GROUP BY affaire_etape.affaire_id) et2
          WHERE et.id = et2.id AND et.operateur_id = op3_1.id AND et.etape_id = etidx.id) etape ON etape.affaire_id = aff.id
     LEFT JOIN infolica.operateur op3 ON aff.technicien_id = op3.id
  ORDER BY aff.id DESC;