<style src="./clientSearch.css" scoped></style>
<template src="./clientSearch.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";
import { stringifyAutocomplete2 } from "@/services/helper";

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {

  name: "ClientSearch",

  mixins: [validationMixin],

  props: {
    initial_client_id: {
      type: Number,
      default: null
    },
    client_id: {
      type: Number,
      default: null
    },
    label: {
      type: String,
      default: 'Client'
    },
    old_clients: {
      type: Boolean,
      default: true
    },
    permission_createClient: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Recherche de client'
    },
    validation_error_msg: {
      type: String,
      default: 'Le client est obligatoire'
    },
    filter_type: {
      type: Array,
      default: () => []
    },
  },

  emits: [
    'update:client_id'
  ],

  data: () => {
    return {
      client: null,
      liste_clients: [],
    };
  },

  validations: {
    client: { required }
  },

  methods: {
    /**
     * searchClient
     */
    async searchClient(searchTerm) {
      let conditions = {
        'searchTerm': searchTerm,
        'old_clients': this.old_clients,
        'filter_type': JSON.stringify(this.filter_type),
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
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENT_AGGREGATED_ENDPOINT + params,
          {
            withCredentials: true,
            headers: { "accept": "application/json" }
          }
        )
          .then(response => resolve(response))
          .catch(err => reject(err));
      });
    },


    async getClientById(client_id) {
      if (client_id === null) {
        this.client = '';
        return;
      }

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENT_AGGREGATED_BY_ID_ENDPOINT + '/' + client_id,
        {
          withCredentials: true,
          headers: { "Accept": "application/json" }
        }
      ).then(response => {
        if (response && response.data) {

          this.client = stringifyAutocomplete2(response.data, ["nom"], ", ", "nom");
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * openCreateClient
     */
    openCreateClient() {
      let routedata = this.$router.resolve({ name: "ClientsNew" });
      window.open(routedata.href, "_blank");
    },

    /**
     * Validations
     */
    getValidationClass(fieldName) {
      const field = this.$v[fieldName];

      if (field) {
        return {
          'md-invalid': field.$invalid && field.$dirty
        }
      }
    },

    validator() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        return true;
      }
      return false
    }

  },

  mounted: function () {
    if (this.initial_client_id !== null) {
      this.getClientById(this.initial_client_id);
    }


    this.$root.$on('resetSearchClientTerm', () => { document.querySelector('#clientSearchAutocomplete > button').click(); });
  },

  watch: {
    client_id: function () {
      if (this.client_id !== null) {
        this.getClientById(this.client_id);
      } else {
        this.client = '';
      }
    },

    client: function () {
      if (this.client && this.client.id) {
        this.$emit('update:client_id', this.client.id);
      } else {
        this.$emit('update:client_id', null);
      }
    }
  }
};

</script>
