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
    affaires: [],
    search: {
      cadastre: null,
      type: null,
    }
  }),

  methods: {

    /*
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
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
            this.types_affaires = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
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
    },
    
    /*
     * SEARCH AFFAIRE
     */
    async searchAffaires() {
      var formData = new FormData();
      if (this.search.cadastre) formData.append("cadastre", this.search.cadastre);
      if (this.search.type) formData.append("type_affaire", this.search.type);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RECHERCHE_AFFAIRES_ENDPOINT,
          formData
        ).then(response => {
          if (response && response.data) {
            this.affaires = response.data;
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenAffaire(id) {
      let routeData = this.$router.resolve('/affaires/' + id);
      window.open(routeData.href, '_blank');
    }
  },

  mounted: function() {
    checkLogged();
    this.initCadastresList();
    this.initTypesAffairesList();
    this.searchAffaires();
  }
};
</script>



