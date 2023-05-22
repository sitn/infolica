<style src="./clientSearch.css" scoped></style>
<template src="./clientSearch.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";
import { stringifyAutocomplete2 } from "@/services/helper";

export default {
  
  name: "ClientSearch",
  
  props: {
    old_clients: {
      type: Boolean,
      default: true
    },
    title: {
      type: String,
      default: 'Recherche de client'
    }
  },
  
  emits: [
    'update:client_id'
  ],
  
  data: () => {
    return {
      liste_clients: [],
      searchTerm: null
    };
  },

  methods: {
    /**
     * searchClient
     */
    async searchClient(searchTerm) {
      let conditions = {
        'searchTerm': searchTerm,
        'old_clients': this.old_clients
      };

      this.getClientsByTerm(conditions)
      .then(response => {
        if (response && response.data) {
          this.liste_clients = stringifyAutocomplete2(response.data);
        }
      }).catch(err => handleException(err, this));
    },


    async getClientsByTerm(conditions) {
      let params = [];
      if (conditions && typeof conditions === 'object') {
          for (const property in conditions) {
              params.push(property + "=" + conditions[property]);
          }
      }
      
      if (params.length > 0) {
          params = "?" + params.join("&");
      } else {
          params = "";
      } 

      return new Promise((resolve, reject) => {
          this.$http.get(
              process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_ENDPOINT + params,
              {
                  withCredentials: true,
                  headers: {"accept": "application/json"}
              }
          )
          .then(response => resolve(response))
          .catch(err => reject(err));
      });
    }
  },

  computed: {
    value: {
      get() {
        return this.client_id;
      },
      set(value) {
        if (value && value.id) {
          this.$emit('update:client_id', value.id);
        }
        if (value === null || value === '') {
          this.$emit('update:client_id', value);
        }
      }
    }
  },

  mounted: function() {
    this.$root.$on('resetSearchClientTerm', () => { document.querySelector('#clientSearchAutocomplete > button').click(); });
  }
};

</script>
