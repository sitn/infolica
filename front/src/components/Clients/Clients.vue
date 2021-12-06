<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission,
        getClients,
        filterList,
        adjustColumnWidths,
        getClientsByTerm } from '@/services/helper';

import moment from "moment";

export default {
  name: 'Clients',
  props: {},
  data: () => ({
      clients: [],
      clients_list: [],
      currentDeleteId: null,
      deleteClientActive: false,
      deleteMessage: '',
      editClientClientAllowed: false,
      search: {
        adresse: null,
        client_id: null,
        entreprise: null,
        localite: null,
        mail: null,
        nom: null,
        npa: null,
        prenom: null
      },
      search_clients_list: [],
      searchTerm: "",
      searchOldClientMode: false,
  }),
  methods: {
        /**
         * Search clients
        */
        async searchClients () {
          this.searchTerm = null;

          let formData = new FormData();

          if(this.search.nom) {
            formData.append("nom", this.search.nom);
          }
          if(this.search.prenom) {
            formData.append("prenom", this.search.prenom);
          }
          if(this.search.entreprise) {
            formData.append("entreprise", this.search.entreprise);
          }
          if(this.search.client_id && this.search.client_id.id) {
            formData.append("id", this.search.client_id.id);
          }
          if(this.search.npa) {
            formData.append("npa", this.search.npa);
          }
          if(this.search.adresse) {
            formData.append("adresse", this.search.adresse);
          }
          if(this.search.localite) {
            formData.append("localite", this.search.localite);
          }
          if(this.search.mail) {
            formData.append("mail", this.search.mail);
          }

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
              this.clients = this.setDateformat(response.data);
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
      getClients()
      .then(response => {
        if (response && response.data) {
          this.clients_list = response.data.map(x => ({
            id: x.id,
            nom: x.adresse_,
            toLowerCase: () => x.adresse_.toLowerCase(),
            toString: () => x.adresse_
          }));
        }
      })
      //Error
      .catch(err => {
        handleException(err, this);
      });
    },

    searchClientsForFormInput(value) {
      this.search_clients_list = filterList(this.clients_list, value, 3);
    },


    /**
     * search Client by term
     */
    async searchClientsByTerm() {
      this.clearForm();

      let conditions = {
        "searchTerm": this.searchTerm? this.searchTerm: "",
        "old_clients": this.searchOldClientMode,
      };

      getClientsByTerm(conditions)
      .then(response => {
        if (response && response.data) {
          this.clients = this.setDateformat(response.data);
        }
      }).catch(err => handleException(err));
    },

    /**
     * set dateformat
     */
    setDateformat(list) {
      list.forEach(x => {
        if (x.sortie !== null) {
          x.sortie = moment(x.sortie, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
          x.sortie_sort = new Date(moment(x.sortie, process.env.VUE_APP_DATEFORMAT_WS)).getTime();
        } else {
          x.sortie_sort = -1;
        }
      });
      return list;
    },

  },

  mounted: function(){    
    this.editClientClientAllowed = checkPermission(process.env.VUE_APP_CLIENT_EDITION);
    this.initClientsSearchList();
    this.searchClients();
    adjustColumnWidths();
  }
}
</script>

