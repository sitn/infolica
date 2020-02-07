<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'Clients',
  props: {},
  data: () => ({
      clients: [],
      search: {
        nom: null,
        prenom: null,
        entreprise: null,
        adresse: null,
        localite: null,
        mail: null
      }
  }),
  methods: {
        /**
         * Search clients
        */
        async searchClients () {
          var formData = new FormData();
          if(this.search.nom)
            formData.append("nom", this.search.nom);

          if(this.search.prenom)
            formData.append("prenom", this.search.prenom);

          if(this.search.entreprise)
            formData.append("entreprise", this.search.entreprise);

          if(this.search.adresse)
            formData.append("adresse", this.search.adresse);

          if(this.search.localite)
            formData.append("localite", this.search.localite);

          if(this.search.mail)
            formData.append("mail", this.search.mail);

          this.$http.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_ENDPOINT, 
            formData
          )
          .then(response =>{
            if(response && response.data){
              this.clients = response.data;
            }
          })
          //Error 
          .catch(err => {
            alert("error : " + err.message);  
          })
        },

        /**
         * Clear the form
         */
        clearForm () {
          this.search.nom = null;
          this.search.prenom = null;
          this.search.entreprise = null;
          this.search.adresse = null;
          this.search.localite = null;
          this.search.mail = null;
        },
  },

  mounted: function(){
    checkLogged();
    this.searchClients();
  }
}
</script>

