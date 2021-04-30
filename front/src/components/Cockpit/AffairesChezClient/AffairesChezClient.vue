<style src="./affairesChezClient.css" scoped></style>
<template src="./affairesChezClient.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'

const moment = require('moment')

export default {
  name: "AffairesChezClient",
  props: {
    affaireTypes: Array,
    operateurs: Array,
    selectedOperateur_id_parent: {type: Number, default: () => -1}
  },
  data: () => {
    return {
      affaires: [{}],
      affaires_bk: [{}],
      affaireTypePPE_conf: Number(process.env.VUE_APP_TYPE_AFFAIRE_PPE),
      selectedTypeAffaire_id: -1,
      selectedOperateur_id: JSON.parse(localStorage.getItem("infolica_user")).id,
      etapeChezClient_conf: Number(process.env.VUE_APP_ETAPE_CHEZ_CLIENT_ID),      
      etapeDevis_conf: Number(process.env.VUE_APP_ETAPE_DEVIS_ID),      
    }
  },

  methods: {
    /**
     * get Affaires
     */
    async getAffaire() {
      let params = "?etape_id=" + this.etapeChezClient_conf + "," + this.etapeDevis_conf;

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;

          tmp.forEach(x => x.etape_datetime = Number(moment(x.etape_datetime, process.env.VUE_APP_DATETIMEFORMAT_WS)));
          this.affaires_bk = tmp;
          
          this.filterAffaires();
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * Filter Affaires
     */
    filterAffaires() {
      //filter affaire type PPE and step client
      this.affaires = this.affaires_bk;

      if (this.selectedOperateur_id > 0) {
        this.affaires = this.affaires.filter(x => x.operateur_id === this.selectedOperateur_id);
      }

      if (this.selectedTypeAffaire_id > 0) {
        this.affaires = this.affaires.filter(x => x.affaire_type_id === this.selectedTypeAffaire_id);
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

    // init selectedOperateur_id from parent component
    this.selectedOperateur_id = this.selectedOperateur_id_parent;
  }
};
</script>

