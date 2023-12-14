<style src="./operatorSelect.css" scoped></style>
<template src="./operatorSelect.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {

  name: "OperatorSelect",

  mixins: [validationMixin],

  props: {
    operateur_id: {
      type: Number,
      default: -1
    },
    label: {
      type: String,
      default: 'Opérateur·rice'
    },
    inactive_operateurs_permitted: {
      type: Boolean,
      default: true
    },
    title: {
      type: String,
      default: 'Sélectionner un opérateur'
    },
    validation_error_msg: {
      type: String,
      default: 'L\'opérateur est obligatoire'
    },
    select_all_permitted: {
      type: Boolean,
      default: false
    },
  },

  emits: [
    'update:operateur_id',
    'selected:operateur_id'
  ],
  
  data: () => {
    return {
      liste_operateurs: [],
    };
  },

  validations: {
      operateur_id: { required }
  },

  methods: {
    /**
     * searchValues
     */
    async searchValues() {
      let conditions = {
        'inactive_operateurs': this.inactive_operateurs_permitted
      };
      this.getValues(conditions)
      .then(response => {
        if (response && response.data) {
          this.liste_operateurs = response.data;
        }
      }).catch(err => handleException(err, this));
    },


    async getValues(conditions) {
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
              process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEUR_AGGREGATED_ENDPOINT + params,
              {
                  withCredentials: true,
                  headers: {"accept": "application/json"}
              }
          )
          .then(response => resolve(response))
          .catch(err => reject(err));
      });
    },

    /**
     * Validations
     */
    getValidationClass (fieldName) {
      const field = this.$v[fieldName];

      if (field) {
        return {
          'md-invalid': field.$invalid && field.$dirty
        }
      }
    },

    validator () {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        return true;
      }
      return false
    }

  },
  
  created: function() {
    this.searchValues();
  },

};

</script>
