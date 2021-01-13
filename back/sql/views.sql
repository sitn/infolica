-- v_affaires
create VIEW infolica.v_affaires
as
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
        FROM infolica.affaire_etape et
            left join infolica.operateur op3_1 on et.operateur_id = op3_1.id,
            infolica.affaire_etape_index etidx,
            ( SELECT max(affaire_etape.id) AS id,
                affaire_etape.affaire_id
            FROM infolica.affaire_etape,
                infolica.affaire_etape_index
            WHERE affaire_etape.etape_id = affaire_etape_index.id AND affaire_etape_index.ordre IS NOT NULL
            GROUP BY affaire_etape.affaire_id) et2
        WHERE et.id = et2.id AND et.etape_id = etidx.id) etape ON etape.affaire_id = aff.id
        LEFT JOIN infolica.operateur op3 ON aff.technicien_id = op3.id
    ORDER BY aff.date_ouverture DESC;

alter table infolica.v_affaires
	owner to infolica;

-- affaires_preavis
create view infolica.v_affaires_preavis
AS
    SELECT pr.id,
        pr.affaire_id,
        ser.abreviation AS service,
        ser.id AS service_id,
        prt.nom AS preavis,
        prt.id AS preavis_type_id,
        pr.date_demande,
        pr.date_reponse,
        pr.remarque
    FROM infolica.service ser,
        infolica.preavis pr
        LEFT JOIN infolica.preavis_type prt ON pr.preavis_type_id = prt.id
    WHERE pr.service_id = ser.id
    ORDER BY pr.affaire_id;

alter table infolica.v_affaires_preavis
	owner to infolica;

-- etapes_affaires
create view infolica.v_etapes_affaires
AS
    SELECT ae.id,
        ae.affaire_id,
        ae.etape_id,
        aei.nom AS etape,
        ae.remarque,
        ae.datetime,
        ae.operateur_id,
        op.nom AS operateur_nom,
        op.prenom AS operateur_prenom,
        aei.ordre AS etape_ordre,
        aei.priorite AS etape_priorite
    FROM infolica.affaire_etape ae
        left join infolica.operateur op on op.id = ae.operateur_id,
        infolica.affaire_etape_index aei
    WHERE ae.etape_id = aei.id
    ORDER BY ae.id DESC;

alter table infolica.v_etapes_affaires
  OWNER to infolica;

-- v_factures
create view infolica.v_factures
as
    SELECT fact.affaire_id,
        aff.vref AS affaire_vref,
        fact.id,
        fact.sap,
        fact.client_id,
        cl.entreprise AS client_entreprise,
        cl.titre AS client_titre,
        cl.nom AS client_nom,
        cl.prenom AS client_prenom,
        cl.co AS client_co,
        cl.adresse AS client_adresse,
        cl.npa AS client_npa,
        cl.localite AS client_localite,
        cl.case_postale AS client_case_postale,
        cl.tel_fixe AS client_tel_fixe,
        cl.fax AS client_fax,
        cl.tel_portable AS client_tel_portable,
        cl.mail AS client_mail,
        cl.entree AS client_entree,
        cl.sortie AS client_sortie,
        cl.no_sap AS client_no_sap,
        cl.no_bdp_bdee AS client_no_bdp_bdee,
        fact.client_co_id,
        clco.entreprise AS client_co_entreprise,
        clco.titre AS client_co_titre,
        clco.nom AS client_co_nom,
        clco.prenom AS client_co_prenom,
        clco.co AS client_co_co,
        clco.adresse AS client_co_adresse,
        clco.npa AS client_co_npa,
        clco.localite AS client_co_localite,
        clco.case_postale AS client_co_case_postale,
        clco.tel_fixe AS client_co_tel_fixe,
        clco.fax AS client_co_fax,
        clco.tel_portable AS client_co_tel_portable,
        clco.mail AS client_co_mail,
        clco.entree AS client_co_entree,
        clco.sortie AS client_co_sortie,
        clco.no_sap AS client_co_no_sap,
        clco.no_bdp_bdee AS client_co_no_bdp_bdee,
        fact.montant_mo,
        fact.montant_mat_diff,
        fact.montant_rf,
        fact.montant_tva,
        fact.montant_total,
        fact.date,
        fact.remarque,
        fact.client_complement,
        fact.client_premiere_ligne,
        fact.numeros,
        fact.type_id
    FROM infolica.facture fact
        LEFT JOIN infolica.client clco ON fact.client_co_id = clco.id,
        infolica.client cl,
        infolica.affaire aff
    WHERE fact.affaire_id = aff.id AND fact.client_id = cl.id;

