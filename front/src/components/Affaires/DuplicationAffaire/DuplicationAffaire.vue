<style src="./duplicationAffaire.css" scoped></style>
<template src="./duplicationAffaire.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'

export default {
  name: "duplicationAffaire",
  props: {
    affaire: {type: Object}
  },
  components: {},
  data: () => ({
    showDuplicationAffaireForm: false,
    types_modifs_affaire_list: [],
    type_modif_affaire: null,
    affaire_numeros_anciens: [],
    affaire_numeros_nouveaux: []
  }),

  methods: {
    /*
    * Init types modifications affaire list
    */
    initTypesModifsAffaireList() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TYPES_MODIF_AFFAIRE_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      )
      .then(response =>{
        if (response && response.data) {
          this.types_modifs_affaire_list = response.data;
        }
      })
      //Error 
      .catch(err => {
        handleException(err, this);
      });
    },

    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.affaire_numeros_all = response.data;
            this.affaire_numeros_nouveaux = response.data.filter(
              x => x.affaire_numero_type === "Nouveau"
            );
            this.affaire_numeros_anciens = response.data.filter(
              x => x.affaire_numero_type === "Ancien"
            );
            this.affaire_numeros_nouveaux.forEach(function(element) {
              if (element.numero_etat === "Abandonné") element.active = false;
              else if (element.numero_etat === "Projet") element.active = true;
            });
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    }
  },

  mounted: function() {
    this.initTypesModifsAffaireList();
    this.searchAffaireNumeros();
  }
};
</script>



