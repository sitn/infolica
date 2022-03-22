<style src="./preavisEdit.css" scoped></style>
<template src="./preavisEdit.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import Documents from "@/components/Affaires/Documents/Documents.vue";

import { handleException } from "@/services/exceptionsHandler";

// import moment from "moment";

export default {
  name: "PreavisAffaire",
  props: {},
  components: {
    MapHandler,
    Documents,
  },
  data() {
    return {
      affaire: {},
      affaireLoaded: false,
      mapLoaded: false,
    };
  },

  methods: {
    /*
     * SEARCH AFFAIRE PREAVIS
     */
    async searchAffaire() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_AFFAIRE_BY_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      )
      .then(response => {
        if (response && response.data) {
          this.affaire = response.data;
          // let obj = response.data;

          // obj["client_commande_nom_"] = [
          //   obj.client_commande_entreprise,
          //   obj.client_commande_complement? "(" + obj.client_commande_complement.replace("À l'att. de ", '') + ")": [obj.client_commande_titre, obj.client_commande_prenom, obj.client_commande_nom].filter(Boolean).join(" "),
          //   obj.client_commande_co,
          //   obj.client_commande_adresse,
          //   obj.client_commande_case_postale,
          //   [obj.client_commande_npa, obj.client_commande_localite].filter(Boolean).join(" ")]
          //   .filter(Boolean).join("\n");

          // // Client d'envoi
          // let adresse_ = ""
          // if (obj.client_envoi_type_id === this.clientTypes_conf.moral) {
          //   adresse_ = [
          //     obj.client_envoi_entreprise,
          //     obj.client_envoi_complement? "À l'att. de " + obj.client_envoi_complement.replace("À l'att. de ", ''): null,
          //     obj.client_envoi_co,
          //     obj.client_envoi_adresse,
          //     obj.client_envoi_case_postale,
          //     [obj.client_envoi_npa, obj.client_envoi_localite].filter(Boolean).join(" ")
          //   ].filter(Boolean);
          // } else {
          //   adresse_ = [
          //     [obj.client_envoi_titre, obj.client_envoi_prenom, obj.client_envoi_nom].filter(Boolean).join(" "),
          //     obj.client_envoi_co,
          //     obj.client_envoi_adresse,
          //     obj.client_envoi_case_postale,
          //     [obj.client_envoi_npa, obj.client_envoi_localite].filter(Boolean).join(" ")
          //   ].filter(Boolean);
          // }

          // obj["client_envoi_nom_"] = adresse_.join("\n");

          // obj["technicien"] = [obj.technicien_prenom, obj.technicien_nom]
          //   .filter(Boolean).join(" ");

          // Object.keys(obj).forEach(function(key) {
          //   // Formater la date en DD.MM.YYYY
          //   if ((key.includes("date") || key.includes("echeance")) && obj[key] !== null && obj[key] !== "") {
          //     obj[key] = moment(obj[key], process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
          //   }
          // });

          // obj.urgent_echeance_reste = null;
          // if (obj.urgent_echeance !== null) {
          //   obj.urgent_echeance_reste = Math.ceil(Math.max(0, moment(obj.urgent_echeance, process.env.VUE_APP_DATEFORMAT_CLIENT)-new Date())/1000/3600/24)+1;
          // }
        }
      })
      .catch((err) => handleException(err, this));
    },

    // /**
    //  * Show map
    //  */
    // showMap() {
    //   if(this.$refs && this.$refs.mapHandler && !this.mapLoaded){
    //     this.center = {
    //       x: this.affaire.localisation_e,
    //       y: this.affaire.localisation_n
    //     };
    //     this.$refs.mapHandler.initMap(
    //       this.center,
    //       process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM
    //     );
    //     this.$refs.mapHandler.addMarker(this.center.x, this.center.y);
    //     this.$refs.mapHandler.modify.setActive(false);
    //     this.$refs.mapHandler.snap.setActive(false);
    //     this.$refs.mapHandler.modify.on("modifyend", this.onFeatureChange(this));
    //     this.mapLoaded = true;
    //   }
    // },


    // /**
    //  * Open Theme SITN
    //  */
    // openSitnTheme(theme) {
    //   let route;
    //   if (theme === "amenagement_territoire") {
    //       route = process.env.VUE_APP_SITN_AMENAGEMENT_TERRITOIRE_URL;
    //   } else if (theme === "cadastre") {
    //       route = process.env.VUE_APP_SITN_CADASTRE_URL;
    //   } else if (theme === "sites_pollues") {
    //       route = process.env.VUE_APP_SITN_SITES_POLLUES_URL;
    //   } else {
    //     return null;
    //   }
    //   window.open(route + "&map_x=" + this.affaire.localisation_e + "&map_y=" + this.affaire.localisation_n, "_blank");
    // },





  },

  mounted: function() {
    this.searchAffaire();

    // this.$root.$on('mapHandlerReady', () => this.showMap() );
  }
};
</script>