alter table infolica.v_factures
owner to infolica;

-- v_numeros
create view infolica.v_numeros
as
    SELECT num.id,
        cad.nom AS cadastre,
        num.cadastre_id,
        num.numero,
        CASE
            WHEN numdiff.date_entree IS NOT NULL AND numdiff.date_sortie IS NULL THEN 'diff'::text
            ELSE num.suffixe
        END AS suffixe,
        nume.nom AS etat,
        num.etat_id,
        numt.nom AS type_numero,
        num.type_id AS type_numero_id,
        numdiff.id AS diff_id,
        numdiff.date_entree AS diff_entree,
        numdiff.date_sortie AS diff_sortie,
        numdiff.affaire_id AS diff_affaire_id
    FROM infolica.numero num
        LEFT JOIN infolica.numero_differe numdiff ON num.id = numdiff.numero_id,
        infolica.numero_etat nume,
        infolica.numero_type numt,
        infolica.cadastre cad
    WHERE num.etat_id = nume.id AND num.type_id = numt.id AND num.cadastre_id = cad.id;

alter table infolica.v_numeros
owner to infolica;

-- v_numeros_affaires
create view infolica.v_numeros_affaires
as
    SELECT affnum.numero_id,
        affnum.id,
        aff.id AS affaire_id,
        affnum.type_id AS affaire_numero_type_id,
        affnum.actif AS affaire_numero_actif,
        affnum.affaire_destination_id,
        aff.nom AS affaire_nom,
        afft.nom AS affaire_type,
        aff.date_ouverture AS affaire_date,
        aff.information AS affaire_information,
        cad.nom AS numero_cadastre,
        cad.id AS numero_cadastre_id,
        numt.nom AS numero_type,
        num.type_id AS numero_type_id,
        num.numero,
        CASE
            WHEN numdiff.date_entree IS NOT NULL AND numdiff.date_sortie IS NULL THEN 'diff'::text
            ELSE num.suffixe
        END AS numero_suffixe,
        nume.nom AS numero_etat,
        nume.id AS numero_etat_id,
        affnumt.nom AS affaire_numero_type,
        numdiff.id AS numero_diff_id,
        numdiff.date_entree AS numero_diff_entree,
        numdiff.date_sortie AS numero_diff_sortie,
        tmp.numero_base_id,
        tmp.numero_base_type,
        tmp.numero_base,
        tmp.numero_base_suffixe,
        tmp.numero_base_etat,
        aff.no_access as affaire_no_access
    FROM infolica.affaire_numero affnum
        LEFT JOIN ( SELECT numr.affaire_id,
            numr.numero_id_associe AS numero_associe_id,
            numb.numero AS numero_base,
            numeb.nom AS numero_base_etat,
            numtb.nom AS numero_base_type,
            numr.numero_id_base AS numero_base_id,
            numb.suffixe AS numero_base_suffixe
        FROM infolica.numero_relation numr,
            infolica.numero numb,
            infolica.numero_type numtb,
            infolica.numero_etat numeb
        WHERE numr.numero_id_base = numb.id AND numb.type_id = numtb.id AND numb.etat_id = numeb.id) tmp ON affnum.affaire_id = tmp.affaire_id AND affnum.numero_id = tmp.numero_associe_id
        LEFT JOIN infolica.numero_differe numdiff ON affnum.numero_id = numdiff.numero_id,
        infolica.affaire aff,
        infolica.affaire_type afft,
        infolica.numero num,
        infolica.cadastre cad,
        infolica.numero_type numt,
        infolica.numero_etat nume,
        infolica.affaire_numero_type affnumt
    WHERE affnum.affaire_id = aff.id AND afft.id = aff.type_id AND affnum.numero_id = num.id AND num.cadastre_id = cad.id AND num.type_id = numt.id AND num.etat_id = nume.id AND affnum.type_id = affnumt.id
    ORDER BY tmp.numero_base_id, affnum.numero_id, aff.date_ouverture DESC;

