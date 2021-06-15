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
        emolumentsUnits: [],
        form: {},
        n_divers: 10,
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
          this.emolumentsUnits = response.data;
          this.emolumentsUnits.forEach(x => x.montant = Number(x.montant));

          this.computeZi();
        }
      }).catch(err => handleException(err, this));
    },


    initForm() {
      this.form = {
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
        //mandats
        nb_mandat1: 0,
        nb_mandat2: 0,
        nb_mandat3: 0,
        nb_mandat4: 0,
        nb_mandat5: 0,
        nb_mandat6: 0,
        montant_mandat1: 0,
        montant_mandat2: 0,
        montant_mandat3: 0,
        montant_mandat4: 0,
        montant_mandat5: 0,
        montant_mandat6: 0,
        montant_mandat_total: 0,
        montant_mandat2_batiment: [],
        montant_mandat3_batiment: [],
        montant_mandat6_batiment: [],
        montant_mandat_batiment_total: [],
        montant_mandat_batiment_total_f: [],
        //travaux terrain
        nb_travauxTerrain1: 0,
        nb_travauxTerrain2: 0,
        nb_travauxTerrain3: 0,
        nb_travauxTerrain4: 0,
        nb_travauxTerrain5: 0,
        nb_travauxTerrain6: 0,
        nb_travauxTerrain7: 0,
        nb_travauxTerrain8: 0,
        nb_travauxTerrain9: 0,
        nb_travauxTerrain10: 0,
        nb_travauxTerrain11: 0,
        nb_travauxTerrain12: 0,
        nb_travauxTerrain13: 0,
        nb_travauxTerrain14: 0,
        nb_travauxTerrain15: 0,
        nb_travauxTerrain16: 0,
        nb_travauxTerrain17: 0,
        nb_travauxTerrain18: 0,
        nb_travauxTerrain19: 0,
        nb_travauxTerrain20: 0,
        nb_travauxTerrain21: 0,
        nb_travauxTerrain22: 0,
        nb_travauxTerrain23: 0,
        nb_travauxTerrain24: 0,
        nb_travauxTerrain25: 0,
        montant_travauxTerrain1: 0,
        montant_travauxTerrain2: 0,
        montant_travauxTerrain3: 0,
        montant_travauxTerrain4: 0,
        montant_travauxTerrain5: 0,
        montant_travauxTerrain6: 0,
        montant_travauxTerrain7: 0,
        montant_travauxTerrain8: 0,
        montant_travauxTerrain9: 0,
        montant_travauxTerrain10: 0,
        montant_travauxTerrain11: 0,
        montant_travauxTerrain12: 0,
        montant_travauxTerrain13: 0,
        montant_travauxTerrain14: 0,
        montant_travauxTerrain15: 0,
        montant_travauxTerrain16: 0,
        montant_travauxTerrain17: 0,
        montant_travauxTerrain18: 0,
        montant_travauxTerrain19: 0,
        montant_travauxTerrain20: 0,
        montant_travauxTerrain21: 0,
        montant_travauxTerrain22: 0,
        montant_travauxTerrain23: 0,
        montant_travauxTerrain24: 0,
        montant_travauxTerrain25: 0,
        montant_21pfp: 0,
        montant_23sit: 0,
        montant_22pl: 0,
        montant_travauxTerrain_total: 0,
        montant_travauxTerrain_total_zi: 0,
        // Travaux matérialisation
        nb_travauxMaterialisation1: 0,
        nb_travauxMaterialisation2: 0,
        nb_travauxMaterialisation3: 0,
        nb_travauxMaterialisation4: 0,
        nb_travauxMaterialisation5: 0,
        nb_travauxMaterialisation6: 0,
        nb_travauxMaterialisation7: 0,
        nb_travauxMaterialisation8: 0,
        nb_travauxMaterialisation9: 0,
        nb_travauxMaterialisation10: 0,
        nb_travauxMaterialisation11: 0,
        nb_travauxMaterialisation12: 0,
        nb_travauxMaterialisation13: 0,
        nb_travauxMaterialisation14: 0,
        nb_travauxMaterialisation15: 0,
        nb_travauxMaterialisation16: 0,
        nb_travauxMaterialisation17: 0,
        nb_travauxMaterialisation18: 0,
        nb_travauxMaterialisation19: 0,
        montant_travauxMaterialisation1: 0,
        montant_travauxMaterialisation2: 0,
        montant_travauxMaterialisation3: 0,
        montant_travauxMaterialisation4: 0,
        montant_travauxMaterialisation5: 0,
        montant_travauxMaterialisation6: 0,
        montant_travauxMaterialisation7: 0,
        montant_travauxMaterialisation8: 0,
        montant_travauxMaterialisation9: 0,
        montant_travauxMaterialisation10: 0,
        montant_travauxMaterialisation11: 0,
        montant_travauxMaterialisation12: 0,
        montant_travauxMaterialisation13: 0,
        montant_travauxMaterialisation14: 0,
        montant_travauxMaterialisation15: 0,
        montant_travauxMaterialisation16: 0,
        montant_travauxMaterialisation17: 0,
        montant_travauxMaterialisation18: 0,
        montant_travauxMaterialisation19: 0,
        montant_31_32_std_compl: 0,
        montant_33_materiel: 0,
        montant_34_matdiff: 0,
        montant_5_depl_debours: 0,
        montant_31_32_std_compl_zi: 0,
        montant_travauxMaterialisation_total: 0,
        // Travaux bureau
        nb_travauxBureau1: 0,
        nb_travauxBureau2: 0,
        nb_travauxBureau3: 0,
        nb_travauxBureau4: 0,
        nb_travauxBureau5: 0,
        nb_travauxBureau6: 0,
        nb_travauxBureau7: 0,
        nb_travauxBureau8: 0,
        nb_travauxBureau9: 0,
        nb_travauxBureau10: 0,
        nb_travauxBureau11: 0,
        nb_travauxBureau12: 0,
        nb_travauxBureau13: 0,
        nb_travauxBureau14: 0,
        nb_travauxBureau15: 0,
        nb_travauxBureau16: 0,
        nb_travauxBureau17: 0,
        nb_travauxBureau18: 0,
        nb_travauxBureau19: 0,
        nb_travauxBureau20: 0,
        nb_travauxBureau21: 0,
        nb_travauxBureau22: 0,
        nb_travauxBureau23: 0,
        nb_travauxBureau24: 0,
        nb_travauxBureau25: 0,
        nb_travauxBureau26: 0,
        nb_travauxBureau27: 0,
        nb_travauxBureau28: 0,
        nb_travauxBureau29: 0,
        nb_travauxBureau30: 0,
        nb_travauxBureau31: 0,
        nb_travauxBureau32: 0,
        nb_travauxBureau33: 0,
        nb_travauxBureau34: 0,
        nb_travauxBureau35: 0,
        nb_travauxBureau36: 0,
        nb_travauxBureau37: 0,
        nb_travauxBureau38: 0,
        nb_travauxBureau39: 0,
        nb_travauxBureau40: 0,
        nb_travauxBureau41: 0,
        nb_travauxBureau42: 0,
        nb_travauxBureau43: 0,
        nb_travauxBureau44: 0,
        nb_travauxBureau45: 0,
        nb_travauxBureau46: 0,
        nb_travauxBureau47: 0,
        nb_travauxBureau48: 0,
        montant_travauxBureau1: 0,
        montant_travauxBureau2: 0,
        montant_travauxBureau3: 0,
        montant_travauxBureau4: 0,
        montant_travauxBureau5: 0,
        montant_travauxBureau6: 0,
        montant_travauxBureau7: 0,
        montant_travauxBureau8: 0,
        montant_travauxBureau9: 0,
        montant_travauxBureau10: 0,
        montant_travauxBureau11: 0,
        montant_travauxBureau12: 0,
        montant_travauxBureau13: 0,
        montant_travauxBureau14: 0,
        montant_travauxBureau15: 0,
        montant_travauxBureau16: 0,
        montant_travauxBureau17: 0,
        montant_travauxBureau18: 0,
        montant_travauxBureau19: 0,
        montant_travauxBureau20: 0,
        montant_travauxBureau21: 0,
        montant_travauxBureau22: 0,
        montant_travauxBureau23: 0,
        montant_travauxBureau24: 0,
        montant_travauxBureau25: 0,
        montant_travauxBureau26: 0,
        montant_travauxBureau27: 0,
        montant_travauxBureau28: 0,
        montant_travauxBureau29: 0,
        montant_travauxBureau30: 0,
        montant_travauxBureau31: 0,
        montant_travauxBureau32: 0,
        montant_travauxBureau33: 0,
        montant_travauxBureau34: 0,
        montant_travauxBureau35: 0,
        montant_travauxBureau36: 0,
        montant_travauxBureau37: 0,
        montant_travauxBureau38: 0,
        montant_travauxBureau39: 0,
        montant_travauxBureau40: 0,
        montant_travauxBureau41: 0,
        montant_travauxBureau42: 0,
        montant_travauxBureau43: 0,
        montant_travauxBureau44: 0,
        montant_travauxBureau45: 0,
        montant_travauxBureau46: 0,
        montant_travauxBureau47: 0,
        montant_travauxBureau48: 0,
        montant_travauxBureau_total: 0,
        // Servitudes
        nb_servitudes1: 0,
        nb_servitudes2: 0,
        nb_servitudes3: 0,
        nb_servitudes4: 0,
        nb_servitudes5: 0,
        montant_rf1: 0,
        montant_rf2: 0,
        montant_rf3: 0,
        montant_rf4: 0,
        montant_rf5: 0,
        montant_rf_total: 0,
        // Divers
        divers_intitule: new Array(this.n_divers).fill(null),
        divers_nb: new Array(this.n_divers).fill(0),
        divers_prix_unitaire: new Array(this.n_divers).fill(0),
        divers_montant: new Array(this.n_divers).fill(0),
        montant_relations_autres_services: 0,
        montant_divers_total: 0,
        // Récapitulatif
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

      // **************************************************** 2 REMOVE - start **********************************************
      this.init2remove();
      // **************************************************** 2 REMOVE - end **********************************************
      
      this.updateNbBatiments();
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
     * Update montants mandat
     */
    updateMontantMandat() {
      this.form.montant_mandat1 = Number(this.form.nb_mandat1) * this.emolumentsUnits[0].montant;
      this.form.montant_mandat2 = Number(this.form.nb_mandat4) * this.emolumentsUnits[1].montant;
      this.form.montant_mandat3 = Number(this.form.nb_mandat5) * this.emolumentsUnits[2].montant;
      this.form.montant_mandat4 = Number(this.form.nb_mandat2) * this.emolumentsUnits[3].montant;
      this.form.montant_mandat5 = Number(this.form.nb_mandat3) * this.emolumentsUnits[4].montant;
      this.form.montant_mandat6 = Number(this.form.nb_mandat6) * this.emolumentsUnits[5].montant;
      this.form.montant_mandat_total = 
        Number(this.form.montant_mandat1) +
        Number(this.form.montant_mandat4) +
        Number(this.form.montant_mandat5) +
        Number(this.form.montant_mandat2) +
        Number(this.form.montant_mandat3) +
        Number(this.form.montant_mandat6);

      // Bâtiments
      for (let i=0; i<this.form.nb_batiments; i++) {
        this.form.montant_mandat2_batiment[i] = Number(this.form.nb_mandat2_batiment[i]) * this.emolumentsUnits[3].montant;
        this.form.montant_mandat3_batiment[i] = Number(this.form.nb_mandat3_batiment[i]) * this.emolumentsUnits[4].montant;
        this.form.montant_mandat6_batiment[i] = Number(this.form.nb_mandat6_batiment[i]) * this.emolumentsUnits[5].montant;

        this.form.montant_mandat_batiment_total[i] = Number(this.form.montant_mandat2_batiment[i]) + Number(this.form.montant_mandat3_batiment[i]) + Number(this.form.montant_mandat6_batiment[i]);
        this.form.montant_mandat_batiment_total_f[i] = Number(this.form.montant_mandat_batiment_total[i]) * Number(this.form.batiment_f[i]);
      }
        
      this.updateRecapitulatif();
    },

    /**
     * Update montants travaux terrain
     */
    updateMontantTravauxTerrain() {
      this.form.montant_travauxTerrain1 = Number(this.form.nb_travauxTerrain1) * this.emolumentsUnits[6].montant;
      this.form.montant_travauxTerrain2 = Number(this.form.nb_travauxTerrain2) * this.emolumentsUnits[7].montant;
      this.form.montant_travauxTerrain3 = Number(this.form.nb_travauxTerrain3) * this.emolumentsUnits[8].montant;
      this.form.montant_travauxTerrain4 = Number(this.form.nb_travauxTerrain4) * this.emolumentsUnits[9].montant;
      this.form.montant_travauxTerrain5 = Number(this.form.nb_travauxTerrain5) * this.emolumentsUnits[10].montant;
      this.form.montant_travauxTerrain6 = Number(this.form.nb_travauxTerrain6) * this.emolumentsUnits[11].montant;
      this.form.montant_travauxTerrain7 = Number(this.form.nb_travauxTerrain7) * this.emolumentsUnits[12].montant;
      this.form.montant_travauxTerrain8 = Number(this.form.nb_travauxTerrain8) * this.emolumentsUnits[13].montant;
      this.form.montant_travauxTerrain9 = Number(this.form.nb_travauxTerrain9) * this.emolumentsUnits[14].montant;
      this.form.montant_travauxTerrain10 = Number(this.form.nb_travauxTerrain10) * this.emolumentsUnits[15].montant;
      this.form.montant_travauxTerrain11 = Number(this.form.nb_travauxTerrain11) * this.emolumentsUnits[16].montant;
      this.form.montant_travauxTerrain12 = Number(this.form.nb_travauxTerrain12) * this.emolumentsUnits[17].montant;
      this.form.montant_travauxTerrain13 = Number(this.form.nb_travauxTerrain13) * this.emolumentsUnits[18].montant;
      this.form.montant_travauxTerrain14 = Number(this.form.nb_travauxTerrain14) * this.emolumentsUnits[19].montant;
      this.form.montant_travauxTerrain15 = Number(this.form.nb_travauxTerrain15) * this.emolumentsUnits[20].montant;
      this.form.montant_travauxTerrain16 = Number(this.form.nb_travauxTerrain16) * this.emolumentsUnits[21].montant;
      this.form.montant_travauxTerrain17 = Number(this.form.nb_travauxTerrain17) * this.emolumentsUnits[22].montant;
      this.form.montant_travauxTerrain18 = Number(this.form.nb_travauxTerrain18) * this.emolumentsUnits[23].montant;
      this.form.montant_travauxTerrain19 = Number(this.form.nb_travauxTerrain19) * this.emolumentsUnits[24].montant;
      this.form.montant_travauxTerrain20 = Number(this.form.nb_travauxTerrain20) * this.emolumentsUnits[25].montant;
      this.form.montant_travauxTerrain21 = Number(this.form.nb_travauxTerrain21) * this.emolumentsUnits[26].montant;
      this.form.montant_travauxTerrain22 = Number(this.form.nb_travauxTerrain22) * this.emolumentsUnits[27].montant;
      this.form.montant_travauxTerrain23 = Number(this.form.nb_travauxTerrain23) * this.emolumentsUnits[28].montant;
      this.form.montant_travauxTerrain24 = Number(this.form.nb_travauxTerrain24) * this.emolumentsUnits[29].montant;
      this.form.montant_travauxTerrain25 = Number(this.form.nb_travauxTerrain25) * this.emolumentsUnits[30].montant;
      this.form.montant_21pfp = 
        Number(this.form.montant_travauxTerrain1) +
        Number(this.form.montant_travauxTerrain2) +
        Number(this.form.montant_travauxTerrain3) +
        Number(this.form.montant_travauxTerrain4) +
        Number(this.form.montant_travauxTerrain5) +
        Number(this.form.montant_travauxTerrain6) +
        Number(this.form.montant_travauxTerrain7) +
        Number(this.form.montant_travauxTerrain8) +
        Number(this.form.montant_travauxTerrain9) +
        Number(this.form.montant_travauxTerrain10) +
        Number(this.form.montant_travauxTerrain11) +
        Number(this.form.montant_travauxTerrain12) +
        Number(this.form.montant_travauxTerrain13) +
        Number(this.form.montant_travauxTerrain14);
      
      this.form.montant_23sit = 
        Number(this.form.montant_travauxTerrain15) +
        Number(this.form.montant_travauxTerrain16);
      
      this.form.montant_22pl = 
        Number(this.form.montant_travauxTerrain17) +
        Number(this.form.montant_travauxTerrain18) +
        Number(this.form.montant_travauxTerrain19) +
        Number(this.form.montant_travauxTerrain20) +
        Number(this.form.montant_travauxTerrain21) +
        Number(this.form.montant_travauxTerrain22) +
        Number(this.form.montant_travauxTerrain23) +
        Number(this.form.montant_travauxTerrain24) +
        Number(this.form.montant_travauxTerrain25);
      
      this.form.montant_travauxTerrain_total = 
        Number(this.form.montant_21pfp) +
        Number(this.form.montant_23sit) +
        Number(this.form.montant_22pl);

      this.form.montant_travauxTerrain_total_zi =
        this.form.montant_travauxTerrain_total * Number(this.form.zi)
      
      // Bâtiments
      this.form.montant_travauxTerrain_batiment_total_f_somme = 0;
      for (let i=0; i<this.form.nb_batiments; i++) {
        this.form.montant_travauxTerrain1_batiment[i] = Number(this.form.nb_travauxTerrain1_batiment[i]) * this.emolumentsUnits[6].montant;
        this.form.montant_travauxTerrain2_batiment[i] = Number(this.form.nb_travauxTerrain2_batiment[i]) * this.emolumentsUnits[7].montant;
        this.form.montant_travauxTerrain3_batiment[i] = Number(this.form.nb_travauxTerrain3_batiment[i]) * this.emolumentsUnits[8].montant;
        this.form.montant_travauxTerrain4_batiment[i] = Number(this.form.nb_travauxTerrain4_batiment[i]) * this.emolumentsUnits[9].montant;
        this.form.montant_travauxTerrain5_batiment[i] = Number(this.form.nb_travauxTerrain5_batiment[i]) * this.emolumentsUnits[10].montant;
        this.form.montant_travauxTerrain6_batiment[i] = Number(this.form.nb_travauxTerrain6_batiment[i]) * this.emolumentsUnits[11].montant;
        this.form.montant_travauxTerrain7_batiment[i] = Number(this.form.nb_travauxTerrain7_batiment[i]) * this.emolumentsUnits[12].montant;
        this.form.montant_travauxTerrain8_batiment[i] = Number(this.form.nb_travauxTerrain8_batiment[i]) * this.emolumentsUnits[13].montant;
        this.form.montant_travauxTerrain9_batiment[i] = Number(this.form.nb_travauxTerrain9_batiment[i]) * this.emolumentsUnits[14].montant;
        this.form.montant_travauxTerrain10_batiment[i] = Number(this.form.nb_travauxTerrain10_batiment[i]) * this.emolumentsUnits[15].montant;
        this.form.montant_travauxTerrain11_batiment[i] = Number(this.form.nb_travauxTerrain11_batiment[i]) * this.emolumentsUnits[16].montant;
        this.form.montant_travauxTerrain12_batiment[i] = Number(this.form.nb_travauxTerrain12_batiment[i]) * this.emolumentsUnits[17].montant;
        this.form.montant_travauxTerrain13_batiment[i] = Number(this.form.nb_travauxTerrain13_batiment[i]) * this.emolumentsUnits[18].montant;
        this.form.montant_travauxTerrain14_batiment[i] = Number(this.form.nb_travauxTerrain14_batiment[i]) * this.emolumentsUnits[19].montant;
        this.form.montant_travauxTerrain15_batiment[i] = Number(this.form.nb_travauxTerrain15_batiment[i]) * this.emolumentsUnits[20].montant;
        this.form.montant_travauxTerrain16_batiment[i] = Number(this.form.nb_travauxTerrain16_batiment[i]) * this.emolumentsUnits[21].montant;

        this.form.montant_travauxTerrain_batiment_total[i] = 
          Number(this.form.montant_travauxTerrain1_batiment[i]) + 
          Number(this.form.montant_travauxTerrain2_batiment[i]) + 
          Number(this.form.montant_travauxTerrain3_batiment[i]) +
          Number(this.form.montant_travauxTerrain4_batiment[i]) +
          Number(this.form.montant_travauxTerrain5_batiment[i]) +
          Number(this.form.montant_travauxTerrain6_batiment[i]) +
          Number(this.form.montant_travauxTerrain7_batiment[i]) +
          Number(this.form.montant_travauxTerrain8_batiment[i]) +
          Number(this.form.montant_travauxTerrain9_batiment[i]) +
          Number(this.form.montant_travauxTerrain10_batiment[i]) +
          Number(this.form.montant_travauxTerrain11_batiment[i]) +
          Number(this.form.montant_travauxTerrain12_batiment[i]) +
          Number(this.form.montant_travauxTerrain13_batiment[i]) +
          Number(this.form.montant_travauxTerrain14_batiment[i]) +
          Number(this.form.montant_travauxTerrain15_batiment[i]) +
          Number(this.form.montant_travauxTerrain16_batiment[i]);
        
        this.form.montant_travauxTerrain_batiment_total_f[i] = 
          Number(this.form.montant_travauxTerrain_batiment_total[i]) * Number(this.form.batiment_f[i]);

        // compute total sum of montant batiments
        this.form.montant_travauxTerrain_batiment_total_f_somme += this.form.montant_travauxTerrain_batiment_total_f[i];
      }

      this.form.montant_travauxTerrain_batiment_total_f_somme_zi = this.form.montant_travauxTerrain_batiment_total_f_somme * Number(this.form.zi)

      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantTravauxMaterialisation() {
      this.form.montant_travauxMaterialisation1 = Number(this.form.nb_travauxMaterialisation1) * this.emolumentsUnits[31].montant;
      this.form.montant_travauxMaterialisation2 = Number(this.form.nb_travauxMaterialisation2) * this.emolumentsUnits[32].montant;
      this.form.montant_travauxMaterialisation3 = Number(this.form.nb_travauxMaterialisation3) * this.emolumentsUnits[33].montant;
      this.form.montant_travauxMaterialisation4 = Number(this.form.nb_travauxMaterialisation4) * this.emolumentsUnits[34].montant;
      this.form.montant_travauxMaterialisation5 = Number(this.form.nb_travauxMaterialisation5) * this.emolumentsUnits[35].montant;
      this.form.montant_travauxMaterialisation6 = Number(this.form.nb_travauxMaterialisation6) * this.emolumentsUnits[36].montant;
      this.form.montant_travauxMaterialisation7 = Number(this.form.nb_travauxMaterialisation7) * this.emolumentsUnits[37].montant;
      this.form.montant_travauxMaterialisation8 = Number(this.form.nb_travauxMaterialisation8) * this.emolumentsUnits[38].montant;
      this.form.montant_travauxMaterialisation9 = Number(this.form.nb_travauxMaterialisation9) * this.emolumentsUnits[39].montant;
      this.form.montant_travauxMaterialisation10 = Number(this.form.nb_travauxMaterialisation10) * this.emolumentsUnits[40].montant;
      this.form.montant_travauxMaterialisation11 = Number(this.form.nb_travauxMaterialisation11) * this.emolumentsUnits[41].montant;
      this.form.montant_travauxMaterialisation12 = Number(this.form.nb_travauxMaterialisation12) * this.emolumentsUnits[42].montant;
      this.form.montant_travauxMaterialisation13 = Number(this.form.nb_travauxMaterialisation13) * this.emolumentsUnits[43].montant;
      this.form.montant_travauxMaterialisation14 = Number(this.form.nb_travauxMaterialisation14) * this.emolumentsUnits[44].montant;
      this.form.montant_travauxMaterialisation15 = Number(this.form.nb_travauxMaterialisation15) * this.emolumentsUnits[45].montant;
      this.form.montant_travauxMaterialisation16 = Number(this.form.nb_travauxMaterialisation16) * this.emolumentsUnits[46].montant;
      this.form.montant_travauxMaterialisation17 = Number(this.form.nb_travauxMaterialisation17) * this.emolumentsUnits[47].montant;
      this.form.montant_travauxMaterialisation18 = Number(this.form.nb_travauxMaterialisation18) * this.emolumentsUnits[48].montant;
      this.form.montant_31_32_std_compl = 
        Number(this.form.montant_travauxMaterialisation1) +
        Number(this.form.montant_travauxMaterialisation2) +
        Number(this.form.montant_travauxMaterialisation3) +
        Number(this.form.montant_travauxMaterialisation4) +
        Number(this.form.montant_travauxMaterialisation5) +
        Number(this.form.montant_travauxMaterialisation6) +
        Number(this.form.montant_travauxMaterialisation7);
      
      this.form.montant_31_32_std_compl_zi = 
        this.form.montant_31_32_std_compl * Number(this.form.zi);

      this.form.montant_33_materiel = 
        Number(this.form.montant_travauxMaterialisation8) +
        Number(this.form.montant_travauxMaterialisation9) +
        Number(this.form.montant_travauxMaterialisation10) +
        Number(this.form.montant_travauxMaterialisation11) +
        Number(this.form.montant_travauxMaterialisation12) +
        Number(this.form.montant_travauxMaterialisation13);
      
      this.form.montant_34_matdiff = 
        Number(this.form.montant_travauxMaterialisation14) +
        Number(this.form.montant_travauxMaterialisation15) +
        Number(this.form.montant_travauxMaterialisation16) +
        Number(this.form.montant_travauxMaterialisation17);
      
      this.form.montant_5_depl_debours = 
        Number(this.form.montant_travauxMaterialisation18);
      
      this.form.montant_travauxMaterialisation_total = 
        Number(this.form.montant_31_32_std_compl_zi) +
        Number(this.form.montant_33_materiel) +
        Number(this.form.montant_34_matdiff) +
        Number(this.form.montant_5_depl_debours);
      
      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantTravauxBureau() {
      this.form.montant_travauxBureau1 = Number(this.form.nb_travauxBureau1) * this.emolumentsUnits[49].montant;
      this.form.montant_travauxBureau2 = Number(this.form.nb_travauxBureau2) * this.emolumentsUnits[50].montant;
      this.form.montant_travauxBureau3 = Number(this.form.nb_travauxBureau3) * this.emolumentsUnits[51].montant;
      this.form.montant_travauxBureau4 = Number(this.form.nb_travauxBureau4) * this.emolumentsUnits[52].montant;
      this.form.montant_travauxBureau5 = Number(this.form.nb_travauxBureau5) * this.emolumentsUnits[53].montant;
      this.form.montant_travauxBureau6 = Number(this.form.nb_travauxBureau6) * this.emolumentsUnits[54].montant;
      this.form.montant_travauxBureau7 = Number(this.form.nb_travauxBureau7) * this.emolumentsUnits[55].montant;
      this.form.montant_travauxBureau8 = Number(this.form.nb_travauxBureau8) * this.emolumentsUnits[56].montant;
      this.form.montant_travauxBureau9 = Number(this.form.nb_travauxBureau9) * this.emolumentsUnits[57].montant;
      this.form.montant_travauxBureau10 = Number(this.form.nb_travauxBureau10) * this.emolumentsUnits[58].montant;
      this.form.montant_travauxBureau11 = Number(this.form.nb_travauxBureau11) * this.emolumentsUnits[59].montant;
      this.form.montant_travauxBureau12 = Number(this.form.nb_travauxBureau12) * this.emolumentsUnits[60].montant;
      this.form.montant_travauxBureau13 = Number(this.form.nb_travauxBureau13) * this.emolumentsUnits[61].montant;
      this.form.montant_travauxBureau14 = Number(this.form.nb_travauxBureau14) * this.emolumentsUnits[62].montant;
      this.form.montant_travauxBureau15 = Number(this.form.nb_travauxBureau15) * this.emolumentsUnits[63].montant;
      this.form.montant_travauxBureau16 = Number(this.form.nb_travauxBureau16) * this.emolumentsUnits[64].montant;
      this.form.montant_travauxBureau17 = Number(this.form.nb_travauxBureau17) * this.emolumentsUnits[65].montant;
      this.form.montant_travauxBureau18 = Number(this.form.nb_travauxBureau18) * this.emolumentsUnits[66].montant;
      this.form.montant_travauxBureau19 = Number(this.form.nb_travauxBureau19) * this.emolumentsUnits[67].montant;
      this.form.montant_travauxBureau20 = Number(this.form.nb_travauxBureau20) * this.emolumentsUnits[68].montant;
      this.form.montant_travauxBureau21 = Number(this.form.nb_travauxBureau21) * this.emolumentsUnits[69].montant;
      this.form.montant_travauxBureau22 = Number(this.form.nb_travauxBureau22) * this.emolumentsUnits[70].montant;
      this.form.montant_travauxBureau23 = Number(this.form.nb_travauxBureau23) * this.emolumentsUnits[71].montant;
      this.form.montant_travauxBureau24 = Number(this.form.nb_travauxBureau24) * this.emolumentsUnits[72].montant;
      this.form.montant_travauxBureau25 = Number(this.form.nb_travauxBureau25) * this.emolumentsUnits[73].montant;
      this.form.montant_travauxBureau26 = Number(this.form.nb_travauxBureau26) * this.emolumentsUnits[74].montant;
      this.form.montant_travauxBureau27 = Number(this.form.nb_travauxBureau27) * this.emolumentsUnits[75].montant;
      this.form.montant_travauxBureau28 = Number(this.form.nb_travauxBureau28) * this.emolumentsUnits[76].montant;
      this.form.montant_travauxBureau29 = Number(this.form.nb_travauxBureau29) * this.emolumentsUnits[77].montant;
      this.form.montant_travauxBureau30 = Number(this.form.nb_travauxBureau30) * this.emolumentsUnits[78].montant;
      this.form.montant_travauxBureau31 = Number(this.form.nb_travauxBureau31) * this.emolumentsUnits[79].montant;
      this.form.montant_travauxBureau32 = Number(this.form.nb_travauxBureau32) * this.emolumentsUnits[80].montant;
      this.form.montant_travauxBureau33 = Number(this.form.nb_travauxBureau33) * this.emolumentsUnits[81].montant;
      this.form.montant_travauxBureau34 = Number(this.form.nb_travauxBureau34) * this.emolumentsUnits[82].montant;
      this.form.montant_travauxBureau35 = Number(this.form.nb_travauxBureau35) * this.emolumentsUnits[83].montant;
      this.form.montant_travauxBureau36 = Number(this.form.nb_travauxBureau36) * this.emolumentsUnits[84].montant;
      this.form.montant_travauxBureau37 = Number(this.form.nb_travauxBureau37) * this.emolumentsUnits[85].montant;
      this.form.montant_travauxBureau38 = Number(this.form.nb_travauxBureau38) * this.emolumentsUnits[86].montant;
      this.form.montant_travauxBureau39 = Number(this.form.nb_travauxBureau39) * this.emolumentsUnits[87].montant;
      this.form.montant_travauxBureau40 = Number(this.form.nb_travauxBureau40) * this.emolumentsUnits[88].montant;
      this.form.montant_travauxBureau41 = Number(this.form.nb_travauxBureau41) * this.emolumentsUnits[89].montant;
      this.form.montant_travauxBureau42 = Number(this.form.nb_travauxBureau42) * this.emolumentsUnits[90].montant;
      this.form.montant_travauxBureau43 = Number(this.form.nb_travauxBureau43) * this.emolumentsUnits[91].montant;
      this.form.montant_travauxBureau44 = Number(this.form.nb_travauxBureau44) * this.emolumentsUnits[92].montant;
      this.form.montant_travauxBureau45 = Number(this.form.nb_travauxBureau45) * this.emolumentsUnits[93].montant;
      this.form.montant_travauxBureau46 = Number(this.form.nb_travauxBureau46) * this.emolumentsUnits[94].montant;
      this.form.montant_41pfp = 
        Number(this.form.montant_travauxBureau1) +
        Number(this.form.montant_travauxBureau2) +
        Number(this.form.montant_travauxBureau3) +
        Number(this.form.montant_travauxBureau4) +
        Number(this.form.montant_travauxBureau5) +
        Number(this.form.montant_travauxBureau6) +
        Number(this.form.montant_travauxBureau7) +
        Number(this.form.montant_travauxBureau8) +
        Number(this.form.montant_travauxBureau9) +
        Number(this.form.montant_travauxBureau10) +
        Number(this.form.montant_travauxBureau11) +
        Number(this.form.montant_travauxBureau12);
      
      this.form.montant_43sit = 
        Number(this.form.montant_travauxBureau13) +
        Number(this.form.montant_travauxBureau14) +
        Number(this.form.montant_travauxBureau15) +
        Number(this.form.montant_travauxBureau16) +
        Number(this.form.montant_travauxBureau17) +
        Number(this.form.montant_travauxBureau18) +
        Number(this.form.montant_travauxBureau19) +
        Number(this.form.montant_travauxBureau20) +
        Number(this.form.montant_travauxBureau21) +
        Number(this.form.montant_travauxBureau22);
      
      this.form.montant_44surf = 
        Number(this.form.montant_travauxBureau23) +
        Number(this.form.montant_travauxBureau24) +
        Number(this.form.montant_travauxBureau25) +
        Number(this.form.montant_travauxBureau26) +
        Number(this.form.montant_travauxBureau27);
      
      this.form.montant_42pl = 
        Number(this.form.montant_travauxBureau28) +
        Number(this.form.montant_travauxBureau29) +
        Number(this.form.montant_travauxBureau30) +
        Number(this.form.montant_travauxBureau31) +
        Number(this.form.montant_travauxBureau32) +
        Number(this.form.montant_travauxBureau33) +
        Number(this.form.montant_travauxBureau34) +
        Number(this.form.montant_travauxBureau35) +
        Number(this.form.montant_travauxBureau36) +
        Number(this.form.montant_travauxBureau37) +
        Number(this.form.montant_travauxBureau38) +
        Number(this.form.montant_travauxBureau39) +
        Number(this.form.montant_travauxBureau40) +
        Number(this.form.montant_travauxBureau41) +
        Number(this.form.montant_travauxBureau42) +
        Number(this.form.montant_travauxBureau43) +
        Number(this.form.montant_travauxBureau44) +
        Number(this.form.montant_travauxBureau45) +
        Number(this.form.montant_travauxBureau46);

      this.form.montant_travauxBureau_total = 
        Number(this.form.montant_41pfp) +
        Number(this.form.montant_43sit) +
        Number(this.form.montant_44surf) +
        Number(this.form.montant_42pl);

      // Bâtiments
      this.form.montant_travauxBureau_batiment_total_f_somme = 0;
      for (let i=0; i<this.form.nb_batiments; i++) {
        this.form.montant_travauxBureau1_batiment[i] = Number(this.form.nb_travauxBureau1_batiment[i]) * this.emolumentsUnits[49].montant;
        this.form.montant_travauxBureau2_batiment[i] = Number(this.form.nb_travauxBureau2_batiment[i]) * this.emolumentsUnits[50].montant;
        this.form.montant_travauxBureau3_batiment[i] = Number(this.form.nb_travauxBureau3_batiment[i]) * this.emolumentsUnits[51].montant;
        this.form.montant_travauxBureau4_batiment[i] = Number(this.form.nb_travauxBureau4_batiment[i]) * this.emolumentsUnits[52].montant;
        this.form.montant_travauxBureau5_batiment[i] = Number(this.form.nb_travauxBureau5_batiment[i]) * this.emolumentsUnits[53].montant;
        this.form.montant_travauxBureau6_batiment[i] = Number(this.form.nb_travauxBureau6_batiment[i]) * this.emolumentsUnits[54].montant;
        this.form.montant_travauxBureau7_batiment[i] = Number(this.form.nb_travauxBureau7_batiment[i]) * this.emolumentsUnits[55].montant;
        this.form.montant_travauxBureau8_batiment[i] = Number(this.form.nb_travauxBureau8_batiment[i]) * this.emolumentsUnits[56].montant;
        this.form.montant_travauxBureau9_batiment[i] = Number(this.form.nb_travauxBureau9_batiment[i]) * this.emolumentsUnits[57].montant;
        this.form.montant_travauxBureau10_batiment[i] = Number(this.form.nb_travauxBureau10_batiment[i]) * this.emolumentsUnits[58].montant;
        this.form.montant_travauxBureau11_batiment[i] = Number(this.form.nb_travauxBureau11_batiment[i]) * this.emolumentsUnits[59].montant;
        this.form.montant_travauxBureau12_batiment[i] = Number(this.form.nb_travauxBureau12_batiment[i]) * this.emolumentsUnits[60].montant;
        this.form.montant_travauxBureau13_batiment[i] = Number(this.form.nb_travauxBureau13_batiment[i]) * this.emolumentsUnits[61].montant;
        this.form.montant_travauxBureau14_batiment[i] = Number(this.form.nb_travauxBureau14_batiment[i]) * this.emolumentsUnits[62].montant;
        this.form.montant_travauxBureau15_batiment[i] = Number(this.form.nb_travauxBureau15_batiment[i]) * this.emolumentsUnits[63].montant;
        this.form.montant_travauxBureau16_batiment[i] = Number(this.form.nb_travauxBureau16_batiment[i]) * this.emolumentsUnits[64].montant;
        this.form.montant_travauxBureau17_batiment[i] = Number(this.form.nb_travauxBureau17_batiment[i]) * this.emolumentsUnits[65].montant;
        this.form.montant_travauxBureau18_batiment[i] = Number(this.form.nb_travauxBureau18_batiment[i]) * this.emolumentsUnits[66].montant;
        this.form.montant_travauxBureau19_batiment[i] = Number(this.form.nb_travauxBureau19_batiment[i]) * this.emolumentsUnits[67].montant;
        this.form.montant_travauxBureau20_batiment[i] = Number(this.form.nb_travauxBureau20_batiment[i]) * this.emolumentsUnits[68].montant;
        this.form.montant_travauxBureau21_batiment[i] = Number(this.form.nb_travauxBureau21_batiment[i]) * this.emolumentsUnits[69].montant;
        this.form.montant_travauxBureau22_batiment[i] = Number(this.form.nb_travauxBureau22_batiment[i]) * this.emolumentsUnits[70].montant;
        this.form.montant_travauxBureau23_batiment[i] = Number(this.form.nb_travauxBureau23_batiment[i]) * this.emolumentsUnits[71].montant;
        this.form.montant_travauxBureau24_batiment[i] = Number(this.form.nb_travauxBureau24_batiment[i]) * this.emolumentsUnits[72].montant;
        this.form.montant_travauxBureau25_batiment[i] = Number(this.form.nb_travauxBureau25_batiment[i]) * this.emolumentsUnits[73].montant;
        this.form.montant_travauxBureau26_batiment[i] = Number(this.form.nb_travauxBureau26_batiment[i]) * this.emolumentsUnits[74].montant;
        this.form.montant_travauxBureau27_batiment[i] = Number(this.form.nb_travauxBureau27_batiment[i]) * this.emolumentsUnits[75].montant;

        this.form.montant_travauxBureau_batiment_total[i] = 
          Number(this.form.montant_travauxBureau1_batiment[i]) + 
          Number(this.form.montant_travauxBureau2_batiment[i]) + 
          Number(this.form.montant_travauxBureau3_batiment[i]) +
          Number(this.form.montant_travauxBureau4_batiment[i]) +
          Number(this.form.montant_travauxBureau5_batiment[i]) +
          Number(this.form.montant_travauxBureau6_batiment[i]) +
          Number(this.form.montant_travauxBureau7_batiment[i]) +
          Number(this.form.montant_travauxBureau8_batiment[i]) +
          Number(this.form.montant_travauxBureau9_batiment[i]) +
          Number(this.form.montant_travauxBureau10_batiment[i]) +
          Number(this.form.montant_travauxBureau11_batiment[i]) +
          Number(this.form.montant_travauxBureau12_batiment[i]) +
          Number(this.form.montant_travauxBureau13_batiment[i]) +
          Number(this.form.montant_travauxBureau14_batiment[i]) +
          Number(this.form.montant_travauxBureau15_batiment[i]) +
          Number(this.form.montant_travauxBureau16_batiment[i]) +
          Number(this.form.montant_travauxBureau17_batiment[i]) +
          Number(this.form.montant_travauxBureau18_batiment[i]) +
          Number(this.form.montant_travauxBureau19_batiment[i]) +
          Number(this.form.montant_travauxBureau20_batiment[i]) +
          Number(this.form.montant_travauxBureau21_batiment[i]) +
          Number(this.form.montant_travauxBureau22_batiment[i]) +
          Number(this.form.montant_travauxBureau23_batiment[i]) +
          Number(this.form.montant_travauxBureau24_batiment[i]) +
          Number(this.form.montant_travauxBureau25_batiment[i]) +
          Number(this.form.montant_travauxBureau26_batiment[i]) +
          Number(this.form.montant_travauxBureau27_batiment[i]);
        
        this.form.montant_travauxBureau_batiment_total_f[i] = 
          Number(this.form.montant_travauxBureau_batiment_total[i]) * Number(this.form.batiment_f[i]);

        // compute total sum of montant batiments
        this.form.montant_travauxBureau_batiment_total_f_somme += this.form.montant_travauxBureau_batiment_total_f[i];
      }

      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantRF() {
      this.form.montant_rf1 = Number(this.form.nb_servitudes1) * this.emolumentsUnits[95].montant;
      this.form.montant_rf2 = Number(this.form.nb_servitudes2) * this.emolumentsUnits[96].montant;
      this.form.montant_rf3 = Number(this.form.nb_servitudes3) * this.emolumentsUnits[97].montant;
      this.form.montant_rf4 = Number(this.form.nb_servitudes4) * this.emolumentsUnits[98].montant;
      this.form.montant_rf5 = Number(this.form.nb_servitudes5) * this.emolumentsUnits[99].montant;
      
      this.form.montant_rf_total = 
        Number(this.form.montant_rf1) +
        Number(this.form.montant_rf2) +
        Number(this.form.montant_rf3) +
        Number(this.form.montant_rf4) +
        Number(this.form.montant_rf5);
      
      this.updateRecapitulatif();
    },

    updateMontantDivers() {
      this.form.montant_divers_total = 0;
      for (let i=0; i<this.n_divers; i++) {
        if (this.form.divers_nb[i] && this.form.divers_prix_unitaire[i] && Number(this.form.divers_nb[i]) >= 0 && Number(this.form.divers_prix_unitaire[i]) >= 0) {
          this.form.divers_montant[i] = Number(this.form.divers_nb[i]) * Number(this.form.divers_prix_unitaire[i]);
          this.form.montant_divers_total += this.form.divers_montant[i];
        }
      }
      this.form.montant_divers_total += this.form.montant_relations_autres_services;
      
      this.updateRecapitulatif();
    },

    updateRecapitulatif() {
      this.form.montant_recapitulatif_mandat = Number(this.form.montant_mandat_total) + Number(this.form.montant_mandat_batiment_total_f.reduce((a, b) => Number(a) + Number(b)));
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
      this.updateMontantMandat();
      this.updateMontantTravauxTerrain();
      this.updateMontantTravauxMaterialisation();
      this.updateMontantTravauxBureau();
      this.updateMontantRF();
      this.updateMontantDivers();
    },

    /** Set format for comptabilité: 0.00 CHF */
    setComptabiliteFormat() {
      Object.keys(this.form).forEach(key => {
        if (key.startsWith("montant")){
          let multiple = 0.1;
          if (key === "montant_recapitulatif_tva" || key === "montant_recapitulatif_somme7" || key === "montant_recapitulatif_total") {
            multiple = 0.05
          }
          if (Array.isArray(this.form[key])) {
            for (var i = 0; i < this.form[key].length; i++) {
              this.form[key][i] = numeral( this.round( this.form[key][i], multiple ) ).format("0.00");
            }
          } else {
            this.form[key] = numeral( this.round( this.form[key], multiple ) ).format("0.00");
          }
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
    }

  },

  mounted: function(){
    this.initForm();
    this.getEmolumentsUnit();
  }
}
</script>

