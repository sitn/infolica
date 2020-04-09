<style src="./suiviMandat.css" scoped></style>
<template src="./suiviMandat.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'

const moment = require("moment");

export default {
  name: "SuiviMandat",
  props: {},
  data: () => ({
    showNewSuiviMandatBtn: false,
    showModifiedSuiviMandat: false,
    needToCreateSuiviMandat: false,
    operateurs_liste: [],
    chefsProjetMO_liste: [],
    showCreatedSuiviMandat: false,
    suiviMandat: {}
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-SUIVI MANDAT
     */
    async searchSuiviMandat() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_SUIVI_MANDAT_ENDPOINT +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.suiviMandat = response.data;
          } else {
            // Il n'existe pas encore de suivi de mandat pour cette affaire
            this.needToCreateSuiviMandat = true;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Cherche les opérateurs
     */
    async searchOperateurs() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.operateurs_liste = response.data;
            this.chefsProjetMO_liste = response.data
              .filter(x => {
                return x.responsable;
              })
              .map(x => ({
                id: x.id,
                nom: [x.nom, x.prenom].join(" "),
                toLowerCase: () => [x.nom, x.prenom].join(" ").toLowerCase(),
                toString: () => [x.nom, x.prenom].join(" ")
              }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Création d'un nouveau suivi
     */
    newSuiviMandat() {
      var formData = new FormData();
      formData.append("affaire_id", this.$route.params.id);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_SUIVI_MANDAT_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response) {
            this.showCreatedSuiviMandat = true;
            this.searchSuiviMandat();
            this.needToCreateSuiviMandat = false;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    onCancelEditSuiviMandat() {
      this.searchSuiviMandat();
    },

    onConfirmEditSuiviMandat() {
      var formData = new FormData();
      if (this.suiviMandat.id) formData.append("id", this.suiviMandat.id);
      if (this.suiviMandat.affaire_id)
        formData.append("affaire_id", this.suiviMandat.affaire_id);
      if (this.suiviMandat.av_11)
        formData.append("av_11", this.suiviMandat.av_11);
      if (this.suiviMandat.av_12)
        formData.append("av_12", this.suiviMandat.av_12);
      if (this.suiviMandat.av_21)
        formData.append("av_21", this.suiviMandat.av_21);
      if (this.suiviMandat.av_31)
        formData.append("av_31", this.suiviMandat.av_31);
      if (this.suiviMandat.av_32)
        formData.append("av_32", this.suiviMandat.av_32);
      if (this.suiviMandat.av_33)
        formData.append("av_33", this.suiviMandat.av_33);
      if (this.suiviMandat.av_41)
        formData.append("av_41", this.suiviMandat.av_41);
      if (this.suiviMandat.av_51)
        formData.append("av_51", this.suiviMandat.av_51);
      if (this.suiviMandat.pdt_11)
        formData.append("pdt_11", this.suiviMandat.pdt_11);
      if (this.suiviMandat.pdt_12)
        formData.append("pdt_12", this.suiviMandat.pdt_12);
      if (this.suiviMandat.pdt_21)
        formData.append("pdt_21", this.suiviMandat.pdt_21);
      if (this.suiviMandat.pdt_22)
        formData.append("pdt_22", this.suiviMandat.pdt_22);
      if (this.suiviMandat.pdt_31)
        formData.append("pdt_31", this.suiviMandat.pdt_31);
      if (this.suiviMandat.pdt_41)
        formData.append("pdt_41", this.suiviMandat.pdt_41);
      if (this.suiviMandat.pdt_42)
        formData.append("pdt_42", this.suiviMandat.pdt_42);
      if (this.suiviMandat.ap_11)
        formData.append("ap_11", this.suiviMandat.ap_11);
      if (this.suiviMandat.ap_12)
        formData.append("ap_12", this.suiviMandat.ap_12);
      if (this.suiviMandat.ap_21)
        formData.append("ap_21", this.suiviMandat.ap_21);
      if (this.suiviMandat.ap_22)
        formData.append("ap_22", this.suiviMandat.ap_22);
      if (this.suiviMandat.ap_31)
        formData.append("ap_31", this.suiviMandat.ap_31);
      if (this.suiviMandat.ap_32)
        formData.append("ap_32", this.suiviMandat.ap_32);
      if (this.suiviMandat.ap_33)
        formData.append("ap_33", this.suiviMandat.ap_33);
      if (this.suiviMandat.ap_41)
        formData.append("ap_41", this.suiviMandat.ap_41);
      if (this.suiviMandat.ap_42)
        formData.append("ap_42", this.suiviMandat.ap_42);
      if (this.suiviMandat.visa)
        formData.append("visa", this.suiviMandat.visa.id);
      if (this.suiviMandat.date)
        formData.append(
          "date",
          moment(this.suiviMandat.date, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http
        .put(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_SUIVI_MANDAT_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response) {
            this.showModifiedSuiviMandat = true;
            this.searchSuiviMandat();
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    }
  },

  mounted: function() {
    this.searchSuiviMandat();
    this.searchOperateurs();
  }
};
</script>



