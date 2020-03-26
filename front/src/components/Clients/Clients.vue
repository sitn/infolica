<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'Clients',
  props: {},
  data: () => ({
      clients: [],
      deleteClientActive: false,
      deleteMessage: '',
      currentDeleteId: null,
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
            formData,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            }
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


        /**
         * Call edit client
         */
        callEditClient (id) {
         this.$router.push('/clients/edit/' + id) ; 
        },
        
        /**
         * Call delete client
         */
        callDeleteClient (id, nom, prenom, entreprise) {
          this.currentDeleteId = id;

          if(prenom && nom)
            this.deleteMessage = prenom + ' ' + nom;
          else if(nom)
            this.deleteMessage = nom;
          else
            this.deleteMessage = "-";

          if(entreprise){
            this.deleteMessage = entreprise;
          }

          this.deleteMessage = "Confirmer la suppression du client '<strong>" + this.deleteMessage + "<strong>' ?";

          this.deleteClientActive = true;
        },


        /**
        * Delete client
        */
        onConfirmDelete () {

          var formData = new FormData();
          
          if(this.currentDeleteId)
            formData.append("id", this.currentDeleteId);

          this.$http.delete(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT + "?id=" +  this.currentDeleteId, 
            {withCredentials: true,}
          )
          .then(response =>{
            if(response && response.data){
              this.searchClients();
            }
          })
          //Error 
          .catch(err => {
            alert("error : " + err.message);  
          })
        },

        /**
        * Delete client
        */
        onCancelDelete () {
          this.currentDeleteId = null;
        }
  },

  mounted: function(){
    checkLogged();
    this.searchClients();
  }
}
</script>

