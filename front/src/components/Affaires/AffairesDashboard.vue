<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
import InfosGenerales from "@/components/Affaires/InfosGenerales/InfosGenerales.vue";
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import NumerosAffaire from "@/components/Affaires/NumerosAffaire/NumerosAffaire.vue";
import Documents from "@/components/Affaires/Documents/Documents.vue";
import Suivi from "@/components/Affaires/Suivi/Suivi.vue";
import Preavis from "@/components/Affaires/Preavis/Preavis.vue";
import Facturation from "@/components/Facturation/Facturation.vue";
import Remarques from "@/components/Affaires/Remarques/Remarques.vue";
import ControleMutation from "@/components/Affaires/ControleMutation/ControleMutation.vue";
import ControlePPE from "@/components/Affaires/ControlePPE/ControlePPE.vue";
import SuiviMandat from "@/components/SuiviMandat/SuiviMandat.vue";

import moment from "moment";

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
    InfosGenerales,
    MapHandler,
    NumerosAffaire,
    Documents,
    Suivi,
    Preavis,
    Facturation,
    Remarques,
    ControleMutation,
    ControlePPE,
    SuiviMandat
  },
  data() {
    return {
      affaire: {}
    };
  },

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
              this.$route.params.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response.data) {
              var obj = response.data;
              obj["client"] = [
                obj.client_entreprise,
                obj.client_titre,
                obj.client_commande_nom,
                obj.client_prenom
              ]
                .filter(Boolean)
                .join(" ");
              obj["client_par"] = [
                obj.client_par_entreprise,
                obj.client_par_titre,
                obj.client_par_commande_nom,
                obj.client_par_prenom
              ]
                .filter(Boolean)
                .join(" ");
              obj["technicien"] = [obj.technicien_prenom, obj.technicien_nom]
                .filter(Boolean)
                .join(" ");
              obj["responsable"] = [obj.responsable_prenom, obj.responsable_nom]
                .filter(Boolean)
                .join(" ");
              Object.keys(obj).forEach(function(key) {
                // Mettre un tiret à toutes les entrées nulles sauf les dates
                if (
                  (obj[key] === null || obj[key] === "") &&
                  !key.includes("date")
                ) {
                  obj[key] = "-";
                } 
                // Formater la date en DD.MM.YYYY
                if (key.includes("date") && obj[key] !== null && obj[key] !== "") {
                  obj[key] = String(moment(obj[key], process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT))
                }
              });
              resolve(obj);
            }
          })
          .catch(() => reject);
      });
    },

    /**
     * Set affaire
     */
    async setAffaire() {
      this.affaire = await this.searchAffaire();
      this.getAffaireData();
    },

    /**
     * Get affaire data before showing the map
     */
    async getAffaireData() {
      this.center = {
        x: this.affaire.localisation_e,
        y: this.affaire.localisation_n
      };
      this.$refs.mapHandler.initMap(
        this.center,
        process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM
      );
      this.$refs.mapHandler.addMarker(this.center.x, this.center.y);
    }
  },

  mounted: function() {
    this.setAffaire();
  }
};
</script>



