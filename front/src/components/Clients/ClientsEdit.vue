<style src="./clientsEdit.css" scoped></style>
<template src="./clientsEdit.html"></template>


<script>
import {checkLogged} from '@/services/helper'
import moment from 'moment'

import { validationMixin } from 'vuelidate'
  import {
    required,
    email,
    minLength
  } from 'vuelidate/lib/validators'

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      types_clients_list: [],
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
        entree: new Date(),
        no_sap: null,
        no_bdp_bdee: null
      },

      dataSaved: false,
      sending: false,
      lastRecord: null
    }),

    // Validations
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
          required
        },
        mail: {
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

      /**
       * Clear the form
       */
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

      /*
      * Init types clients list
      */
      initTypesClientsList() {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_TYPES_CLIENTS_ENDPOINT,
        )
        .then(response =>{
          if (response && response.data) {
            this.types_clients_list = response.data;
          }
        })
        //Error 
        .catch(err => {
          alert("error : " + err.message);  
        });
      },
      
      /**
       * Save data
       */
      saveData () {
        this.sending = true

        var formData = new FormData();
        formData.append("type_client", this.form.type_client.id);
        formData.append("entreprise", this.form.entreprise);
        formData.append("titre", this.form.titre);
        formData.append("nom", this.form.nom);
        formData.append("prenom", this.form.prenom);
        formData.append("represente_par", this.form.represente_par);
        formData.append("adresse", this.form.adresse);
        formData.append("npa", this.form.npa);
        formData.append("localite", this.form.localite);
        formData.append("case_postale", this.form.case_postale);
        formData.append("tel_fixe", this.form.tel_fixe);
        formData.append("fax", this.form.fax);
        formData.append("tel_portable", this.form.tel_portable);
        formData.append("mail", this.form.mail);
        formData.append("entree", moment(new Date(this.form.entree)).format('yyyy-mm-dd'));
        formData.append("no_sap", this.form.no_sap);
        formData.append("no_bdp_bdee", this.form.no_bdp_bdee);
        
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT, 
          formData
        )
        .then(response =>{
          if(response && response.data){
            var a = "1";
            alert(a);
          }
        })
        //Error 
        .catch(err => {
          alert("error : " + err.message);  
        });


        window.setTimeout(() => {
          this.lastRecord = `${this.form.prenom} ${this.form.nom}`
          this.dataSaved = true
          this.sending = false
          this.clearForm()
        }, 1500)
      },

      /**
       * Validate form
       */
      validateForm () {
        this.$v.$touch()

        if (!this.$v.$invalid) {
          this.saveData()
        }
      }
    },

    mounted: function(){
      checkLogged();

      this.initTypesClientsList();
      
    }
  }

</script>

