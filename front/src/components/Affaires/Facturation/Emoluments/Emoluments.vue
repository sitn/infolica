<style src="./emoluments.css" scoped></style>
<template src="./emoluments.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
// import NumerosAffaireVue from '../../NumerosAffaire/NumerosAffaire.vue'
const numeral = require("numeral")

export default {
  name: 'Emoluments',
  props: {
    affaire: {type: Object},
    showEmolumentsDialog: {type: Boolean, default: false}
  },
  data: function () {
      return {
        divers: [],
        emolumentsUnits: [],
        form: {},
        form2: {},
        n_divers: 10,
        enableSave: false,
        indexFromDB: {
          mandat: [1,2,3,4,5,6],
          travauxTerrain: [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
          travauxMaterialisation: [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48],
          deplacementDebours: [49],
          travauxBureau: [50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95],
          registreFoncier: [96,97,98,99,100]
        },
        total: {}
      }
  },

  methods:{
    init2remove() {
      this.form.nb_batiments = 2;
      this.form.batiment_f = [0.8, 1.3];
    },
    
    getEmolumentsUnit() {
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
            this.form2["mandat" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux terrain
          i = 1;
          this.indexFromDB.travauxTerrain.forEach(x => {
            this.form2["travauxTerrain" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux matérialisation
          i = 1;
          this.indexFromDB.travauxMaterialisation.forEach(x => {
            this.form2["travauxMaterialisation" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Déplacements et débours
          i = 1;
          this.indexFromDB.deplacementDebours.forEach(x => {
            this.form2["deplacementDebours" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // Travaux bureau
          i = 1;
          this.indexFromDB.travauxBureau.forEach(x => {
            this.form2["travauxBureau" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          // RF
          i = 1;
          this.indexFromDB.registreFoncier.forEach(x => {
            this.form2["registreFoncier" + String(i)] = {
              tableau_emolument_id: x,
              nom: tmp[x-1].nom,
              unite: tmp[x-1].unite,
              prix_unitaire: Number(tmp[x-1].montant),
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
            i = i+1;
          });

          console.log("this.form2 = ", this.form2)

          // Divers
          for (let i=0; i<this.n_divers; i++) {
            this.form2["divers" + String(i+1)] = {
              tableau_emolument_id: null,
              nom: null,
              unite: "Heure",
              prix_unitaire: null,
              nombre: 0,
              batiment: null,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
          }

          this.emolumentsUnits = tmp;

        }
      }).catch(err => handleException(err, this));
    },


    async initForm() {
      await this.getEmolumentsUnit();

      this.form = {
        affaire_id: this.affaire.id,
        plans_folio: null,
        parcelles: null,
        echelle: null,
        technicien: this.affaire.technicien_id,
        nb_pfp3_hors_mutation: null,
        pente: 0,
        visibilite: 0,
        trafic: 0,
        zi: 1,
        nb_batiments: 0,
        indice_application: 1.22,
        indice_tva: 7.7, // %
        remarque: "",
        montant_relations_autres_services: numeral(0).format("0.00"),

        montant_recapitulatif_mandat: 0,
        montant_recapitulatif_terrain_materialisation_deplacements: 0,
        montant_recapitulatif_bureau: 0,
        montant_recapitulatif_indice_application: 0,
        montant_recapitulatif_materiel_divers: 0,
        montant_recapitulatif_matdiff: 0,
        montant_recapitulatif_tva: 0,
        montant_recapitulatif_registre_foncier: 0,
        montant_recapitulatif_somme1: 0,
        montant_recapitulatif_somme2: 0,
        montant_recapitulatif_somme3: 0,
        montant_recapitulatif_somme4: 0,
        montant_recapitulatif_somme5: 0,
        montant_recapitulatif_somme6: 0,
        montant_recapitulatif_somme7: 0,
        montant_recapitulatif_total: 0,

        // Bâtiments
        batiment_f: [],
      };


      this.total = {
        montant_mandat_total: 0,
        montant_21pfp: 0,
        montant_23sit: 0,
        montant_22pl: 0,
        montant_travauxTerrain_total: 0,
        montant_travauxTerrain_total_zi: 0,
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
        montant_travauxBureau_batiment_total_f_somme: 0,
        montant_divers_total: 0,
      };

      this.setComptabiliteFormat();

      // **************************************************** 2 REMOVE - start **********************************************
      // this.init2remove();
      // **************************************************** 2 REMOVE - end **********************************************
      
      this.computeZi();
      // this.updateNbBatiments();
      this.updateRecapitulatif();
    },

    
    /**
     * update nb bâtiments
     */
    updateNbBatiments() {
      // Facteur de correction
      this.form.batiment_f = new Array(Number(this.form.nb_batiments));
      // Mandats
      this.form.nb_mandat2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_mandat3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_mandat6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_mandat2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_mandat3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_mandat6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_mandat_batiment_total = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_mandat_batiment_total_f = new Array(Number(this.form.nb_batiments)).fill(0);
      // Travaux terrain
      this.form.nb_travauxTerrain1_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain4_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain5_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain7_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain8_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain9_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain10_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain11_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain12_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain13_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain14_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain15_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxTerrain16_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain1_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain4_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain5_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain7_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain8_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain9_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain10_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain11_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain12_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain13_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain14_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain15_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain16_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain_batiment_total = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain_batiment_total_f = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxTerrain_batiment_total_f_somme = 0;
      this.form.montant_travauxTerrain_batiment_total_f_somme_zi = 0;
      // Travaux bureau
      this.form.nb_travauxBureau1_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau4_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau5_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau7_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau8_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau9_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau10_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau11_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau12_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau13_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau14_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau15_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau16_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau17_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau18_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau19_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau20_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau21_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau22_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau23_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau24_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau25_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau26_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.nb_travauxBureau27_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau1_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau2_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau3_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau4_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau5_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau6_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau7_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau8_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau9_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau10_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau11_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau12_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau13_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau14_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau15_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau16_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau17_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau18_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau19_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau20_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau21_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau22_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau23_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau24_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau25_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau26_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau27_batiment = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau_batiment_total = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau_batiment_total_f = new Array(Number(this.form.nb_batiments)).fill(0);
      this.form.montant_travauxBureau_batiment_total_f_somme = 0;
    },


    /**
     * Update value of zi
     */
    computeZi() {
      this.form.zi = numeral(
        1 + 
        Number(this.form.pente) / 100 +
        Number(this.form.visibilite) + 
        Number(this.form.trafic)
      ).format("0.00");

      this.computeAll();
    },

    /**
     * Update montants
     */
    updateMontants() {
      //form
      for (let key in this.form2) {
        console.log("key = ", key)
        this.form2[key].montant = numeral(Number(this.form2[key].nombre) * Number(this.form2[key].prix_unitaire)).format("0.00");
      }
      //update format montant_relation_autres_services
      this.form.montant_relations_autres_services = numeral(this.form.montant_relations_autres_services).format("0.00");

      // update montant_total par categorie
      //Montants totaux Mandat
      this.total.montant_mandat_total = 
        Number(this.form2.mandat1.montant) +
        Number(this.form2.mandat2.montant) +
        Number(this.form2.mandat3.montant) +
        Number(this.form2.mandat4.montant) +
        Number(this.form2.mandat5.montant) +
        Number(this.form2.mandat6.montant);

      //Montants totaux TravauxTerrain
      this.total.montant_21pfp = 
        Number(this.form2.travauxTerrain1.montant) +
        Number(this.form2.travauxTerrain2.montant) +
        Number(this.form2.travauxTerrain3.montant) +
        Number(this.form2.travauxTerrain4.montant) +
        Number(this.form2.travauxTerrain5.montant) +
        Number(this.form2.travauxTerrain6.montant) +
        Number(this.form2.travauxTerrain7.montant) +
        Number(this.form2.travauxTerrain8.montant) +
        Number(this.form2.travauxTerrain9.montant) +
        Number(this.form2.travauxTerrain10.montant) +
        Number(this.form2.travauxTerrain11.montant) +
        Number(this.form2.travauxTerrain12.montant) +
        Number(this.form2.travauxTerrain13.montant) +
        Number(this.form2.travauxTerrain14.montant);
      
      this.total.montant_23sit = 
        Number(this.form2.travauxTerrain15.montant) +
        Number(this.form2.travauxTerrain16.montant);
      
      this.total.montant_22pl = 
        Number(this.form2.travauxTerrain17.montant) +
        Number(this.form2.travauxTerrain18.montant) +
        Number(this.form2.travauxTerrain19.montant) +
        Number(this.form2.travauxTerrain20.montant) +
        Number(this.form2.travauxTerrain21.montant) +
        Number(this.form2.travauxTerrain22.montant) +
        Number(this.form2.travauxTerrain23.montant) +
        Number(this.form2.travauxTerrain24.montant) +
        Number(this.form2.travauxTerrain25.montant);
      
      this.total.montant_travauxTerrain_total = 
        Number(this.total.montant_21pfp) +
        Number(this.total.montant_23sit) +
        Number(this.total.montant_22pl);

      this.total.montant_travauxTerrain_total_zi =
        Number(this.total.montant_travauxTerrain_total) * Number(this.form.zi);

      //Montants totaux TravauxMatérialisation
      this.total.montant_31_32_std_compl = 
        Number(this.form2.travauxMaterialisation1.montant) +
        Number(this.form2.travauxMaterialisation2.montant) +
        Number(this.form2.travauxMaterialisation3.montant) +
        Number(this.form2.travauxMaterialisation4.montant) +
        Number(this.form2.travauxMaterialisation5.montant) +
        Number(this.form2.travauxMaterialisation6.montant) +
        Number(this.form2.travauxMaterialisation7.montant);
      
      this.total.montant_31_32_std_compl_zi = 
        this.total.montant_31_32_std_compl * Number(this.form.zi);

      this.total.montant_33_materiel = 
        Number(this.form2.travauxMaterialisation8.montant) +
        Number(this.form2.travauxMaterialisation9.montant) +
        Number(this.form2.travauxMaterialisation10.montant) +
        Number(this.form2.travauxMaterialisation11.montant) +
        Number(this.form2.travauxMaterialisation12.montant) +
        Number(this.form2.travauxMaterialisation13.montant);
      
      this.total.montant_34_matdiff = 
        Number(this.form2.travauxMaterialisation14.montant) +
        Number(this.form2.travauxMaterialisation15.montant) +
        Number(this.form2.travauxMaterialisation16.montant) +
        Number(this.form2.travauxMaterialisation17.montant);
      
      this.total.montant_5_depl_debours = 
        Number(this.form2.deplacementDebours1.montant);
      
      this.total.montant_travauxMaterialisation_total = 
        Number(this.total.montant_31_32_std_compl_zi) +
        Number(this.total.montant_33_materiel) +
        Number(this.total.montant_34_matdiff) +
        Number(this.total.montant_5_depl_debours);

      //Montants totaux TravauxBureau
      this.total.montant_41pfp = 
        Number(this.form2.travauxBureau1.montant) +
        Number(this.form2.travauxBureau2.montant) +
        Number(this.form2.travauxBureau3.montant) +
        Number(this.form2.travauxBureau4.montant) +
        Number(this.form2.travauxBureau5.montant) +
        Number(this.form2.travauxBureau6.montant) +
        Number(this.form2.travauxBureau7.montant) +
        Number(this.form2.travauxBureau8.montant) +
        Number(this.form2.travauxBureau9.montant) +
        Number(this.form2.travauxBureau10.montant) +
        Number(this.form2.travauxBureau11.montant) +
        Number(this.form2.travauxBureau12.montant);
      
      this.total.montant_43sit = 
        Number(this.form2.travauxBureau13.montant) +
        Number(this.form2.travauxBureau14.montant) +
        Number(this.form2.travauxBureau15.montant) +
        Number(this.form2.travauxBureau16.montant) +
        Number(this.form2.travauxBureau17.montant) +
        Number(this.form2.travauxBureau18.montant) +
        Number(this.form2.travauxBureau19.montant) +
        Number(this.form2.travauxBureau20.montant) +
        Number(this.form2.travauxBureau21.montant) +
        Number(this.form2.travauxBureau22.montant);
      
      this.total.montant_44surf = 
        Number(this.form2.travauxBureau23.montant) +
        Number(this.form2.travauxBureau24.montant) +
        Number(this.form2.travauxBureau25.montant) +
        Number(this.form2.travauxBureau26.montant) +
        Number(this.form2.travauxBureau27.montant);
      
      this.total.montant_42pl = 
        Number(this.form2.travauxBureau28.montant) +
        Number(this.form2.travauxBureau29.montant) +
        Number(this.form2.travauxBureau30.montant) +
        Number(this.form2.travauxBureau31.montant) +
        Number(this.form2.travauxBureau32.montant) +
        Number(this.form2.travauxBureau33.montant) +
        Number(this.form2.travauxBureau34.montant) +
        Number(this.form2.travauxBureau35.montant) +
        Number(this.form2.travauxBureau36.montant) +
        Number(this.form2.travauxBureau37.montant) +
        Number(this.form2.travauxBureau38.montant) +
        Number(this.form2.travauxBureau39.montant) +
        Number(this.form2.travauxBureau40.montant) +
        Number(this.form2.travauxBureau41.montant) +
        Number(this.form2.travauxBureau42.montant) +
        Number(this.form2.travauxBureau43.montant) +
        Number(this.form2.travauxBureau44.montant) +
        Number(this.form2.travauxBureau45.montant) +
        Number(this.form2.travauxBureau46.montant);

      this.total.montant_travauxBureau_total = 
        Number(this.total.montant_41pfp) +
        Number(this.total.montant_43sit) +
        Number(this.total.montant_44surf) +
        Number(this.total.montant_42pl);

      this.total.montant_divers_total = 
        Number(this.form2.divers1.montant) +
        Number(this.form2.divers2.montant) +
        Number(this.form2.divers3.montant) +
        Number(this.form2.divers4.montant) +
        Number(this.form2.divers5.montant) +
        Number(this.form2.divers6.montant) +
        Number(this.form2.divers7.montant) +
        Number(this.form2.divers8.montant) +
        Number(this.form2.divers9.montant) +
        Number(this.form2.divers10.montant) +
        Number(this.form.montant_relations_autres_services);


      this.setComptabiliteFormat();
    },


    updateMontantDivers() {
      this.form.montant_divers_total = 0;
      for (let i=0; i<this.n_divers; i++) {
        if (this.form.nb_divers[i] && this.form.divers_prix_unitaire[i] && Number(this.form.nb_divers[i]) >= 0 && Number(this.form.divers_prix_unitaire[i]) >= 0) {
          this.form.montant_divers[i] = Number(this.form.nb_divers[i]) * Number(this.form.divers_prix_unitaire[i]);
          this.form.montant_divers_total += Number(this.form.montant_divers[i]);
        }
      }
      this.form.montant_divers_total += Number(this.form.montant_relations_autres_services);
      
      this.updateRecapitulatif();
    },

    updateRecapitulatif() {
      this.form.montant_recapitulatif_mandat = Number(this.form.montant_mandat_total) + this.form.montant_mandat_batiment_total_f.length > 0? Number(this.form.montant_mandat_batiment_total_f.reduce((a, b) => Number(a) + Number(b))): 0;
      this.form.montant_recapitulatif_somme1 = Number(this.form.montant_recapitulatif_mandat)

      this.form.montant_recapitulatif_terrain_materialisation_deplacements = Number(this.form.montant_travauxTerrain_total_zi) + Number(this.form.montant_travauxTerrain_batiment_total_f_somme_zi) + Number(this.form.montant_5_depl_debours);
      this.form.montant_recapitulatif_somme2 = Number(this.form.montant_recapitulatif_somme1) + Number(this.form.montant_recapitulatif_terrain_materialisation_deplacements);

      this.form.montant_recapitulatif_bureau = Number(this.form.montant_travauxBureau_total) + Number(this.form.montant_travauxBureau_batiment_total_f_somme);
      this.form.montant_recapitulatif_somme3 = Number(this.form.montant_recapitulatif_somme2) + Number(this.form.montant_recapitulatif_bureau);

      this.form.montant_recapitulatif_indice_application = this.round( Number(this.form.montant_recapitulatif_somme3) * (Number(this.form.indice_application) - 1));
      this.form.montant_recapitulatif_somme4 = Number(this.form.montant_recapitulatif_somme3) + Number(this.form.montant_recapitulatif_indice_application);

      this.form.montant_recapitulatif_materiel_divers = Number(this.form.montant_33_materiel) + Number(this.form.montant_divers_total);
      this.form.montant_recapitulatif_somme5 = Number(this.form.montant_recapitulatif_somme4) + Number(this.form.montant_recapitulatif_materiel_divers);

      this.form.montant_recapitulatif_matdiff = this.round( Number(this.form.montant_34_matdiff) * Number(this.form.indice_application));
      this.form.montant_recapitulatif_somme6 = Number(this.form.montant_recapitulatif_somme5) + Number(this.form.montant_recapitulatif_matdiff);

      this.form.montant_recapitulatif_tva = this.round(Number(this.form.montant_recapitulatif_somme6) * Number(this.form.indice_tva) / 100, 0.05);
      this.form.montant_recapitulatif_somme7 = this.form.montant_recapitulatif_somme6 + Number(this.form.montant_recapitulatif_tva);

      this.form.montant_recapitulatif_registre_foncier = Number(this.form.montant_rf_total);

      this.form.montant_recapitulatif_total = Number(this.form.montant_recapitulatif_somme7) + Number(this.form.montant_recapitulatif_registre_foncier);

      this.setComptabiliteFormat();
    },


    /**
     * Compute all
     */
    computeAll() {
      this.updateMontants();
    },

    /** Set format for comptabilité: 0.00 CHF */
    setComptabiliteFormat() {
      Object.keys(this.total).forEach(x => this.total[x] = numeral(this.total[x]).format("0.00"));
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
      let formData = new FormData();
      formData.append('form', this.form);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENTS_FACTURE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.$root.$emit("ShowMessage", "Le formulaire a été enregistré correctment");
        }
      }).catch(err => handleException(err, this)); 
    },

    /**
     * form to array of objects
     */
    form2ArrayObj() {
      let form_ = [];
      for (const key in Object.keys(this.form)) {
        if (key.startsWith("montant_") && Number(this.form[key]) > 0) {
          form_.push({

          });
        }
      }

    }


  },

  mounted: function(){
    this.initForm();
    // this.getEmolumentsUnit();
  }
}
</script>

