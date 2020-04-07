<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
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
import {handleException} from '@/services/exceptionsHandler'

const moment = require("moment");

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
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
      affaire: {},
      affaire_backup: {},
      affaire_numeros: [],
      readonly: true
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
                if (
                  (obj[key] === null || obj[key] === "") &&
                  !key.includes("date")
                )
                  obj[key] = "-";
              });
              this.affaire = obj;
              Object.assign(this.affaire_backup, obj);
              resolve({
                x: response.data.localisation_e,
                y: response.data.localisation_n
              });
            }
          })
          .catch(() => reject);
      });
    },

    /**
     * Annuler l'édition du formulaire
     */
    onCancelEdit() {
      Object.assign(this.affaire, this.affaire_backup);
      this.readonly = true;
    },

    /**
     * Enregistrer les modifications
     */
    onConfirmEdit() {
      var formData = new FormData();
      alert(this.affaire.id)
      formData.append("id_affaire", this.affaire.id);
      if (this.affaire.nom && this.affaire.nom !== "-") formData.append("nom", this.affaire.nom);
      if (this.affaire.information && this.affaire.information !== "-")
        formData.append("information", this.affaire.information);
      if (this.affaire.vref && this.affaire.vref !== "-") formData.append("vref", this.affaire.vref);
      if (this.affaire.date_validation && this.affaire.date_validation !== "-")
        formData.append(
          "date_validation",
          moment(new Date(new Date(this.affaire.date_validation))).format(
            "YYYY-MM-DD"
          )
        );
      if (this.affaire.date_cloture && this.affaire.date_cloture !== "-")
        formData.append(
          "date_cloture",
          moment(new Date(new Date(this.affaire.date_cloture))).format(
            "YYYY-MM-DD"
          )
        );

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response =>{
          this.handleSaveDataSuccess(response);
          this.searchAffaire()
        })
        //Error 
        .catch(err => {
          handleException(err, this); 
        });
    }
  },

  mounted: function() {
    let _this = this;
    this.searchAffaire().then(function(center) {
      _this.$refs.mapHandler.initMap(
        center,
        process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM
      );
      _this.$refs.mapHandler.addMarker(center.x, center.y);
    });
  }
};
</script>



