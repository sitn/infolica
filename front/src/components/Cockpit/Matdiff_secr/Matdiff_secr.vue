<style src="./matdiff_secr.css" scoped></style>
<template src="./matdiff_secr.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
import { getDocument } from '@/services/helper'

const moment = require("moment");

export default {
  name: "Matdiff",
  data: () => {
    return {
      numerosDifferes: [{}],
      selectedItem: [],
      showConfirmationDialog: false,
    }
  },

  methods: {
    /**
     * Get numeros differes
     */
    async getNumerosDifferes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT + "?role=secr",
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
     * generateReq_confirmation
     */
    generateReq(item) {
      this.selectedItem = item;
      this.showConfirmationDialog = true;
    },
    
    /**
     * onCancel req radiation
     */
    onCancelGenerateReq() {
      this.selectedItem = [];
      this.showConfirmationDialog = false;
    },

    /**
     * on confirm Generate req radiation
     */
    async onConfirmGenerateReq() {
      let formData = new FormData();
      formData.append("template", "ReqMatDiff");
      formData.append("values", JSON.stringify({
        "ANNEE": new Date().getFullYear(),
        "CADASTRE": this.selectedItem.cadastre,
        "BIENS_FONDS": this.selectedItem.numero,
        "DATE": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT)
      }));

      getDocument(formData).then(response => {
        // update numero_differe state
        let promises = [];
        this.selectedItem.diff_id.forEach(num => promises.push(this.updateNumeroDiff(num)));

        Promise.all(promises).then(() => this.getNumerosDifferes())
        .catch(err => handleException(err));

        this.$root.$emit("ShowMessage", "Le fichier '" + response + "' se trouve dans le dossier 'Téléchargement'");
      }).catch(err => handleException(err, this));
    },


    /**
     * update Numero Differe
     */
    async updateNumeroDiff(diff_id) {
      let formData = new FormData();
      formData.append('numero_diff_id', diff_id);
      formData.append('req_radiation', true);

      return new Promise ((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    }

  },

  mounted: function() {
    this.getNumerosDifferes();
  }
};
</script>

