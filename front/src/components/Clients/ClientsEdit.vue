<style src="./clientsEdit.css" scoped></style>
<template src="./clientsEdit.html"></template>


<script>
import {checkLogged} from '@/services/helper'

import { validationMixin } from 'vuelidate'
  import {
    required,
    email,
    date,
    minLength
  } from 'vuelidate/lib/validators'

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      form: {
        type_client: null,
        entreprise: null,
        titre: null,
        nom: null,
        prenom: null,
        represente_par: null,
        adresse: null,
        npa: null,
        localite: null,
        case_postale: null,
        tel_fixe: null,
        fax: null,
        tel_portable: null,
        mail: null,
        entree: null,
        no_sap: null,
        no_bdp_bdee: null
      },

      userSaved: false,
      sending: false,
      lastUser: null
    }),
    validations: {
      form: {
        type_client: {
          required
        },
        nom: {          
          minLength: minLength(3)
        },
        prenom: {
          minLength: minLength(3)
        },
        entree: {
          required,
          date
        },
        email: {
          email
        }
      }
    },
    
    methods: {
      getValidationClass (fieldName) {
        const field = this.$v.form[fieldName]

        if (field) {
          return {
            'md-invalid': field.$invalid && field.$dirty
          }
        }
      },
      clearForm () {
        this.$v.$reset()
        this.form.type_client = null;
        this.form.entreprise = null;
        this.form.titre = null;
        this.form.nom = null;
        this.form.prenom = null;
        this.form.represente_par = null;
        this.form.adresse = null;
        this.form.npa = null;
        this.form.localite = null;
        this.form.case_postale = null;
        this.form.tel_fixe = null;
        this.form.fax = null;
        this.form.tel_portable = null;
        this.form.mail = null;
        this.form.entree = null;
        this.form.no_sap = null;
        this.form.no_bdp_bdee = null;
      },
      saveUser () {
        this.sending = true

        // Instead of this timeout, here you can call your API
        window.setTimeout(() => {
          this.lastUser = `${this.form.firstName} ${this.form.lastName}`
          this.userSaved = true
          this.sending = false
          this.clearForm()
        }, 1500)
      },
      validateUser () {
        this.$v.$touch()

        if (!this.$v.$invalid) {
          this.saveUser()
        }
      }
    },

    mounted: function(){
      checkLogged();
      
    }
  }

</script>

