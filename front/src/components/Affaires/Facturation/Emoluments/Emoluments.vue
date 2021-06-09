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
        nb_batiments: 0,
        indice_application: 1.22,
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
        montant_travauxTerrain_total: numeral(0).format("0.00"),
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
        montant_travauxMaterialisation1: numeral(0).format("0.00"),
        montant_travauxMaterialisation2: numeral(0).format("0.00"),
        montant_travauxMaterialisation3: numeral(0).format("0.00"),
        montant_travauxMaterialisation4: numeral(0).format("0.00"),
        montant_travauxMaterialisation5: numeral(0).format("0.00"),
        montant_travauxMaterialisation6: numeral(0).format("0.00"),
        montant_travauxMaterialisation7: numeral(0).format("0.00"),
        montant_travauxMaterialisation8: numeral(0).format("0.00"),
        montant_travauxMaterialisation9: numeral(0).format("0.00"),
        montant_travauxMaterialisation10: numeral(0).format("0.00"),
        montant_travauxMaterialisation11: numeral(0).format("0.00"),
        montant_travauxMaterialisation12: numeral(0).format("0.00"),
        montant_travauxMaterialisation13: numeral(0).format("0.00"),
        montant_travauxMaterialisation14: numeral(0).format("0.00"),
        montant_travauxMaterialisation15: numeral(0).format("0.00"),
        montant_travauxMaterialisation16: numeral(0).format("0.00"),
        montant_travauxMaterialisation17: numeral(0).format("0.00"),
        montant_travauxMaterialisation18: numeral(0).format("0.00"),
        montant_travauxMaterialisation19: numeral(0).format("0.00"),
        montant_travauxMaterialisation_total: numeral(0).format("0.00"),
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
        montant_travauxBureau1: numeral(0).format("0.00"),
        montant_travauxBureau2: numeral(0).format("0.00"),
        montant_travauxBureau3: numeral(0).format("0.00"),
        montant_travauxBureau4: numeral(0).format("0.00"),
        montant_travauxBureau5: numeral(0).format("0.00"),
        montant_travauxBureau6: numeral(0).format("0.00"),
        montant_travauxBureau7: numeral(0).format("0.00"),
        montant_travauxBureau8: numeral(0).format("0.00"),
        montant_travauxBureau9: numeral(0).format("0.00"),
        montant_travauxBureau10: numeral(0).format("0.00"),
        montant_travauxBureau11: numeral(0).format("0.00"),
        montant_travauxBureau12: numeral(0).format("0.00"),
        montant_travauxBureau13: numeral(0).format("0.00"),
        montant_travauxBureau14: numeral(0).format("0.00"),
        montant_travauxBureau15: numeral(0).format("0.00"),
        montant_travauxBureau16: numeral(0).format("0.00"),
        montant_travauxBureau17: numeral(0).format("0.00"),
        montant_travauxBureau18: numeral(0).format("0.00"),
        montant_travauxBureau19: numeral(0).format("0.00"),
        montant_travauxBureau20: numeral(0).format("0.00"),
        montant_travauxBureau21: numeral(0).format("0.00"),
        montant_travauxBureau22: numeral(0).format("0.00"),
        montant_travauxBureau23: numeral(0).format("0.00"),
        montant_travauxBureau24: numeral(0).format("0.00"),
        montant_travauxBureau25: numeral(0).format("0.00"),
        montant_travauxBureau26: numeral(0).format("0.00"),
        montant_travauxBureau27: numeral(0).format("0.00"),
        montant_travauxBureau28: numeral(0).format("0.00"),
        montant_travauxBureau29: numeral(0).format("0.00"),
        montant_travauxBureau30: numeral(0).format("0.00"),
        montant_travauxBureau31: numeral(0).format("0.00"),
        montant_travauxBureau32: numeral(0).format("0.00"),
        montant_travauxBureau33: numeral(0).format("0.00"),
        montant_travauxBureau34: numeral(0).format("0.00"),
        montant_travauxBureau35: numeral(0).format("0.00"),
        montant_travauxBureau36: numeral(0).format("0.00"),
        montant_travauxBureau37: numeral(0).format("0.00"),
        montant_travauxBureau38: numeral(0).format("0.00"),
        montant_travauxBureau39: numeral(0).format("0.00"),
        montant_travauxBureau40: numeral(0).format("0.00"),
        montant_travauxBureau41: numeral(0).format("0.00"),
        montant_travauxBureau42: numeral(0).format("0.00"),
        montant_travauxBureau43: numeral(0).format("0.00"),
        montant_travauxBureau44: numeral(0).format("0.00"),
        montant_travauxBureau45: numeral(0).format("0.00"),
        montant_travauxBureau46: numeral(0).format("0.00"),
        montant_travauxBureau47: numeral(0).format("0.00"),
        montant_travauxBureau48: numeral(0).format("0.00"),
        montant_travauxBureau_total: numeral(0).format("0.00"),
        // Servitudes
        nb_servitudes1: 0,
        nb_servitudes2: 0,
        nb_servitudes3: 0,
        montant_servitudes1: numeral(0).format("0.00"),
        montant_servitudes2: numeral(0).format("0.00"),
        montant_servitudes3: numeral(0).format("0.00"),
        montant_servitudes_total: numeral(0).format("0.00"),
        // Récapitulatif
        montant_recapitulatif_somme1: numeral(0).format("0.00"),
        montant_recapitulatif_somme2: numeral(0).format("0.00"),
        montant_recapitulatif_somme3: numeral(0).format("0.00"),
        montant_recapitulatif_somme4: numeral(0).format("0.00"),
        montant_recapitulatif_somme5: numeral(0).format("0.00"),
        montant_recapitulatif_somme6: numeral(0).format("0.00"),
        montant_recapitulatif_indice_application: numeral(0).format("0.00"),
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
      this.updateRecapitulatif();
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
      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantTravauxMaterialisation() {
      this.form.montant_travauxMaterialisation1 = numeral(Number(this.form.nb_travauxMaterialisation1) * Number(this.emolumentsUnits[31].montant)).format("0.00");
      this.form.montant_travauxMaterialisation2 = numeral(Number(this.form.nb_travauxMaterialisation2) * Number(this.emolumentsUnits[32].montant)).format("0.00");
      this.form.montant_travauxMaterialisation3 = numeral(Number(this.form.nb_travauxMaterialisation3) * Number(this.emolumentsUnits[33].montant)).format("0.00");
      this.form.montant_travauxMaterialisation4 = numeral(Number(this.form.nb_travauxMaterialisation4) * Number(this.emolumentsUnits[34].montant)).format("0.00");
      this.form.montant_travauxMaterialisation5 = numeral(Number(this.form.nb_travauxMaterialisation5) * Number(this.emolumentsUnits[35].montant)).format("0.00");
      this.form.montant_travauxMaterialisation6 = numeral(Number(this.form.nb_travauxMaterialisation6) * Number(this.emolumentsUnits[36].montant)).format("0.00");
      this.form.montant_travauxMaterialisation7 = numeral(Number(this.form.nb_travauxMaterialisation7) * Number(this.emolumentsUnits[37].montant)).format("0.00");
      this.form.montant_travauxMaterialisation8 = numeral(Number(this.form.nb_travauxMaterialisation8) * Number(this.emolumentsUnits[38].montant)).format("0.00");
      this.form.montant_travauxMaterialisation9 = numeral(Number(this.form.nb_travauxMaterialisation9) * Number(this.emolumentsUnits[39].montant)).format("0.00");
      this.form.montant_travauxMaterialisation10 = numeral(Number(this.form.nb_travauxMaterialisation10) * Number(this.emolumentsUnits[40].montant)).format("0.00");
      this.form.montant_travauxMaterialisation11 = numeral(Number(this.form.nb_travauxMaterialisation11) * Number(this.emolumentsUnits[41].montant)).format("0.00");
      this.form.montant_travauxMaterialisation12 = numeral(Number(this.form.nb_travauxMaterialisation12) * Number(this.emolumentsUnits[42].montant)).format("0.00");
      this.form.montant_travauxMaterialisation13 = numeral(Number(this.form.nb_travauxMaterialisation13) * Number(this.emolumentsUnits[43].montant)).format("0.00");
      this.form.montant_travauxMaterialisation14 = numeral(Number(this.form.nb_travauxMaterialisation14) * Number(this.emolumentsUnits[44].montant)).format("0.00");
      this.form.montant_travauxMaterialisation15 = numeral(Number(this.form.nb_travauxMaterialisation15) * Number(this.emolumentsUnits[45].montant)).format("0.00");
      this.form.montant_travauxMaterialisation16 = numeral(Number(this.form.nb_travauxMaterialisation16) * Number(this.emolumentsUnits[46].montant)).format("0.00");
      this.form.montant_travauxMaterialisation17 = numeral(Number(this.form.nb_travauxMaterialisation17) * Number(this.emolumentsUnits[47].montant)).format("0.00");
      this.form.montant_travauxMaterialisation18 = numeral(Number(this.form.nb_travauxMaterialisation18) * Number(this.emolumentsUnits[48].montant)).format("0.00");
      this.form.montant_travauxMaterialisation_total = numeral(
        Number(this.form.montant_travauxMaterialisation1) +
        Number(this.form.montant_travauxMaterialisation2) +
        Number(this.form.montant_travauxMaterialisation3) +
        Number(this.form.montant_travauxMaterialisation4) +
        Number(this.form.montant_travauxMaterialisation5) +
        Number(this.form.montant_travauxMaterialisation6) +
        Number(this.form.montant_travauxMaterialisation7) +
        Number(this.form.montant_travauxMaterialisation8) +
        Number(this.form.montant_travauxMaterialisation9) +
        Number(this.form.montant_travauxMaterialisation10) +
        Number(this.form.montant_travauxMaterialisation11) +
        Number(this.form.montant_travauxMaterialisation12) +
        Number(this.form.montant_travauxMaterialisation13) +
        Number(this.form.montant_travauxMaterialisation14) +
        Number(this.form.montant_travauxMaterialisation15) +
        Number(this.form.montant_travauxMaterialisation16) +
        Number(this.form.montant_travauxMaterialisation17) +
        Number(this.form.montant_travauxMaterialisation18)
      ).format("0.00");
      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantTravauxBureau() {
      this.form.montant_travauxBureau1 = numeral(Number(this.form.nb_travauxBureau1 * Number(this.emolumentsUnits[49].montant))).format("0.00");
      this.form.montant_travauxBureau2 = numeral(Number(this.form.nb_travauxBureau2 * Number(this.emolumentsUnits[50].montant))).format("0.00");
      this.form.montant_travauxBureau3 = numeral(Number(this.form.nb_travauxBureau3 * Number(this.emolumentsUnits[51].montant))).format("0.00");
      this.form.montant_travauxBureau4 = numeral(Number(this.form.nb_travauxBureau4 * Number(this.emolumentsUnits[52].montant))).format("0.00");
      this.form.montant_travauxBureau5 = numeral(Number(this.form.nb_travauxBureau5 * Number(this.emolumentsUnits[53].montant))).format("0.00");
      this.form.montant_travauxBureau6 = numeral(Number(this.form.nb_travauxBureau6 * Number(this.emolumentsUnits[54].montant))).format("0.00");
      this.form.montant_travauxBureau7 = numeral(Number(this.form.nb_travauxBureau7 * Number(this.emolumentsUnits[55].montant))).format("0.00");
      this.form.montant_travauxBureau8 = numeral(Number(this.form.nb_travauxBureau8 * Number(this.emolumentsUnits[56].montant))).format("0.00");
      this.form.montant_travauxBureau9 = numeral(Number(this.form.nb_travauxBureau9 * Number(this.emolumentsUnits[57].montant))).format("0.00");
      this.form.montant_travauxBureau10 = numeral(Number(this.form.nb_travauxBureau10 * Number(this.emolumentsUnits[58].montant))).format("0.00");
      this.form.montant_travauxBureau11 = numeral(Number(this.form.nb_travauxBureau11 * Number(this.emolumentsUnits[59].montant))).format("0.00");
      this.form.montant_travauxBureau12 = numeral(Number(this.form.nb_travauxBureau12 * Number(this.emolumentsUnits[60].montant))).format("0.00");
      this.form.montant_travauxBureau13 = numeral(Number(this.form.nb_travauxBureau13 * Number(this.emolumentsUnits[61].montant))).format("0.00");
      this.form.montant_travauxBureau14 = numeral(Number(this.form.nb_travauxBureau14 * Number(this.emolumentsUnits[62].montant))).format("0.00");
      this.form.montant_travauxBureau15 = numeral(Number(this.form.nb_travauxBureau15 * Number(this.emolumentsUnits[63].montant))).format("0.00");
      this.form.montant_travauxBureau16 = numeral(Number(this.form.nb_travauxBureau16 * Number(this.emolumentsUnits[64].montant))).format("0.00");
      this.form.montant_travauxBureau17 = numeral(Number(this.form.nb_travauxBureau17 * Number(this.emolumentsUnits[65].montant))).format("0.00");
      this.form.montant_travauxBureau18 = numeral(Number(this.form.nb_travauxBureau18 * Number(this.emolumentsUnits[66].montant))).format("0.00");
      this.form.montant_travauxBureau19 = numeral(Number(this.form.nb_travauxBureau19 * Number(this.emolumentsUnits[67].montant))).format("0.00");
      this.form.montant_travauxBureau20 = numeral(Number(this.form.nb_travauxBureau20 * Number(this.emolumentsUnits[68].montant))).format("0.00");
      this.form.montant_travauxBureau21 = numeral(Number(this.form.nb_travauxBureau21 * Number(this.emolumentsUnits[69].montant))).format("0.00");
      this.form.montant_travauxBureau22 = numeral(Number(this.form.nb_travauxBureau22 * Number(this.emolumentsUnits[70].montant))).format("0.00");
      this.form.montant_travauxBureau23 = numeral(Number(this.form.nb_travauxBureau23 * Number(this.emolumentsUnits[71].montant))).format("0.00");
      this.form.montant_travauxBureau24 = numeral(Number(this.form.nb_travauxBureau24 * Number(this.emolumentsUnits[72].montant))).format("0.00");
      this.form.montant_travauxBureau25 = numeral(Number(this.form.nb_travauxBureau25 * Number(this.emolumentsUnits[73].montant))).format("0.00");
      this.form.montant_travauxBureau26 = numeral(Number(this.form.nb_travauxBureau26 * Number(this.emolumentsUnits[74].montant))).format("0.00");
      this.form.montant_travauxBureau27 = numeral(Number(this.form.nb_travauxBureau27 * Number(this.emolumentsUnits[75].montant))).format("0.00");
      this.form.montant_travauxBureau28 = numeral(Number(this.form.nb_travauxBureau28 * Number(this.emolumentsUnits[76].montant))).format("0.00");
      this.form.montant_travauxBureau29 = numeral(Number(this.form.nb_travauxBureau29 * Number(this.emolumentsUnits[77].montant))).format("0.00");
      this.form.montant_travauxBureau30 = numeral(Number(this.form.nb_travauxBureau30 * Number(this.emolumentsUnits[78].montant))).format("0.00");
      this.form.montant_travauxBureau31 = numeral(Number(this.form.nb_travauxBureau31 * Number(this.emolumentsUnits[79].montant))).format("0.00");
      this.form.montant_travauxBureau32 = numeral(Number(this.form.nb_travauxBureau32 * Number(this.emolumentsUnits[80].montant))).format("0.00");
      this.form.montant_travauxBureau33 = numeral(Number(this.form.nb_travauxBureau33 * Number(this.emolumentsUnits[81].montant))).format("0.00");
      this.form.montant_travauxBureau34 = numeral(Number(this.form.nb_travauxBureau34 * Number(this.emolumentsUnits[82].montant))).format("0.00");
      this.form.montant_travauxBureau35 = numeral(Number(this.form.nb_travauxBureau35 * Number(this.emolumentsUnits[83].montant))).format("0.00");
      this.form.montant_travauxBureau36 = numeral(Number(this.form.nb_travauxBureau36 * Number(this.emolumentsUnits[84].montant))).format("0.00");
      this.form.montant_travauxBureau37 = numeral(Number(this.form.nb_travauxBureau37 * Number(this.emolumentsUnits[85].montant))).format("0.00");
      this.form.montant_travauxBureau38 = numeral(Number(this.form.nb_travauxBureau38 * Number(this.emolumentsUnits[86].montant))).format("0.00");
      this.form.montant_travauxBureau39 = numeral(Number(this.form.nb_travauxBureau39 * Number(this.emolumentsUnits[87].montant))).format("0.00");
      this.form.montant_travauxBureau40 = numeral(Number(this.form.nb_travauxBureau40 * Number(this.emolumentsUnits[88].montant))).format("0.00");
      this.form.montant_travauxBureau41 = numeral(Number(this.form.nb_travauxBureau41 * Number(this.emolumentsUnits[89].montant))).format("0.00");
      this.form.montant_travauxBureau42 = numeral(Number(this.form.nb_travauxBureau42 * Number(this.emolumentsUnits[90].montant))).format("0.00");
      this.form.montant_travauxBureau43 = numeral(Number(this.form.nb_travauxBureau43 * Number(this.emolumentsUnits[91].montant))).format("0.00");
      this.form.montant_travauxBureau44 = numeral(Number(this.form.nb_travauxBureau44 * Number(this.emolumentsUnits[92].montant))).format("0.00");
      this.form.montant_travauxBureau45 = numeral(Number(this.form.nb_travauxBureau45 * Number(this.emolumentsUnits[93].montant))).format("0.00");
      this.form.montant_travauxBureau46 = numeral(Number(this.form.nb_travauxBureau46 * Number(this.emolumentsUnits[94].montant))).format("0.00");
      this.form.montant_travauxBureau_total = numeral(
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
        Number(this.form.montant_travauxBureau12) +
        Number(this.form.montant_travauxBureau13) +
        Number(this.form.montant_travauxBureau14) +
        Number(this.form.montant_travauxBureau15) +
        Number(this.form.montant_travauxBureau16) +
        Number(this.form.montant_travauxBureau17) +
        Number(this.form.montant_travauxBureau18) +
        Number(this.form.montant_travauxBureau19) +
        Number(this.form.montant_travauxBureau20) +
        Number(this.form.montant_travauxBureau21) +
        Number(this.form.montant_travauxBureau22) +
        Number(this.form.montant_travauxBureau23) +
        Number(this.form.montant_travauxBureau24) +
        Number(this.form.montant_travauxBureau25) +
        Number(this.form.montant_travauxBureau26) +
        Number(this.form.montant_travauxBureau27) +
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
        Number(this.form.montant_travauxBureau46)
      ).format("0.00");
      this.updateRecapitulatif();
    },


    /**
     * Update montants travaux matérialisation
     */
    updateMontantServitudes() {
      this.form.montant_servitudes1 = numeral(Number(this.form.nb_servitudes1 * Number(this.emolumentsUnits[95].montant))).format("0.00");
      this.form.montant_servitudes2 = numeral(Number(this.form.nb_servitudes2 * Number(this.emolumentsUnits[96].montant))).format("0.00");
      this.form.montant_servitudes3 = numeral(Number(this.form.nb_servitudes3 * Number(this.emolumentsUnits[97].montant))).format("0.00");
      this.form.montant_servitudes_total = numeral(
        Number(this.form.montant_servitudes1) +
        Number(this.form.montant_servitudes2) +
        Number(this.form.montant_servitudes3)
      ).format("0.00");
      this.updateRecapitulatif();
    },

    updateRecapitulatif() {
      this.form.montant_recapitulatif_somme1 = numeral(Number(this.form.montant_mandat_total)).format("0.00");
      this.form.montant_recapitulatif_somme2 = numeral(
        Number(this.form.montant_recapitulatif_somme1) +
        Number(this.form.montant_travauxTerrain_total)
      ).format("0.00");
      this.form.montant_recapitulatif_somme3 = numeral(
        Number(this.form.montant_recapitulatif_somme2) +
        Number(this.form.montant_travauxBureau_total)
      ).format("0.00");
      this.form.montant_recapitulatif_indice_application = numeral(
        Math.round( 10 * (
          Number(this.form.montant_recapitulatif_somme3) *
          (Number(this.form.indice_application)-1)
        )) / 10
      ).format("0.00");
      this.form.montant_recapitulatif_somme4 = numeral(
        Number(this.form.montant_recapitulatif_somme2) +
        Number(this.form.montant_recapitulatif_indice_application)
      ).format("0.00");

      this.form.montant_recapitulatif_somme5 = numeral(0).format("0.00");
      this.form.montant_recapitulatif_somme6 = numeral(0).format("0.00");
    }

  },

  mounted: function(){
    this.initForm();
    this.computeZi();
    this.getEmolumentsUnit();
  }
}
</script>

