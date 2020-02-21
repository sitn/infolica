<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
var numeral = require("numeral");
import {
  checkLogged,
} from "@/services/helper";

import MapHandler from '@/components/MapHandler/MapHandler.vue';

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
    MapHandler
  },
  data: () => ({
    affaire: {},
    affaire_numeros: [],
    affaire_remarques: [],
    affaire_factures: [],
  }),

  methods: {

    /*
     * SEARCH AFFAIRE
     */
    async searchAffaire() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            // this.affaire = response.data
            var obj = response.data;
            Object.keys(obj).forEach(function(key) {
              if (obj[key] === null) obj[key] = "-";
            })
            this.affaire = obj;
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.affaire_numeros = response.data
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * SEARCH AFFAIRE FACTURES
     */
    async searchAffaireFactures() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response && response.data) {
            this.affaire_factures = response.data.map(x => ({
              date: x.date,
              client_id: x.client_id,
              montant_mo: numeral(x.montant_mo).format('0.00'),
              montant_mat_diff: numeral(x.montant_mat_diff).format('0.00'),
              montant_rf: numeral(x.montant_rf).format('0.00'),
              montant_tva: numeral(x.montant_tva).format('0.00'),
              montant_total: numeral(x.montant_total).format('0.00'),
            }))
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireRemarques() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.affaire_factures = response.data
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenNumero(id) {
      window.setTimeout;
      let routeData = this.$router.resolve("/numeros/" + id);
      window.open(routeData.href, "_blank");
    },

    

  },

  mounted: function() {
    checkLogged();
    this.searchAffaire();
    this.searchAffaireNumeros();
    this.searchAffaireRemarques();
    this.searchAffaireFactures();
  }
};
</script>



