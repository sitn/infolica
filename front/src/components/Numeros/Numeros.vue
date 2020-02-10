<style src="./numeros.css" scoped></style>
<template src="./numeros.html"></template>


<script>
import { checkLogged } from "@/services/helper";

export default {
  name: "Numeros",
  props: {},
  data: () => ({
    numeros: [],
    cadastre_liste: [],
    types_numeros: [],
    etats_numeros: [],
    search: {
      cadastre: null,
      type: null,
      etat: null
    }
  }),

  methods: {
    /*
     * SEARCH NUMEROS
     */
    async searchNumeros() {
      var formData = new FormData();
      if (this.search.cadastre)
        formData.append("cadastre", this.search.cadastre);

      if (this.search.type) formData.append("type_numero", this.search.type);

      if (this.search.etat) formData.append("etat", this.search.etat);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RECHERCHE_NUMEROS_ENDPOINT,
          formData
        )

        .then(response => {
          if (response && response.data) {
            this.numeros = response.data;
          }
        })

        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * Get Cadastres
     */
    async getCadastres() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT
        )

        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = response.data.map(function(obj) {
              return obj.nom;
            });
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    /*
     * Get Types Numeros
     */
    async getTypesNumeros() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT
        )

        .then(response => {
          if (response && response.data) {
            this.types_numeros = response.data.map(function(obj) {
              return obj.nom;
            });
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    /*
     * Get Etats Numeros
     */
    async getEtatsNumeros() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT
        )

        .then(response => {
          if (response && response.data) {
            this.etats_numeros = response.data.map(function(obj) {
              return obj.nom;
            });
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.search.cadastre = null;
      this.search.type = null;
      this.search.etat = null;
    }
  },

  mounted: function() {
    checkLogged();
    this.getCadastres();
    this.getTypesNumeros();
    this.getEtatsNumeros();
    this.searchNumeros();
  }
};
</script>

