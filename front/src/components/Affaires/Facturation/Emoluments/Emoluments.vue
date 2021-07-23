<style src="./emoluments.css" scoped></style>
<template src="./emoluments.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler';
const numeral = require("numeral");

export default {
  name: 'Emoluments',
  props: {
    affaire: {type: Object},
  },
  data: function () {
      return {
        divers: [],
        emolumentsUnits: [],
        form_general: {}, //général
        form_detail: {}, //emoluments sans bâtiment
        form_detail_batiment: [], //emoluments avec bâtiments
        n_divers: 10,
        enableSave: false,
        indexFromDB: {
          mandat: [1,2,3,4,5,6],
          travauxTerrain: [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
          travauxMaterialisation: [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48],
          deplacementDebours: [49],
          travauxBureau: [50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95],
          registreFoncier: [96,97,98,99,100],
          divers: 101,
          relations_autres_services: 102,
          forfait_rf: 103
        },
        showEmolumentsDialog: true,
        total: {}
      }
  },

  methods:{
    fillFakeValues() {

      for (let i=0; i<3; i++){
        // mandat
        let idx = Math.ceil(Math.random() * this.indexFromDB.mandat.length);
        let idx2 = Math.floor(Math.random() * this.form_general.nb_batiments);
        this.form_detail["mandat"+String(idx)].nombre = 1;
        if (this.form_general.nb_batiments>0) this.form_detail_batiment[idx2]["mandat"+String(idx)].nombre = 1;
        // travauxTerrain
        idx = Math.ceil(Math.random() * this.indexFromDB.travauxTerrain.length);
        idx2 = Math.floor(Math.random() * this.form_general.nb_batiments);
        this.form_detail["travauxTerrain"+String(idx)].nombre = 1;
        if (this.form_general.nb_batiments>0) this.form_detail_batiment[idx2]["travauxTerrain"+String(idx)].nombre = 1;
        // travauxMaterialisation
        idx = Math.ceil(Math.random() * this.indexFromDB.travauxMaterialisation.length);
        this.form_detail["travauxMaterialisation"+String(idx)].nombre = 1;
        // travauxBureau
        idx = Math.ceil(Math.random() * this.indexFromDB.travauxBureau.length);
        idx2 = Math.floor(Math.random() * this.form_general.nb_batiments);
        this.form_detail["travauxBureau"+String(idx)].nombre = 1;
        if (this.form_general.nb_batiments>0) this.form_detail_batiment[idx2]["travauxBureau"+String(idx)].nombre = 1;
        // registreFoncier
        idx = Math.ceil(Math.random() * this.indexFromDB.registreFoncier.length);
        this.form_detail["registreFoncier"+String(idx)].nombre = 1;
      }
      this.form_detail.divers1.nombre = 1;
      this.form_detail.divers1.montant = 182;
      this.form_detail.divers1.prix_unitaire = 182;
      this.form_detail.divers1.nom = "test";

      this.updateMontants();
    },
    
    /**
     * Get emoluments units from DB
     */
    async getEmolumentsUnit() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENTS_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          tmp.forEach(x => x.montant = Number(x.montant));

          // Mandat
          let i = 1;
          this.indexFromDB.mandat.forEach(x => {
            this.form_detail["mandat" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux terrain
          i = 1;
          this.indexFromDB.travauxTerrain.forEach(x => {
            this.form_detail["travauxTerrain" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux matérialisation
          i = 1;
          this.indexFromDB.travauxMaterialisation.forEach(x => {
            this.form_detail["travauxMaterialisation" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Déplacements et débours
          i = 1;
          this.indexFromDB.deplacementDebours.forEach(x => {
            this.form_detail["deplacementDebours" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux bureau
          i = 1;
          this.indexFromDB.travauxBureau.forEach(x => {
            this.form_detail["travauxBureau" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // RF
          i = 1;
          this.indexFromDB.registreFoncier.forEach(x => {
            this.form_detail["registreFoncier" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Divers
          for (let i=0; i<this.n_divers; i++) {
            this.form_detail["divers" + String(i+1)] = {
              tableau_emolument_id: this.indexFromDB.divers,
              nom: null,
              unite: "Heure",
              prix_unitaire: null,
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
          }

          //relations avec autres services
          this.form_detail["relations_autres_services1"] = {
            tableau_emolument_id: this.indexFromDB.relations_autres_services,
            nom: "Relations avec d'autres services (de 50.00 à 200.00 CHF)",
            unite: "-",
            prix_unitaire: numeral(0).format("0.00"),
            nombre: 1,
            batiment: 0,
            batiment_f: 1,
            montant: numeral(0).format("0.00"),
          }

          //forfait RF
          this.form_detail["forfait_rf1"] = {
            tableau_emolument_id: this.indexFromDB.divers,
            nom: "Forfait RF",
            unite: "-",
            prix_unitaire: numeral(0).format("0.00"),
            nombre: 1,
            batiment: 0,
            batiment_f: 1,
            montant: numeral(0).format("0.00"),
          }

          this.emolumentsUnits = tmp;

          this.initForm();

        }
      }).catch(err => handleException(err, this));
    },


    async initForm() {
      this.form_general = {
        affaire_id: this.affaire.id,
        pente_pc: 0,
        diff_visibilite_pc: 0,
        trafic_pc: 0,
        zi: 1,
        nb_batiments: 0,
        indice_application: 1.22,
        tva_pc: 7.7, // %
        remarque: "",

        // Bâtiments
        batiment_f: [],
      };


      this.total = {
        montant_mandat_total: 0,
        montant_mandat_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_mandat_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_21pfp: 0,
        montant_23sit: 0,
        montant_22pl: 0,
        montant_travauxTerrain_total: 0,
        montant_travauxTerrain_total_zi: 0,
        montant_travauxTerrain_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxTerrain_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxTerrain_batiment_total_f_somme: 0,
        montant_travauxTerrain_batiment_total_f_somme_zi: 0,
        montant_31_32_std_compl: 0,
        montant_31_32_std_compl_zi: 0,
        montant_33_materiel: 0,
        montant_34_matdiff: 0,
        montant_5_depl_debours: 0,
        montant_travauxMaterialisation_total: 0,
        montant_41pfp: 0,
        montant_43sit: 0,
        montant_44surf: 0,
        montant_42pl: 0,
        montant_travauxBureau_total: 0,
        montant_travauxBureau_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxBureau_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxBureau_batiment_total_f_somme: 0,
        montant_divers_total: 0,
        montant_rf_total: 0,
        montant_recapitulatif_mandat: 0,
        montant_recapitulatif_somme1: 0,
        montant_recapitulatif_terrain_materialisation_deplacements: 0,
        montant_recapitulatif_somme2: 0,
        montant_recapitulatif_bureau: 0,
        montant_recapitulatif_somme3: 0,
        montant_recapitulatif_indice_application: 0,
        montant_recapitulatif_somme4: 0,
        montant_recapitulatif_materiel_divers: 0,
        montant_recapitulatif_somme5: 0,
        montant_recapitulatif_matdiff: 0,
        montant_recapitulatif_somme6: 0,
        montant_recapitulatif_tva: 0,
        montant_recapitulatif_somme7: 0,
        montant_recapitulatif_registre_foncier: 0,
        montant_recapitulatif_total: 0,
        montant_divers_total_with_5_depl_debours: 0,
      };

      this.computeZi();
      this.updateRecapitulatif();
    },

    /**
     * Add batiment
     */
    addBatiment() {
      this.form_general.nb_batiments += 1;

      for (let i=0; i<Number(this.form_general.nb_batiments); i++)  {
        this.form_detail_batiment.push( JSON.parse( JSON.stringify(this.form_detail)) );
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].batiment = i+1;
          this.form_detail_batiment[i][key].montant = numeral(0).format("0.00");
          this.form_detail_batiment[i][key].nombre = 0;
          this.form_detail_batiment[i][key].batiment_f = this.form_general.batiment_f[i];
        }
      }
    },

    /**
     * Remove batiment
     */
    removeBatiment(batiment_i) {
      let tmp = [];
      let c = 1; // renumérotation bâtiment
      for (let i=0; i<this.form_general.nb_batiments; i++) {
        if (this.form_detail_batiment[i]['mandat1'].batiment !== batiment_i) {
          for (let key in this.form_detail_batiment[i]) {
            this.form_detail_batiment[i][key].batiment = c;
          }
          tmp.push(this.form_detail_batiment[i]);
          c += 1;
        }
      }

      this.form_detail_batiment = JSON.parse(JSON.stringify(tmp));
      this.form_general.batiment_f.splice(batiment_i-1,1);
      this.form_general.nb_batiments -= 1;
    },


    /**
     * Update batimentCorrectionFactor
     */
    updateBatimentCorrectionFactor() {
      for (let i=0; i<Number(this.form_general.nb_batiments); i++) {
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].batiment_f = Number(this.form_general.batiment_f[i]);
        }
      }

      this.updateMontants();
    },


    /**
     * Update value of zi
     */
    computeZi() {
      this.form_general.zi = numeral(
        1 + 
        Number(this.form_general.pente_pc) / 100 +
        Number(this.form_general.diff_visibilite_pc) + 
        Number(this.form_general.trafic_pc)
      ).format("0.00");
    },

    /**
     * Update montants
     */
    updateMontants() {
      //form_detail
      for (let key in this.form_detail) {
        this.form_detail[key].montant = numeral(Number(this.form_detail[key].nombre) * Number(this.form_detail[key].prix_unitaire)).format("0.00");
      }
         
      //form_detail_batiment
      for (let i=0; i<Number(this.form_general.nb_batiments); i++) {
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].montant = numeral(Number(this.form_detail_batiment[i][key].nombre) * Number(this.form_detail_batiment[i][key].prix_unitaire)).format("0.00");
        }
      }
      
      // cas particuliers relations_autres_services et forfait_rf
      this.form_detail.relations_autres_services1.prix_unitaire = numeral(this.form_detail.relations_autres_services1.prix_unitaire).format("0.00");
      this.form_detail.forfait_rf1.prix_unitaire = numeral(this.form_detail.forfait_rf1.prix_unitaire).format("0.00");
      

      // update montant_total par categorie
      //Montants totaux Mandat
      this.total.montant_mandat_total = 
        Number(this.form_detail.mandat1.montant) +
        Number(this.form_detail.mandat2.montant) +
        Number(this.form_detail.mandat3.montant) +
        Number(this.form_detail.mandat4.montant) +
        Number(this.form_detail.mandat5.montant) +
        Number(this.form_detail.mandat6.montant);

      for (let j=0; j<Number(this.form_general.nb_batiments); j++) {
        // Mandat
        this.total.montant_mandat_batiment_total[j] = 
          Number(this.form_detail_batiment[j].mandat1.montant) +
          Number(this.form_detail_batiment[j].mandat2.montant) +
          Number(this.form_detail_batiment[j].mandat3.montant) +
          Number(this.form_detail_batiment[j].mandat4.montant) +
          Number(this.form_detail_batiment[j].mandat5.montant) +
          Number(this.form_detail_batiment[j].mandat6.montant);

        this.total.montant_mandat_batiment_total_f[j] =
          Number(this.total.montant_mandat_batiment_total[j]) * Number(this.form_general.batiment_f[j]);
      
        // Travaux terrain
        this.total.montant_travauxTerrain_batiment_total[j] =
          Number(this.form_detail_batiment[j].travauxTerrain1.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain2.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain3.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain4.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain5.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain6.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain7.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain8.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain9.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain10.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain11.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain12.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain13.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain14.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain15.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain16.montant);

        this.total.montant_travauxTerrain_batiment_total_f[j] =
          Number(this.total.montant_travauxTerrain_batiment_total[j]) * Number(this.form_general.batiment_f[j]);

        // Travaux bureau
        this.total.montant_travauxBureau_batiment_total[j] =
          Number(this.form_detail_batiment[j].travauxBureau1.montant) +
          Number(this.form_detail_batiment[j].travauxBureau2.montant) +
          Number(this.form_detail_batiment[j].travauxBureau3.montant) +
          Number(this.form_detail_batiment[j].travauxBureau4.montant) +
          Number(this.form_detail_batiment[j].travauxBureau5.montant) +
          Number(this.form_detail_batiment[j].travauxBureau6.montant) +
          Number(this.form_detail_batiment[j].travauxBureau7.montant) +
          Number(this.form_detail_batiment[j].travauxBureau8.montant) +
          Number(this.form_detail_batiment[j].travauxBureau9.montant) +
          Number(this.form_detail_batiment[j].travauxBureau10.montant) +
          Number(this.form_detail_batiment[j].travauxBureau11.montant) +
          Number(this.form_detail_batiment[j].travauxBureau12.montant) +
          Number(this.form_detail_batiment[j].travauxBureau13.montant) +
          Number(this.form_detail_batiment[j].travauxBureau14.montant) +
          Number(this.form_detail_batiment[j].travauxBureau15.montant) +
          Number(this.form_detail_batiment[j].travauxBureau16.montant) +
          Number(this.form_detail_batiment[j].travauxBureau17.montant) +
          Number(this.form_detail_batiment[j].travauxBureau18.montant) +
          Number(this.form_detail_batiment[j].travauxBureau19.montant) +
          Number(this.form_detail_batiment[j].travauxBureau20.montant) +
          Number(this.form_detail_batiment[j].travauxBureau21.montant) +
          Number(this.form_detail_batiment[j].travauxBureau22.montant) +
          Number(this.form_detail_batiment[j].travauxBureau23.montant) +
          Number(this.form_detail_batiment[j].travauxBureau24.montant) +
          Number(this.form_detail_batiment[j].travauxBureau25.montant) +
          Number(this.form_detail_batiment[j].travauxBureau26.montant) +
          Number(this.form_detail_batiment[j].travauxBureau27.montant);

        this.total.montant_travauxBureau_batiment_total_f[j] =
          Number(this.total.montant_travauxBureau_batiment_total[j]) * Number(this.form_general.batiment_f[j]);
      }

      //Montants totaux TravauxTerrain
      this.total.montant_21pfp = 
        Number(this.form_detail.travauxTerrain1.montant) +
        Number(this.form_detail.travauxTerrain2.montant) +
        Number(this.form_detail.travauxTerrain3.montant) +
        Number(this.form_detail.travauxTerrain4.montant) +
        Number(this.form_detail.travauxTerrain5.montant) +
        Number(this.form_detail.travauxTerrain6.montant) +
        Number(this.form_detail.travauxTerrain7.montant) +
        Number(this.form_detail.travauxTerrain8.montant) +
        Number(this.form_detail.travauxTerrain9.montant) +
        Number(this.form_detail.travauxTerrain10.montant) +
        Number(this.form_detail.travauxTerrain11.montant) +
        Number(this.form_detail.travauxTerrain12.montant) +
        Number(this.form_detail.travauxTerrain13.montant) +
        Number(this.form_detail.travauxTerrain14.montant);
      
      this.total.montant_23sit = 
        Number(this.form_detail.travauxTerrain15.montant) +
        Number(this.form_detail.travauxTerrain16.montant);
      
      this.total.montant_22pl = 
        Number(this.form_detail.travauxTerrain17.montant) +
        Number(this.form_detail.travauxTerrain18.montant) +
        Number(this.form_detail.travauxTerrain19.montant) +
        Number(this.form_detail.travauxTerrain20.montant) +
        Number(this.form_detail.travauxTerrain21.montant) +
        Number(this.form_detail.travauxTerrain22.montant) +
        Number(this.form_detail.travauxTerrain23.montant) +
        Number(this.form_detail.travauxTerrain24.montant) +
        Number(this.form_detail.travauxTerrain25.montant);
      
      this.total.montant_travauxTerrain_total = 
        Number(this.total.montant_21pfp) +
        Number(this.total.montant_23sit) +
        Number(this.total.montant_22pl);

      this.total.montant_travauxTerrain_total_zi =
        Number(this.total.montant_travauxTerrain_total) * Number(this.form_general.zi);

      this.total.montant_travauxTerrain_batiment_total_f_somme =
        this.form_general.nb_batiments>0? Number(this.total.montant_travauxTerrain_batiment_total_f.reduce((a, b) => Number(a) + Number(b))): 0;

      this.total.montant_travauxTerrain_batiment_total_f_somme_zi =
        Number(this.total.montant_travauxTerrain_batiment_total_f_somme) * Number(this.form_general.zi);

      //Montants totaux TravauxMatérialisation
      this.total.montant_31_32_std_compl = 
        Number(this.form_detail.travauxMaterialisation1.montant) +
        Number(this.form_detail.travauxMaterialisation2.montant) +
        Number(this.form_detail.travauxMaterialisation3.montant) +
        Number(this.form_detail.travauxMaterialisation4.montant) +
        Number(this.form_detail.travauxMaterialisation5.montant) +
        Number(this.form_detail.travauxMaterialisation6.montant) +
        Number(this.form_detail.travauxMaterialisation7.montant);
      
      this.total.montant_31_32_std_compl_zi = 
        this.total.montant_31_32_std_compl * Number(this.form_general.zi);

      this.total.montant_33_materiel = 
        Number(this.form_detail.travauxMaterialisation8.montant) +
        Number(this.form_detail.travauxMaterialisation9.montant) +
        Number(this.form_detail.travauxMaterialisation10.montant) +
        Number(this.form_detail.travauxMaterialisation11.montant) +
        Number(this.form_detail.travauxMaterialisation12.montant) +
        Number(this.form_detail.travauxMaterialisation13.montant);
      
      this.total.montant_5_depl_debours = 
        Number(this.form_detail.deplacementDebours1.montant);
      
      this.total.montant_travauxMaterialisation_total = 
        Number(this.total.montant_31_32_std_compl_zi) +
        Number(this.total.montant_33_materiel) +
        Number(this.total.montant_34_matdiff);

      //Montants totaux TravauxBureau
      this.total.montant_41pfp = 
        Number(this.form_detail.travauxBureau1.montant) +
        Number(this.form_detail.travauxBureau2.montant) +
        Number(this.form_detail.travauxBureau3.montant) +
        Number(this.form_detail.travauxBureau4.montant) +
        Number(this.form_detail.travauxBureau5.montant) +
        Number(this.form_detail.travauxBureau6.montant) +
        Number(this.form_detail.travauxBureau7.montant) +
        Number(this.form_detail.travauxBureau8.montant) +
        Number(this.form_detail.travauxBureau9.montant) +
        Number(this.form_detail.travauxBureau10.montant) +
        Number(this.form_detail.travauxBureau11.montant) +
        Number(this.form_detail.travauxBureau12.montant);
      
      this.total.montant_43sit = 
        Number(this.form_detail.travauxBureau13.montant) +
        Number(this.form_detail.travauxBureau14.montant) +
        Number(this.form_detail.travauxBureau15.montant) +
        Number(this.form_detail.travauxBureau16.montant) +
        Number(this.form_detail.travauxBureau17.montant) +
        Number(this.form_detail.travauxBureau18.montant) +
        Number(this.form_detail.travauxBureau19.montant) +
        Number(this.form_detail.travauxBureau20.montant) +
        Number(this.form_detail.travauxBureau21.montant) +
        Number(this.form_detail.travauxBureau22.montant);
      
      this.total.montant_44surf = 
        Number(this.form_detail.travauxBureau23.montant) +
        Number(this.form_detail.travauxBureau24.montant) +
        Number(this.form_detail.travauxBureau25.montant) +
        Number(this.form_detail.travauxBureau26.montant) +
        Number(this.form_detail.travauxBureau27.montant);
      
      this.total.montant_42pl = 
        Number(this.form_detail.travauxBureau28.montant) +
        Number(this.form_detail.travauxBureau29.montant) +
        Number(this.form_detail.travauxBureau30.montant) +
        Number(this.form_detail.travauxBureau31.montant) +
        Number(this.form_detail.travauxBureau32.montant) +
        Number(this.form_detail.travauxBureau33.montant) +
        Number(this.form_detail.travauxBureau34.montant) +
        Number(this.form_detail.travauxBureau35.montant) +
        Number(this.form_detail.travauxBureau36.montant) +
        Number(this.form_detail.travauxBureau37.montant) +
        Number(this.form_detail.travauxBureau38.montant) +
        Number(this.form_detail.travauxBureau39.montant) +
        Number(this.form_detail.travauxBureau40.montant) +
        Number(this.form_detail.travauxBureau41.montant) +
        Number(this.form_detail.travauxBureau42.montant) +
        Number(this.form_detail.travauxBureau43.montant) +
        Number(this.form_detail.travauxBureau44.montant) +
        Number(this.form_detail.travauxBureau45.montant) +
        Number(this.form_detail.travauxBureau46.montant);

      this.total.montant_travauxBureau_total = 
        Number(this.total.montant_41pfp) +
        Number(this.total.montant_43sit) +
        Number(this.total.montant_44surf) +
        Number(this.total.montant_42pl);

      this.total.montant_travauxBureau_batiment_total_f_somme = 
        this.form_general.nb_batiments>0? Number(this.total.montant_travauxBureau_batiment_total_f.reduce((a, b) => Number(a) + Number(b))): 0;

      //Divers
      this.total.montant_divers_total = 
        Number(this.form_detail.divers1.montant) +
        Number(this.form_detail.divers2.montant) +
        Number(this.form_detail.divers3.montant) +
        Number(this.form_detail.divers4.montant) +
        Number(this.form_detail.divers5.montant) +
        Number(this.form_detail.divers6.montant) +
        Number(this.form_detail.divers7.montant) +
        Number(this.form_detail.divers8.montant) +
        Number(this.form_detail.divers9.montant) +
        Number(this.form_detail.divers10.montant) +
        Number(this.form_detail.relations_autres_services1.montant);

      this.total.montant_divers_total_with_5_depl_debours = 
        Number(this.total.montant_divers_total) +
        Number(this.total.montant_5_depl_debours);
      
      //Registre foncier
      this.total.montant_rf_total =
        Number(this.form_detail.registreFoncier1.montant) +
        Number(this.form_detail.registreFoncier2.montant) +
        Number(this.form_detail.registreFoncier3.montant) +
        Number(this.form_detail.registreFoncier4.montant) +
        Number(this.form_detail.registreFoncier5.montant) +
        Number(this.form_detail.forfait_rf1.montant);


      this.updateRecapitulatif();
    },


    updateRecapitulatif() {
      let mandat_batiment = (this.form_general.nb_batiments > 0)? Number(this.total.montant_mandat_batiment_total_f.reduce((a, b) => Number(a) + Number(b))): 0
      this.total.montant_recapitulatif_mandat = Number(this.total.montant_mandat_total) + mandat_batiment;
      this.total.montant_recapitulatif_somme1 = Number(this.total.montant_recapitulatif_mandat)

      this.total.montant_recapitulatif_terrain_materialisation_deplacements = Number(this.total.montant_travauxTerrain_total_zi) + Number(this.total.montant_5_depl_debours) + Number(this.total.montant_travauxTerrain_batiment_total_f_somme_zi);
      this.total.montant_recapitulatif_somme2 = Number(this.total.montant_recapitulatif_somme1) + Number(this.total.montant_recapitulatif_terrain_materialisation_deplacements);

      this.total.montant_recapitulatif_bureau = Number(this.total.montant_travauxBureau_total) + Number(this.total.montant_travauxBureau_batiment_total_f_somme);
      this.total.montant_recapitulatif_somme3 = Number(this.total.montant_recapitulatif_somme2) + Number(this.total.montant_recapitulatif_bureau);

      this.total.montant_recapitulatif_indice_application = this.round( Number(this.total.montant_recapitulatif_somme3) * (Number(this.form_general.indice_application) - 1));
      this.total.montant_recapitulatif_somme4 = Number(this.total.montant_recapitulatif_somme3) + Number(this.total.montant_recapitulatif_indice_application);

      this.total.montant_recapitulatif_materiel_divers = Number(this.total.montant_33_materiel) + Number(this.total.montant_divers_total);
      this.total.montant_recapitulatif_somme5 = Number(this.total.montant_recapitulatif_somme4) + Number(this.total.montant_recapitulatif_materiel_divers);

      this.total.montant_recapitulatif_matdiff = this.round( Number(this.total.montant_34_matdiff) * Number(this.form_general.indice_application));
      this.total.montant_recapitulatif_somme6 = Number(this.total.montant_recapitulatif_somme5) + Number(this.total.montant_recapitulatif_matdiff);

      this.total.montant_recapitulatif_tva = this.round(Number(this.total.montant_recapitulatif_somme6) * Number(this.form_general.tva_pc) / 100, 0.05);
      this.total.montant_recapitulatif_somme7 = this.total.montant_recapitulatif_somme6 + Number(this.total.montant_recapitulatif_tva);

      this.total.montant_recapitulatif_registre_foncier = Number(this.total.montant_rf_total);

      this.total.montant_recapitulatif_total = Number(this.total.montant_recapitulatif_somme7) + Number(this.total.montant_recapitulatif_registre_foncier);

      this.setComptabiliteFormat();
    },

    /** Set format for comptabilité: 0.00 CHF */
    setComptabiliteFormat() {
      Object.keys(this.total).forEach(x => {
        if (Array.isArray(this.total[x])) {
          for (let i=0; i<this.form_general.nb_batiments; i++) {
            this.total[x][i] = numeral(this.total[x][i]).format("0.00");
          }
        } else {
          this.total[x] = numeral(this.total[x]).format("0.00");
        }
      });
    },

    /**
     * Round numbers
     */
    round(num, multiple=0.1) {
      num = Number(num);
      multiple = Number(multiple);
      return Math.round(num / multiple) * multiple;
    },

    /**
     * Event handler when tab changed
     */
    changeHandler(index) {
      this.enableSave = index === this.$refs.tabRecapitulatif.$el.id;
    },


    /**
     * postFormular
     */
    async postEmolument() {
      this.postEmolumentsGeneral().then(response => {
        if (response && response.data) {
          this.postEmolumentsDetail(response.data.emolument_affaire_id).then(response => {
            if (response && response.data) {
              this.showEmolumentsDialog = false;
              this.$root.$emit("ShowMessage", "Le formulaire a été enregistré correctement");
            }
          }).catch(err => handleException(err, this));
        }
      }).catch(err => handleException(err, this));
    },

    async postEmolumentsGeneral() {
      let formData = new FormData();
      formData.append("data", JSON.stringify(this.form_general));

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },

    async postEmolumentsDetail(emolument_affaire_id) {
      let form = this.form_detail_batiment;
      form.push(this.form_detail)

      let formData = new FormData();
      formData.append("data", JSON.stringify(form));
      formData.append("emolument_affaire_id", emolument_affaire_id);

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },

    /**
     * selected option mat diff
     */
    matDiffChanged(montant) {
      let travauxMaterialisation = [
        "travauxMaterialisation14",
        "travauxMaterialisation15",
        "travauxMaterialisation16",
        "travauxMaterialisation17"
      ];
      
      for (let element_i of travauxMaterialisation) {
        if (Number(this.form_detail[element_i].prix_unitaire) === Number(montant)) {
          this.form_detail[element_i].nombre = 1;
          this.form_detail[element_i].montant = montant;
        } else {
          this.form_detail[element_i].nombre = 0;
          this.form_detail[element_i].montant = 0;
        }
      }
      
      this.updateMontants()
    }

  },

  mounted: function(){
    // this.initForm();
    this.getEmolumentsUnit();
  }
}
</script>

