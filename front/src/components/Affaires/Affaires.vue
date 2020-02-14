<style src="./affaires.css" scoped></style>
<template src="./affaires.html"></template>


<script>
import {
  checkLogged,
  getCadastres,
  getTypesAffaires,
} from "@/services/helper";

export default {
  name: "Affaires",
  props: {},
  data: () => ({
    cadastre_liste: [],
    types_affaires: [],
    search: {
      cadastre: null,
      type: null,
    }
  }),

  methods: {
    /*
     * SEARCH AFFAIRE
     */
    // async searchAffaires() {
    //   var formData = new FormData();
    //   if (this.search.cadastre) formData.append("cadastre", this.search.cadastre);

    //   if (this.search.type) formData.append("type_numero", this.search.type);

    //   this.$http
    //     .post(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_RECHERCHE_NUMEROS_ENDPOINT,
    //       formData
    //     )
    //     .then(response => {
    //       if (response && response.data) {
    //         this.numeros = response.data;
    //       }
    //     })
    //     .catch(err => {
    //       alert("error : " + err.message);
    //     });
    // },

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
     * Init Types affaires list
     */
    async initTypesAffairesList() {
      getTypesAffaires()
        .then(response => {
          if (response && response.data) {
            this.types_affaires = response.data.map(function(obj) {
              return obj.nom;
            });
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    // /*
    //  * Init Etats Numeros list
    //  */
    // async initEtatsNumerosList() {
    //   getEtatsNumeros()
    //     .then(response => {
    //       if (response && response.data) {
    //         this.etats_numeros = response.data.map(function(obj) {
    //           return obj.nom;
    //         });
    //       }
    //     })

    //     .catch(err => {
    //       alert("error: " + err.message);
    //     });
    // },

    /**
     * Clear the form
     */
    clearForm() {
      this.search.cadastre = null;
      this.search.type = null;
    },

    // /*
    //  * Open numéro in new tab
    //  */
    // doOpenNumero(id) {
    //   window.setTimeout
    //   let routeData = this.$router.resolve('/numeros/' + id);
    //   window.open(routeData.href, '_blank');
    // }
  },

  mounted: function() {
    checkLogged();
    this.initCadastresList();
    this.initTypesAffairesList();
    // this.initEtatsNumerosList();
    // this.searchAffaires();
  }
};
</script>



