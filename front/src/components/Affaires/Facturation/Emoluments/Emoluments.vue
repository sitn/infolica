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
      }
  },

  methods:{
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
        }
      }).catch(err => handleException(err, this));
    },


    initForm() {
      this.form = {
        plans_folio: null,
        parcelles: null,
        echelle: null,
        no_facture: null,
        technicien: this.affaire.technicien_id,
        nb_pfp3_hors_mutation: null,
        pente: 0,
        visibilite: 0,
        trafic: 0,
        zi: numeral(1).format("0.00"),
        //mandats
        nb_mandat1: 0,
        montant_mandat1: numeral(0).format("0.00"),
        nb_mandat4: 0,
        montant_mandat4: numeral(0).format("0.00"),
        nb_mandat5: 0,
        montant_mandat5: numeral(0).format("0.00"),
        nb_mandat2: 0,
        montant_mandat2: numeral(0).format("0.00"),
        nb_mandat3: 0,
        montant_mandat3: numeral(0).format("0.00"),
        nb_mandat6: 0,
        montant_mandat6: numeral(0).format("0.00"),
        montant_mandat_total: numeral(0).format("0.00"),
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
        montant_travauxTerrain1: numeral(0).format("0.00"),
        montant_travauxTerrain2: numeral(0).format("0.00"),
        montant_travauxTerrain3: numeral(0).format("0.00"),
        montant_travauxTerrain4: numeral(0).format("0.00"),
        montant_travauxTerrain5: numeral(0).format("0.00"),
        montant_travauxTerrain6: numeral(0).format("0.00"),
        montant_travauxTerrain7: numeral(0).format("0.00"),
        montant_travauxTerrain8: numeral(0).format("0.00"),
        montant_travauxTerrain9: numeral(0).format("0.00"),
        montant_travauxTerrain10: numeral(0).format("0.00"),
        montant_travauxTerrain11: numeral(0).format("0.00"),
        montant_travauxTerrain12: numeral(0).format("0.00"),
        montant_travauxTerrain13: numeral(0).format("0.00"),
        montant_travauxTerrain14: numeral(0).format("0.00"),
        montant_travauxTerrain15: numeral(0).format("0.00"),
        montant_travauxTerrain16: numeral(0).format("0.00"),
        montant_travauxTerrain17: numeral(0).format("0.00"),
        montant_travauxTerrain18: numeral(0).format("0.00"),
        montant_travauxTerrain19: numeral(0).format("0.00"),
        montant_travauxTerrain20: numeral(0).format("0.00"),
        montant_travauxTerrain21: numeral(0).format("0.00"),
        montant_travauxTerrain22: numeral(0).format("0.00"),
        montant_travauxTerrain23: numeral(0).format("0.00"),
        montant_travauxTerrain24: numeral(0).format("0.00"),
        montant_travauxTerrain25: numeral(0).format("0.00"),

      }
    },

    /**
     * Update value of zi
     */
    computeZi() {
      this.form.zi = numeral(
        1 + 
        Number(this.form.pente)/100 +
        Number(this.form.visibilite) + 
        Number(this.form.trafic)
      ).format("0.00");
    },

    /**
     * Update montants mandat
     */
    updateMontantMandat() {
      this.form.montant_mandat1 = numeral(Number(this.form.nb_mandat1) * Number(this.emolumentsUnits[0].montant)).format("0.00");
      this.form.montant_mandat2 = numeral(Number(this.form.nb_mandat4) * Number(this.emolumentsUnits[1].montant)).format("0.00");
      this.form.montant_mandat3 = numeral(Number(this.form.nb_mandat5) * Number(this.emolumentsUnits[2].montant)).format("0.00");
      this.form.montant_mandat4 = numeral(Number(this.form.nb_mandat2) * Number(this.emolumentsUnits[3].montant)).format("0.00");
      this.form.montant_mandat5 = numeral(Number(this.form.nb_mandat3) * Number(this.emolumentsUnits[4].montant)).format("0.00");
      this.form.montant_mandat6 = numeral(Number(this.form.nb_mandat6) * Number(this.emolumentsUnits[5].montant)).format("0.00");
      this.form.montant_mandat_total = numeral(
        Number(this.form.montant_mandat1) +
        Number(this.form.montant_mandat4) +
        Number(this.form.montant_mandat5) +
        Number(this.form.montant_mandat2) +
        Number(this.form.montant_mandat3) +
        Number(this.form.montant_mandat6)
      ).format("0.00");
    },

    /**
     * Update montants travaux terrain
     */
    updateMontantTravauxTerrain() {
      this.form.montant_travauxTerrain1 = numeral(Number(this.form.nb_travauxTerrain1) * Number(this.emolumentsUnits[6].montant)).format("0.00");
      this.form.montant_travauxTerrain2 = numeral(Number(this.form.nb_travauxTerrain2) * Number(this.emolumentsUnits[7].montant)).format("0.00");
      this.form.montant_travauxTerrain3 = numeral(Number(this.form.nb_travauxTerrain3) * Number(this.emolumentsUnits[8].montant)).format("0.00");
      this.form.montant_travauxTerrain4 = numeral(Number(this.form.nb_travauxTerrain4) * Number(this.emolumentsUnits[9].montant)).format("0.00");
      this.form.montant_travauxTerrain5 = numeral(Number(this.form.nb_travauxTerrain5) * Number(this.emolumentsUnits[10].montant)).format("0.00");
      this.form.montant_travauxTerrain6 = numeral(Number(this.form.nb_travauxTerrain6) * Number(this.emolumentsUnits[11].montant)).format("0.00");
      this.form.montant_travauxTerrain7 = numeral(Number(this.form.nb_travauxTerrain7) * Number(this.emolumentsUnits[12].montant)).format("0.00");
      this.form.montant_travauxTerrain8 = numeral(Number(this.form.nb_travauxTerrain8) * Number(this.emolumentsUnits[13].montant)).format("0.00");
      this.form.montant_travauxTerrain9 = numeral(Number(this.form.nb_travauxTerrain9) * Number(this.emolumentsUnits[14].montant)).format("0.00");
      this.form.montant_travauxTerrain10 = numeral(Number(this.form.nb_travauxTerrain10) * Number(this.emolumentsUnits[15].montant)).format("0.00");
      this.form.montant_travauxTerrain11 = numeral(Number(this.form.nb_travauxTerrain11) * Number(this.emolumentsUnits[16].montant)).format("0.00");
      this.form.montant_travauxTerrain12 = numeral(Number(this.form.nb_travauxTerrain12) * Number(this.emolumentsUnits[17].montant)).format("0.00");
      this.form.montant_travauxTerrain13 = numeral(Number(this.form.nb_travauxTerrain13) * Number(this.emolumentsUnits[18].montant)).format("0.00");
      this.form.montant_travauxTerrain14 = numeral(Number(this.form.nb_travauxTerrain14) * Number(this.emolumentsUnits[19].montant)).format("0.00");
      this.form.montant_travauxTerrain15 = numeral(Number(this.form.nb_travauxTerrain15) * Number(this.emolumentsUnits[20].montant)).format("0.00");
      this.form.montant_travauxTerrain16 = numeral(Number(this.form.nb_travauxTerrain16) * Number(this.emolumentsUnits[21].montant)).format("0.00");
      this.form.montant_travauxTerrain17 = numeral(Number(this.form.nb_travauxTerrain17) * Number(this.emolumentsUnits[22].montant)).format("0.00");
      this.form.montant_travauxTerrain18 = numeral(Number(this.form.nb_travauxTerrain18) * Number(this.emolumentsUnits[23].montant)).format("0.00");
      this.form.montant_travauxTerrain19 = numeral(Number(this.form.nb_travauxTerrain19) * Number(this.emolumentsUnits[24].montant)).format("0.00");
      this.form.montant_travauxTerrain20 = numeral(Number(this.form.nb_travauxTerrain20) * Number(this.emolumentsUnits[25].montant)).format("0.00");
      this.form.montant_travauxTerrain21 = numeral(Number(this.form.nb_travauxTerrain21) * Number(this.emolumentsUnits[26].montant)).format("0.00");
      this.form.montant_travauxTerrain22 = numeral(Number(this.form.nb_travauxTerrain22) * Number(this.emolumentsUnits[27].montant)).format("0.00");
      this.form.montant_travauxTerrain23 = numeral(Number(this.form.nb_travauxTerrain23) * Number(this.emolumentsUnits[28].montant)).format("0.00");
      this.form.montant_travauxTerrain24 = numeral(Number(this.form.nb_travauxTerrain24) * Number(this.emolumentsUnits[29].montant)).format("0.00");
      this.form.montant_travauxTerrain25 = numeral(Number(this.form.nb_travauxTerrain25) * Number(this.emolumentsUnits[30].montant)).format("0.00");
      this.form.montant_travauxTerrain_total = numeral(
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
        Number(this.form.montant_travauxTerrain14) +
        Number(this.form.montant_travauxTerrain15) +
        Number(this.form.montant_travauxTerrain16) +
        Number(this.form.montant_travauxTerrain17) +
        Number(this.form.montant_travauxTerrain18) +
        Number(this.form.montant_travauxTerrain19) +
        Number(this.form.montant_travauxTerrain20) +
        Number(this.form.montant_travauxTerrain21) +
        Number(this.form.montant_travauxTerrain22) +
        Number(this.form.montant_travauxTerrain23) +
        Number(this.form.montant_travauxTerrain24) +
        Number(this.form.montant_travauxTerrain25)
      ).format("0.00");
    }


  },

  mounted: function(){
    this.initForm();
    this.computeZi();
    this.getEmolumentsUnit();
  }
}
</script>