alter table infolica.v_numeros_affaires
owner to infolica;

-- v_numeros_relations
create view infolica.v_numeros_relations
as
    SELECT numrel.id AS numero_relation_id,
        numrel.numero_id_base AS numero_base_id,
        numb.cadastre_id AS numero_base_cadastre_id,
        cadb.nom AS numero_base_cadastre,
        numb.type_id AS numero_base_type_id,
        numtb.nom AS numero_base_type,
        numb.numero AS numero_base,
        numb.suffixe AS numero_base_suffixe,
        numb.etat_id AS numero_base_etat_id,
        numeb.nom AS numero_base_etat,
        numrel.numero_id_associe AS numero_associe_id,
        numa.cadastre_id AS numero_associe_cadastre_id,
        cada.nom AS numero_associe_cadastre,
        numa.type_id AS numero_associe_type_id,
        numta.nom AS numero_associe_type,
        numa.numero AS numero_associe,
        numa.suffixe AS numero_associe_suffixe,
        numa.etat_id AS numero_associe_etat_id,
        numea.nom AS numero_associe_etat,
        numrel.relation_type_id AS numero_relation_type_id,
        numrelt.nom AS numero_relation_type,
        numrel.affaire_id
    FROM infolica.numero_relation numrel,
        infolica.numero numb,
        infolica.numero_type numtb,
        infolica.numero_etat numeb,
        infolica.cadastre cadb,
        infolica.numero numa,
        infolica.numero_type numta,
        infolica.numero_etat numea,
        infolica.cadastre cada,
        infolica.numero_relation_type numrelt
    WHERE numrel.numero_id_base = numb.id AND numb.cadastre_id = cadb.id AND numb.type_id = numtb.id AND numb.etat_id = numeb.id AND numrel.numero_id_associe = numa.id AND numa.cadastre_id = cada.id AND numa.type_id = numta.id AND numa.etat_id = numea.id AND numrel.relation_type_id = numrelt.id;

alter table infolica.v_numeros_relations
owner to infolica;

-- v_plans_mo
create view infolica.v_plans_mo
AS
    SELECT plan.idobj,
    plan.id_obj2,
    "left"(plan.id_obj2::text, strpos(plan.id_obj2::text, '_'::text) - 1)::integer AS cadastre_id,
        cad.nom AS cadastre,
        plan.planno::integer AS planno,
        plan.typlan,
        plan.datmev,
        plan.statut,
        plan.echell,
        plan.idborplan,
        plan.idrepplan,
        plan.base
    FROM infolica.mo_distr_plan plan,
    infolica.cadastre cad
  WHERE "left"
(plan.id_obj2::text, strpos
(plan.id_obj2::text, '_'::text) - 1)::integer = cad.id;

alter table infolica.v_plans_mo
owner to infolica;

-- v_reservations_numseros_mo
create view infolica.v_reservation_numeros_mo AS
SELECT resnum.id,
    resnum.affaire_id,
    resnum.cadastre_id,
    cad.nom AS cadastre,
    resnum.type_id,
    numt.nom AS type_numero,
    resnum.numero_de,
    resnum.numero_a,
    resnum.date,
    resnum.remarque,
    resnum.operateur_id,
    op.nom AS operateur_nom,
    op.prenom AS operateur_prenom,
    resnum.plan_id,
    plan.id_obj2 AS plan_id2,
    plan.planno AS plan_no,
    plan.typlan AS plan_type,
    plan.datmev AS plan_datemev,
    plan.statut AS plan_statut,
    plan.echell AS plan_echelle,
    plan.idborplan AS plan_idorplan,
    plan.idrepplan AS plan_idrepplan,
    plan.base AS plan_base
FROM infolica.reservation_numeros resnum
    LEFT JOIN infolica.mo_distr_plan plan ON plan.idobj = resnum.plan_id,
    infolica.cadastre cad,
    infolica.numero_type numt,
    infolica.operateur op
WHERE cad.id = resnum.cadastre_id AND numt.id = resnum.type_id AND op.id = resnum.operateur_id;

alter table infolica.v_reservation_numeros_mo
owner to infolica;
