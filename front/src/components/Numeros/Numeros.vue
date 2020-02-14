<style src="./numeros.css" scoped></style>
<template src="./numeros.html"></template>


<script>
import {
  checkLogged,
  getCadastres,
  getTypesNumeros,
  getEtatsNumeros
} from "@/services/helper";

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
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
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
     * Init Types Numeros list
     */
    async initTypesNumerosList() {
      getTypesNumeros()
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
     * Init Etats Numeros list
     */
    async initEtatsNumerosList() {
      getEtatsNumeros()
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
    },

    /*
     * Open numéro in new tab
     */
    doOpenNumero(id) {
      window.setTimeout
      let routeData = this.$router.resolve('/numeros/' + id);
      window.open(routeData.href, '_blank');
    }
  },

  mounted: function() {
    checkLogged();
    this.initCadastresList();
    this.initTypesNumerosList();
    this.initEtatsNumerosList();
    // this.cadastre_liste = getCadastres();
    // getTypesNumeros();
    // getEtatsNumeros();
    this.searchNumeros();
  }
};
</script>

