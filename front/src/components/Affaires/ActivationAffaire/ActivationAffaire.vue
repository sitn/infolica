<style src="./activationAffaire.css"></style>
<template src="./activationAffaire.html"></template>

// PROCESSUS
//  - SUPPRIMER NUMEROS RELATIONS

<script>
import { handleException } from "@/services/exceptionsHandler";
import NewStepSetter from "@/components/Utils/NewStepSetter/NewStepSetter.vue";

import moment from "moment";

export default {
  name: "ActivationAffaire",
  props: {
    affaire: Object
  },
  components: {
    NewStepSetter,
  },
  data: () => {
    return {
      disabledConfirmBtn: true,
      nouvelle_etape_affaire_id: null,
      showActivationDialog: false,
      showProgressBar: false,
    };
  },
  methods: {
    openActivationDialog(){
      this.showActivationDialog = true;
      this.disabledConfirmBtn = true;
    },

    /**
     * (Re-)Activation function
     */
    async activateAffaire() {
      this.showProgressBar = true;
      
      let formData = new FormData();
      formData.append('affaire_id', this.affaire.id);
      formData.append('etape_id', this.nouvelle_etape_affaire_id);
      
      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ACTIVATE_AFFAIRE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
        ).then(response => {
          if (response && response.data) {
            this.$root.$emit('ShowMessage', "L''affaire a bien été réactivée.")
            this.showProgressBar = false;
            this.$router.go(0);
          }
        }).catch(err => {
          handleException(err, this);
          this.showProgressBar = false;
        });
      },


    /**
     * Enregistrer le nouvel état des numéros
     */
    async saveNewEtatNumero(num) {
      var formData = new FormData();
      formData.append("id", num.numero_id);
      formData.append("etat_id", num.numero_etatFutur_id);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        )
        .then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * Enregistrer l'historique du changement d'état du numéro
     */
    async saveNewEtatHistoryNumero(num) {
      var formData = new FormData();
      formData.append("numero_id", num.numero_id);
      formData.append("numero_etat_id", num.numero_etatFutur_id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_ETAT_HISTO_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        )
        .then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * set nouvelle_etape_affaire_id
     */
    setNewStepId(new_step_id) {
      this.nouvelle_etape_affaire_id = new_step_id;
      this.disabledConfirmBtn = false;
    }

  },
};
</script>