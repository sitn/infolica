<style src="./ppe.css" scoped></style>
<template src="./ppe.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
// import { checkPermission } from '@/services/helper'

const moment = require('moment')

export default {
  name: "PPE",
  props: {
    operateurs: Array
  },
  data: () => {
    return {
      affairesClient: [{}],
      affairesClient_bk: [{}],
      affaireTypePPE_conf: Number(process.env.VUE_APP_TYPE_AFFAIRE_PPE),
      etapeChezClient_conf: Number(process.env.VUE_APP_ETAPE_CHEZ_CLIENT_ID),
      currentUser_id: JSON.parse(localStorage.getItem("infolica_user")).id,
      
    }
  },

  methods: {
    /**
     * get Affaires
     */
    async getAffaire() {
      let params = "?type_id=" + this.affaireTypePPE_conf + "&etape_id=" + this.etapeChezClient_conf;

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = JSON.parse(response.data);

          tmp.forEach(x => x.etape_datetime = Number(moment(x.etape_datetime, process.env.VUE_APP_DATETIMEFORMAT_WS)));
          this.affairesClient_bk = tmp;
          
          this.filterAffairesClient();
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * Filter AffairesClient
     */
    filterAffairesClient() {
      //filter affaire type PPE and step client
      this.affairesClient = this.affairesClient_bk;

      if (this.currentUser_id > 0) {
        this.affairesClient = this.affairesClient.filter(x => x.operateur_id === this.currentUser_id);
      }

    },

    /**
     * openAffaire
     */
    async openAffaire(affaire_id) {
      this.$router.push({ name: "AffairesDashboard", params: {id: affaire_id}});
    }

  },

  mounted: function() {
    this.getAffaire();
  }
};
</script>

