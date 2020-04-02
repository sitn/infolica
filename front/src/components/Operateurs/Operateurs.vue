<style src="./operateurs.css" scoped></style>
<template src="./operateurs.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'

export default {
  name: 'Operateurs',
  props: {},
  data: () => ({
      operateurs: [],
      deleteOperateurActive: false,
      deleteMessage: '',
      currentDeleteId: null,
      search: {
        nom: null,
        prenom: null,
        login: null
      }
  }),
  methods: {
        /**
         * Search operateurs
        */
        async searchOperateurs () {
          var formData = new FormData();
          if(this.search.nom)
            formData.append("nom", this.search.nom);

          if(this.search.prenom)
            formData.append("prenom", this.search.prenom);

          if(this.search.login)
            formData.append("login", this.search.login);

          this.$http.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_OPERATEURS_ENDPOINT, 
            formData,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            }
          )
          .then(response =>{
            if(response && response.data){
              this.operateurs = response.data;
            }
          })
          //Error 
          .catch(err => {
            handleException(err, this);  
          })
        },

        /**
         * Clear the form
         */
        clearForm () {
          this.search.nom = null;
          this.search.prenom = null;
          this.search.login = null;
        },


        /**
         * Call edit operateur
         */
        callEditOperateur (id) {
         this.$router.push('/operateurs/edit/' + id) ; 
        },
        
        /**
         * Call delete operateur
         */
        callDeleteOperateur (id, nom, prenom) {
          this.currentDeleteId = id;

          if(prenom && nom)
            this.deleteMessage = prenom + ' ' + nom;
          else if(nom)
            this.deleteMessage = nom;
          else
            this.deleteMessage = "-";

          this.deleteMessage = "Confirmer la suppression de l'operateur '<strong>" + this.deleteMessage + "<strong>' ?";

          this.deleteOperateurActive = true;
        },

        /**
        * Delete operateur
        */
        onConfirmDelete () {

          /*var formData = new FormData();
          
          if(this.currentDeleteId)
            formData.append("id", this.currentDeleteId);*/

          this.$http.delete(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT + "?id=" +  this.currentDeleteId, 
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            }
          )
          .then(response =>{
            if(response && response.data){
              this.searchOperateurs();
            }
          })
          //Error 
          .catch(err => {
            handleException(err, this);  
          })
        },

        /**
        * Delete operateur
        */
        onCancelDelete () {
          this.currentDeleteId = null;
        }
  },

  mounted: function(){
    //checkLogged();
    this.searchOperateurs();
  }
}
</script>

