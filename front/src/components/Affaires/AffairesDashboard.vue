<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
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
    affaire_numeros: {},
    affaire_remarques: {},
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
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireRemarques() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_REMARQUES_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.affaire_remarques = response.data
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
  }
};
</script>



