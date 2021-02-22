<style src="./matdiff_mo.css" scoped></style>
<template src="./matdiff_mo.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
import { checkPermission } from '@/services/helper'

const moment = require('moment')

export default {
  name: "Matdiff",
  data: () => {
    return {
      numerosDifferes: [],
      showConfirmationDialog: false,
    }
  },

  methods: {
    /**
     * Get numeros differes for MO users
     */
    async getNumerosDifferes() {
      let user_id = JSON.parse(localStorage.getItem("infolica_user")).id;
      
      let params =  "?role=mo&user_id=" + user_id
      if (checkPermission(process.env.VUE_APP_FONCTION_ADMIN)) {
        params =  "?role=mo"
      }

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = JSON.parse(response.data);
          tmp.forEach(x => {
            x.numero = x.numero.join(', '),
            x.diff_entree = Number(moment(x.diff_entree, process.env.VUE_APP_DATEFORMAT_WS))
          });
          this.numerosDifferes = tmp;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * openAffaire
     */
    async openAffaire(affaire_id) {
      this.$router.push({ name: "AffairesDashboard", params: {id: affaire_id}});
    }

  },

  mounted: function() {
    this.getNumerosDifferes();
  }
};
</script>

