<style src="./matdiff.css" scoped></style>
<template src="./matdiff.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
// import { checkPermission, getOperateurs, stringifyAutocomplete } from '@/services/helper'


export default {
  name: "Matdiff",
  data: () => {
    return {
      numerosDifferes: [],
    }
  },

  methods: {
    /**
     * Get numeros differes
     */
    async getNumerosDifferes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = JSON.parse(response.data);
          tmp.forEach(x => x.numero = x.numero.join(', '));
          this.numerosDifferes = tmp;
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * Generate req radiation
     */
    generateReq() {
      alert("bloc en construction")
      // to be build
    }
  },

  mounted: function() {
    this.getNumerosDifferes();
  }
};
</script>

