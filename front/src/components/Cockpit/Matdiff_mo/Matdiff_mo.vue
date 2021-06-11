<style src="./matdiff_mo.css" scoped></style>
<template src="./matdiff_mo.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
import { checkPermission, getCurrentUserRoleId } from '@/services/helper'

const moment = require('moment')

export default {
  name: "Matdiff_mo",
  props: {
    operateurs: {type: Array},
    selectedOperateur_id_parent: {type: Number, default: () => -1}
  },
  data: () => {
    return {
      affaires: [{}],
      affaires_bk: [{}],
      selectedOperateur_id: JSON.parse(localStorage.getItem("infolica_user")).id,
    }
  },

  methods: {
    /**
     * Get numeros differes for MO users
     */
    async getNumerosDifferes() {
      let params =  "?role=mo&user_id=" + this.selectedOperateur_id;
      if (checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ||
          getCurrentUserRoleId() === Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)) {
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
          let tmp = response.data;
          tmp.forEach(x => {
            x.numero = x.numero.join(', '),
            x.diff_entree = Number(moment(x.diff_entree, process.env.VUE_APP_DATEFORMAT_WS))
          });
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
        this.affaires = this.affaires.filter(x => x.diff_operateur_id === this.selectedOperateur_id);
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
    this.getNumerosDifferes();

    // init selectedOperateur_id from parent component
    this.selectedOperateur_id = this.selectedOperateur_id_parent;
  }
};
</script>

