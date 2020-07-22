<style src="./affaires.css" scoped></style>
<template src="./affaires.html"></template>


<script>
import {
  getCadastres,
  getTypesAffaires,
  checkPermission
} from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler';

export default {
  name: "Affaires",
  props: {},
  data: () => ({
    cadastre_liste: [],
    types_affaires: [],
    affaires: [],
    newAffaireAllowed: false,
    search: {
      id: null,
      nom: null,
      cadastre: "",
      type: "",
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
          handleException(err, this);
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
          handleException(err, this);
        });
    },
   

    /**
     * Clear the form
     */
    clearForm() {
      this.search.id = null;
      this.search.nom = null;
      this.search.cadastre = "";
      this.search.type = "";
    },
    
    /*
     * SEARCH AFFAIRE
     */
    async searchAffaires() {
      var formData = new FormData();
      if (this.search.id) {
        formData.append("id", this.search.id);
      }
      
      if (this.search.nom) {
        formData.append("nom", this.search.nom);
      }
      
      if (this.search.cadastre) {
        formData.append("cadastre", this.search.cadastre);
      }
      
      if (this.search.type) {
        formData.append("type_affaire", this.search.type);
      }
      

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RECHERCHE_AFFAIRES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.affaires = response.data;
          }
          this.newAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION);
        }).catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenAffaire(id) {
      this.$router.push({ name: "AffairesDashboard", params: {id}});
    }
  },

  mounted: function() {
    this.initCadastresList();
    this.initTypesAffairesList();
    this.searchAffaires();
  }
};
</script>



