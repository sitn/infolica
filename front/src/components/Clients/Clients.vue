<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler';
import {
  checkPermission,
  getClientTypes,
  // getClients,
  // filterList
} from '@/services/helper';

import moment from "moment";

export default {
  name: 'Clients',
  props: {},
  data: () => ({
    clients: [],
    // clients_list: [],
    client_types: [],
    currentDeleteId: null,
    deleteClientActive: false,
    deleteMessage: '',
    editClientClientAllowed: false,
    isExpendedSearchPanel: false,
    search: {
      adresse: null,
      client_id: null,
      entreprise: null,
      localite: null,
      mail: null,
      nom: null,
      npa: null,
      prenom: null,
      client_type_id: null,
    },
    search_clients_list: [],
    searchTerm: "",
    searchOldClientMode: false,
  }),
  methods: {

    onExpand() {
      this.isExpendedSearchPanel = !this.isExpendedSearchPanel;

      if (this.isExpendedSearchPanel) {
        this.searchTerm = "";
        this.searchClients();
      } else {
        this.clearForm();
        this.searchClientsByTerm();
      }
    },

    /**
     * Search clients
    */
    async searchClients() {
      this.searchTerm = null;

      let formData = new FormData();

      if (this.search.nom) {
        formData.append("nom", this.search.nom);
      }
      if (this.search.prenom) {
        formData.append("prenom", this.search.prenom);
      }
      if (this.search.entreprise) {
        formData.append("entreprise", this.search.entreprise);
      }
      if (this.search.client_id && this.search.client_id.id) {
        formData.append("id", this.search.client_id.id);
      }
      if (this.search.npa) {
        formData.append("npa", this.search.npa);
      }
      if (this.search.adresse) {
        formData.append("adresse", this.search.adresse);
      }
      if (this.search.localite) {
        formData.append("localite", this.search.localite);
      }
      if (this.search.mail) {
        formData.append("mail", this.search.mail);
      }
      if (this.search.client_type_id) {
        formData.append("type_client", this.search.client_type_id);
      }
      formData.append("old_clients", this.searchOldClientMode);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { "Accept": "application/json" }
        }
      ).then(response => {
          if (response && response.data) {
            this.clients = this.setDateformat(response.data);
          }
        }).catch(err => {
          handleException(err, this);
        })
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.search.nom = null;
      this.search.prenom = null;
      this.search.entreprise = null;
      this.search.adresse = null;
      this.search.localite = null;
      this.search.mail = null;
      this.search.client_type_id = null;
    },


    /**
    * Update client
    */
    updateClient(client) {
      if (client.sortie === null) {
        client.sortie = (new Date()).toLocaleDateString('fr-CH');
      } else {
        client.sortie = null;
      }

      let formData = new FormData();
      formData.append("id", client.id);
      formData.append("sortie", client.sortie);


      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { "Accept": "application/json" }
        }
      )
        .then(response => {
          if (response && response.data) {
            this.updateSearchClients();
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },



    /*
     * Init clients list (for search input in form)
     */
    // async initClientsSearchList() {
    //   let params = '?old_clients=' + this.searchOldClientMode + '&searchTerm=' + this.searchTerm;
    //   this.$http.get(
    //     process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_BY_TERM_ENDPOINT + params,
    //     {
    //       withCredentials: true,
    //       headers: { "accept": "application/json" }
    //     }
    //   ).then(response => {
    //     if (response && response.data) {
    //       this.clients_list = response.data.map(x => ({
    //         id: x.id,
    //         nom: x.adresse_,
    //         toLowerCase: () => x.adresse_.toLowerCase(),
    //         toString: () => x.adresse_
    //       }));
    //     }
    //   })
    //     //Error
    //     .catch(err => {
    //       handleException(err, this);
    //     });
    // },

    // searchClientsForFormInput(value) {
    //   this.search_clients_list = filterList(this.clients_list, value, 3);
    // },


    /**
     * search Client by term
     */
    async searchClientsByTerm() {
      // this.clearForm();

      let params = '?old_clients=' + this.searchOldClientMode + '&searchTerm=' + this.searchTerm;

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_BY_TERM_ENDPOINT + params,
        {
          withCredentials: true,
          headers: { "accept": "application/json" }
        }
      ).then(response => {
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

    updateSearchClients() {
      if (this.isExpendedSearchPanel) {
        this.searchClients();
      } else {
        this.searchClientsByTerm();
      }
    },

    async getClientTypes_() {
      getClientTypes()
        .then(response => {
          if (response && response.data) {
            this.client_types = response.data.map(x => ({
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


  },

  mounted: function () {
    this.editClientClientAllowed = checkPermission(process.env.VUE_APP_CLIENT_EDITION);
    this.searchClientsByTerm();
    // this.initClientsSearchList();
    this.getClientTypes_();
  }
}
</script>
