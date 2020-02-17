<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
import {
  checkLogged,
} from "@/services/helper";

export default {
  name: "AffairesDashboard",
  props: {},
  data: () => ({
    affaire: [],
  }),

  methods: {

    // /*
    //  * Init Cadastres list
    //  */
    // initCadastresList() {
    //   getCadastres()
    //     .then(response => {
    //       if (response && response.data) {
    //         this.cadastre_liste = response.data.map(function(obj) {
    //           return obj.nom;
    //         });
    //       }
    //     }).catch(err => {
    //       alert("error: " + err.message);
    //     });
    // },

    // /*
    //  * Init Types affaires list
    //  */
    // async initTypesAffairesList() {
    //   getTypesAffaires()
    //     .then(response => {
    //       if (response && response.data) {
    //         this.types_affaires = response.data.map(function(obj) {
    //           return obj.nom;
    //         });
    //       }
    //     }).catch(err => {
    //       alert("error: " + err.message);
    //     });
    // },

    // /**
    //  * Clear the form
    //  */
    // clearForm() {
    //   this.search.cadastre = null;
    //   this.search.type = null;
    // },
    
    /*
     * SEARCH AFFAIRE
     */
    async searchAffaire() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.affaire = response.data;
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },
  },

  mounted: function() {
    checkLogged();
    this.searchAffaire();
  }
};
</script>



