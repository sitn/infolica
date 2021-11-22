<style src="./matdiff_ctrl.css" scoped></style>
<template src="./matdiff_ctrl.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'

const moment = require('moment')

export default {
  name: "Matdiff_ctrl",
  props: {
    operateurs: {type: Array},
  },
  data: () => {
    return {
      affaires: [],
      loading: false,
      plural: "",
      selectedOperateur_id: -1,
    }
  },

  methods: {
    /**
     * Get numeros differes for coordinateurs users
     */
    async getNumerosDifferes() {
      this.loading = true;

      let params =  "?role=coord";
      if (this.selectedOperateur_id >= 0) {
        params += "&user_id=" + this.selectedOperateur_id;
      }

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          tmp.forEach(x => {
            x.numero = x.numero.join(', '),
            x.diff_entree = Number(moment(x.diff_entree, process.env.VUE_APP_DATEFORMAT_WS))
          });
          this.affaires = tmp;

          // set plural
          if (tmp.length > 1) {
            this.plural = "s";
          } else {
            this.plural = "";
          }

          this.loading = false;
        }
      }).catch(err => {
        handleException(err, this);
        this.loading = false;
      });
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

