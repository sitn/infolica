<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission} from '@/services/helper';

export default {
  name: 'Clients',
  props: {},
  data: () => ({
      clients: [],
      deleteClientActive: false,
      editClientClientAllowed: false,
      deleteMessage: '',
      currentDeleteId: null,
      clients_list: [],
      search_clients_list: [],
      search: {
        client_id: null,
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

          if(this.search.client_id)
            formData.append("id", this.search.client_id.id);

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
              headers: {"Accept": "application/json"}
            }
          )
          .then(response =>{
            if(response && response.data){
              this.clients = response.data;
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
          this.search.entreprise = null;
          this.search.adresse = null;
          this.search.localite = null;
          this.search.mail = null;
        },


        /**
         * Call edit client
         */
        callEditClient (id) { 
         this.$router.push({ name: "ClientsEdit", params: { id: id } }) ;
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
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
          )
          .then(response =>{
            if(response && response.data){
              this.searchClients();
            }
          })
          //Error 
          .catch(err => {
            handleException(err, this);
          })
        },

        /**
        * Cancel delete client
        */
        onCancelDelete () {
          this.currentDeleteId = null;
        },

    /*
     * Init clients list (for search input in form)
     */
    async initClientsSearchList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            var tmp = response.data;
            tmp.forEach(x => {
              x.nom_ = [
                x.entreprise,
                [x.nom, x.prenom].filter(Boolean).join(" "),
                x.adresse,
                [x.npa, x.localite].filter(Boolean).join(" ")
              ]
                .filter(Boolean)
                .join(", ");
            });

            this.clients_list = tmp.map(x => ({
              id: x.id,
              nom: x.nom_,
              toLowerCase: () => x.nom_.toLowerCase(),
              toString: () => x.nom_
            }));
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
      },

      /**
     * Search Client for form input after 3 letters
     */
    searchClientsForFormInput(value) {
      let tmp = [];
      if (value !== null) {
        if (value.length >= 3) {
          tmp = this.clients_list.filter(x =>
            x.nom.toLowerCase().includes(value.toLowerCase())
          );
        }
      }
      this.search_clients_list = tmp;
    }
  },

  mounted: function(){    
    this.editClientClientAllowed = checkPermission(process.env.VUE_APP_CLIENT_EDITION);
    this.initClientsSearchList();
    this.searchClients();
  }
}
</script>

