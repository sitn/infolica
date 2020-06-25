<style src="./infosGenerales.css" scoped></style>
<template src="./infosGenerales.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission} from '@/services/helper';

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
      infoGenReadonly: true,
      affaireReadonly: true
    };
  },

  methods: {
    /**
     * Ouvre la page de consultation/édition de client
     */
    openClientEditor(field_name) {
      let routedata = this.$router.resolve({name: 'ClientsEdit', params: {id: this.affaire[field_name]}});
      window.open(routedata.href, "_blank");
    },
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
      this.infoGenReadonly = true;
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
      else
        formData.append("date_validation", null);
      if (this.affaire.date_envoi)
        formData.append(
          "date_envoi", this.affaire.date_envoi? 
          moment(this.affaire.date_envoi, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      else
        formData.append("date_cloture", null);
      if (this.affaire.date_cloture)
        formData.append(
          "date_cloture", this.affaire.date_cloture? 
          moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      else
        formData.append("date_cloture", null);
        
      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => { //response =>{
          // this.handleSaveDataSuccess(response);
          this.infoGenReadonly = true;
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
    this.copyAffaire();
    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



