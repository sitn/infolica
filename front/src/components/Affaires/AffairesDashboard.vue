<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
import {checkLogged} from '@/services/helper'
import MapHandler from '@/components/MapHandler/MapHandler.vue';
import NumerosAffaire from '@/components/Affaires/NumerosAffaire/NumerosAffaire.vue';
import Suivi from '@/components/Affaires/Suivi/Suivi.vue';
import Facturation from '@/components/Facturation/Facturation.vue';
import Remarques from '@/components/Affaires/Remarques/Remarques.vue';

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
    MapHandler,
    NumerosAffaire,
    Suivi,
    Facturation,
    Remarques,
  },
  data: () => ({
    affaire: {},
    affaire_numeros: [],
    // affaire_remarques: [],

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

  },

  mounted: function() {
    checkLogged();
    this.searchAffaire();
  }
};
</script>



