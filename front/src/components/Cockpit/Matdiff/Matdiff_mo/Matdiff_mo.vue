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
  },
  data: () => {
    return {
      affaires: [],
      loading: false,
      plural: "",
      selectedOperateur_id: JSON.parse(localStorage.getItem("infolica_user")).id,
    }
  },

  methods: {
    async initSelectedOperateur() {
      return new Promise((resolve) => {
        if (checkPermission(process.env.VUE_APP_FONCTION_ADMIN) || getCurrentUserRoleId() === Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)) {
          this.selectedOperateur_id = -1;
        } else {
          this.selectedOperateur_id = JSON.parse(localStorage.getItem("infolica_user")).id;
        }
        resolve(this.selectedOperateur_id);
      });
    },


    /**
     * Get numeros differes for MO users
     */
    async getNumerosDifferes() {
      this.loading = true;

      let params = "?role=mo";
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
    }
  },

  mounted: function() {
    this.initSelectedOperateur().then(() => {
      this.getNumerosDifferes();
    });
  }
};
</script>

