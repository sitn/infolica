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
  }),

  methods: {

    /*
     * SEARCH AFFAIRE
     */
    async searchAffaire() {
      return new Promise((resolve, reject) => {
          this.$http
            .get(
              process.env.VUE_APP_API_URL +
                process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
                this.$route.params.id
            ).then(response => {
              if (response.data) {
                var obj = response.data;
                Object.keys(obj).forEach(function(key) {
                  if (obj[key] === null) obj[key] = "-";
                })
                this.affaire = obj;
                resolve({x: response.data.localisation_e, y: response.data.localisation_n});
              }
            })
            .catch(() => reject)
          });
    }
  },

  mounted: function() {
    checkLogged();
    let _this = this;
    this.searchAffaire().then(function(center){
      _this.$refs.mapHandler.initMap(center, process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM);
      
      setTimeout(function(){
        _this.$refs.mapHandler.addMarker(center.x, center.y);
      }, 1000);
    });
  }
};
</script>



