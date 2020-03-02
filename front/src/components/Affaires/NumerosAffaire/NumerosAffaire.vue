<style src="./numerosAffaire.css" scoped></style>
<template src="./numerosAffaire.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: "NumerosAffaire",
  props: {},
  components: {},
  data: () => ({
    affaire_numeros: [],

  }),

  methods: {
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
    this.searchAffaireNumeros();
  }
};
</script>



