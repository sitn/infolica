<style src="./infosGenerales.css" scoped></style>
<template src="./infosGenerales.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'

const moment = require("moment");

export default {
  name: "AffairesDashboard",
  props: {
    affaire: {type: Object}
    },
  components: {},
  data() {
    return {
      affaire_backup: {},
      readonly: true
    };
  },

  methods: {
    /*
     * CREATE COPY OF AFFAIRE
     */
    copyAffaire() {
      Object.assign(this.affaire_backup, this.affaire);
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
    async onConfirmEdit() {
      var formData = new FormData();
      formData.append("id_affaire", this.affaire.id);
      if (this.affaire.nom !== "-") formData.append("nom", this.affaire.nom || null);
      if (this.affaire.information !== "-")
        formData.append("information", this.affaire.information || null);
      if (this.affaire.vref !== "-") formData.append("vref", this.affaire.vref || null);
      if (this.affaire.date_validation)
        formData.append(
          "date_validation", this.affaire.date_validation?
          moment(this.affaire.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      if (this.affaire.date_cloture)
        formData.append(
          "date_cloture", this.affaire.date_cloture? 
          moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => { //response =>{
          // this.handleSaveDataSuccess(response);
          this.readonly = true;
          this.$parent.setAffaire();
          this.copyAffaire();
        })
        //Error 
        .catch(err => {
          handleException(err, this); 
        });
    }
  },

  mounted: function() {
    this.copyAffaire()
  }
};
</script>



