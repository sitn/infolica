<style src="./suivi.css" scoped></style>
<template src="./suivi.html"></template>


<script>
import { checkLogged, getCurrentDate } from "@/services/helper";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  name: "suivi",
  mixins: [validationMixin],
  props: {},
  components: {},
  data: () => {
    return {
      affaire_suivi: [],
      etapes_list: [],
      lastRecord: null,
      dataSaved: false,
      showNewEtapeBtn: false,
      showEtapeDialog: false,
      new_etape: {
        etape: null,
        date: getCurrentDate(),
        remarque: ""
      }
    };
  },

  // Validations
  validations: {
    new_etape: {
      etape: { required },
      date: { required }
    }
  },

  methods: {
    /*
     * SEARCH AFFAIRE SUIVI
     */
    async searchAffaireSuivi() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_SUIVI_ENDPOINT +
            this.$route.params.id
        )
        .then(response => {
          if (response.data) {
            this.affaire_suivi = response.data;
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * SEARCH ETAPES
     */
    async searchEtapes() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_ETAPES_INDEX_ENDPOINT
        )
        .then(response => {
          if (response.data) {
            this.etapes_list = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /**
     * Ouvrir div nouvel étape
     */
    addEtape: function() {
      this.new_etape.showDiv = !this.new_remarque.showDiv;
    },

    /**
     * Enregistrer une nouvelle étape
     */
    saveNewEtape: function() {
      if (this.new_etape.etape != null && this.new_etape.date != null) {
        var formData = new FormData();
        formData.append("affaire_id", this.$route.params.id);
        if (this.new_etape.etape.id) {
          formData.append("etape_id", this.new_etape.etape.id);
          this.lastRecord = this.new_etape.etape.nom;
          }
        if (this.new_etape.date) formData.append("date", this.new_etape.date);
        if (this.new_etape.remarque)
          formData.append("remarque", this.new_etape.remarque);

        this.$http
          .post(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRE_ETAPES_ENDPOINT,
            formData
          )
          .then(response => {
            if (response.data) {
              this.searchAffaireSuivi();
              // handle success
              this.dataSaved = true;
            }
          })
          .catch(err => {
            alert("error: " + err);
          });
      }
    },

    /**
     * Confirmer l'édition d'état
     */
    onConfirmEditEtape: function() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        this.saveNewEtape();
        this.clearForm();
      }
    },

    /**
     * Annuler l'édition d'état
     */
    onCancelEditEtape: function() {
      this.clearForm();
    },

    /**
     * Clear form
     */
    clearForm() {
      this.saveNewEtape();
        this.$v.$reset();
        this.showEtapeDialog = false;
        this.new_etape.etape = null;
        this.new_etape.date = getCurrentDate();
        this.new_etape.remarque = "";
    },

    // /**
    //   * Handle save data success
    //   */
    //   handleSaveDataSuccess () {
    //     this.lastRecord = this.new_etape.etape;
    //     this.dataSaved = true;
    //   },

    /*
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      const field = this.$v.new_etape[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    }
  },

  mounted: function() {
    checkLogged();
    this.searchAffaireSuivi();
    this.searchEtapes();
  }
};
</script>



