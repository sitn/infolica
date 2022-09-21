<style src="./suiviMandat.css" scoped></style>
<template src="./suiviMandat.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {logAffaireEtape, stringifyAutocomplete2, getOperateurs} from '@/services/helper';

const moment = require("moment");

export default {
  name: "SuiviMandat",
  props: {
    affaire: Object,
    permission: Object,
    typesAffaires_conf: Object
  },
  data: () => ({
    chefsProjetMO_liste: [],
    confirmUpdateAffaireDateValidation: false,
    needToCreateSuiviMandat: false,
    selectAll_val: {
      plan_: false,
      desbal_: false,
      geos_: false,
      emol_: false,
      preavis_: false,
    },
    showModifiedSuiviMandat: false,
    showNewSuiviMandatBtn: false,
    suiviMandat: {}
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-SUIVI MANDAT
     */
    async searchSuiviMandat() {
      this.searchOperateurs()
      .then(() => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRE_SUIVI_MANDAT_ENDPOINT +
              this.affaire.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response && response.data) {
              this.suiviMandat = response.data;
              if (this.suiviMandat.date !== null) {
                this.suiviMandat.date = moment(this.suiviMandat.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
              }
              if (this.suiviMandat.av_33 !== null) {
                this.suiviMandat.av_33 = moment(this.suiviMandat.av_33, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
              }
              if (this.suiviMandat.av_32 !== null) {
                this.suiviMandat.av_32 = this.chefsProjetMO_liste.filter(x => x.id === this.suiviMandat.av_32).pop();
              }
              if (this.suiviMandat.visa !== null) {
                this.suiviMandat.visa = this.chefsProjetMO_liste.filter(x => x.id === this.suiviMandat.visa).pop();
              } 
            }else {
              // Il n'existe pas encore de suivi de mandat pour cette affaire
              this.needToCreateSuiviMandat = true;
            }
          })
          .catch(err => {
            handleException(err, this);
          });
      }
      )
    },

    /**
     * Cherche les opérateurs
     */
    async searchOperateurs() {
      return new Promise((resolve, reject) => {
        getOperateurs()
          .then(response => {
            if (response.data) {
              this.chefsProjetMO_liste = stringifyAutocomplete2(response.data, "prenom_nom", null, "prenom_nom");
              
              resolve(response);
            }
          })
          .catch(err => reject(err));
      })
    },

    /**
     * Création d'un nouveau suivi
     */
    newSuiviMandat() {
      var formData = new FormData();
      formData.append("affaire_id", this.affaire.id);

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
      let formData = new FormData();
      for (const elem in this.suiviMandat) {
        if (!["av_32", "av_33", "visa", "date"].includes(elem)) {
          formData.append(elem, this.suiviMandat[elem]);
        }
      }
      if (this.suiviMandat.av_32 && this.suiviMandat.av_32.id) { formData.append("av_32", this.suiviMandat.av_32.id) }
      if (this.suiviMandat.av_33) { formData.append("av_33", moment(this.suiviMandat.av_33, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS)) }
      formData.append("visa", JSON.parse(localStorage.getItem("infolica_user")).id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

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
            this.$root.$emit("ShowMessage", "Le suivi du mandat a été mis à jour avec succès");
            this.searchSuiviMandat();

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_VALIDATION_TECHNIQUE_ID), "Edition du formulaire");

            // reload affaire to update geos_retarder_validation
            this.$root.$emit('setAffaire');
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },


    /**
     * select all in form
     */
    selectAll(term) {
      let fields = document.getElementById(term).getElementsByClassName('md-checkbox');

      for (const x in fields) {
        if (typeof fields[x] === 'object' && !fields[x].classList.contains('md-checked')) {
          for (const elem of fields[x].children) {
            if (elem.className === 'md-checkbox-container') {
              elem.click();
              break
            }
          }
        }
      }
    }
  },

  mounted: function() {
    this.searchSuiviMandat();
    this.searchOperateurs();
  }
};
</script>



