<style src="./clientsEdit.css" scoped></style>
<template src="./clientsEdit.html"></template>


<script>
import {checkLogged} from '@/services/helper'

import { validationMixin } from 'vuelidate'
  import {
    required,
    email,
    minLength
  } from 'vuelidate/lib/validators'

  const moment = require('moment')

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      types_clients_list: [],
      //Mode : new or edit
      mode: 'new',
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

      /**
       * Get validation class par fieldname
       */
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
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
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
        this.sending = true;
        var formData = this.initPostData();
        
        var url = process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT;

        if(this.mode === 'new'){
          this.$http.post(
            url, 
            formData,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            }
          )
          .then(response =>{
            this.handleSaveDataSuccess(response);
          })
          //Error 
          .catch(err => {
            this.sending = false
            alert("error : " + err.message);  
          });
        }
        else{
          var id = this.$route.params.id;
          formData.append("id", id);
          
          this.$http.put(
            url, 
            formData,
            {
              withCredentials: true,
              headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }
          )
          .then(response =>{
            this.handleSaveDataSuccess(response);
          })
          //Error 
          .catch(err => {
            this.sending = false
            alert("error : " + err.message);  
          });
        }
      },

      /**
      * Handle save data success
      */
      initPostData () {
        var formData = new FormData();
        formData.append("type_client", this.form.type_client);

        if(this.form.entreprise)
          formData.append("entreprise", this.form.entreprise);
        if(this.form.titre)
          formData.append("titre", this.form.titre);
        if(this.form.nom)
          formData.append("nom", this.form.nom);
        if(this.form.prenom)
          formData.append("prenom", this.form.prenom);
        if(this.form.represente_par)
          formData.append("represente_par", this.form.represente_par);
        if(this.form.adresse)
          formData.append("adresse", this.form.adresse);
        if(this.form.npa)
          formData.append("npa", this.form.npa);
        if(this.form.localite)
          formData.append("localite", this.form.localite);
        if(this.form.case_postale)
          formData.append("case_postale", this.form.case_postale);
        if(this.form.tel_fixe)
          formData.append("tel_fixe", this.form.tel_fixe);
        if(this.form.fax)
          formData.append("fax", this.form.fax);
        if(this.form.tel_portable)
          formData.append("tel_portable", this.form.tel_portable);
        if(this.form.mail)
          formData.append("mail", this.form.mail);
        if(this.form.entree)
          formData.append("entree", moment(new Date(new Date(this.form.entree))).format('YYYY-MM-DD'));
        if(this.form.no_sap)
          formData.append("no_sap", this.form.no_sap);
        if(this.form.no_bdp_bdee)
          formData.append("no_bdp_bdee", this.form.no_bdp_bdee);

        return formData;
      },

      /**
      * Handle save data success
      */
      handleSaveDataSuccess (response) {
        if(response && response.data){
          this.lastRecord = `${this.form.prenom} ${this.form.nom}`;
          this.dataSaved = true;
          this.sending = false;
          this.clearForm();
        }
      },

      /**
       * Validate form
       */
      validateForm () {
        this.$v.$touch()

        if (!this.$v.$invalid) {
          this.saveData()
        }
      },
      
      /**
       * Cancel edit
       */
      cancelEdit () {
        this.$router.push('/clients');
      },
      
      /**
       * Init edit data
       */
      initEditData (id) {
        
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT + '/' + id,
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
        )
        .then(response =>{
          if(response && response.data){
            this.form.type_client = response.data.type_client;
            this.form.entreprise = response.data.entreprise;
            this.form.titre = response.data.titre;
            this.form.nom = response.data.nom;
            this.form.prenom = response.data.prenom;
            this.form.represente_par = response.data.represente_par;
            this.form.adresse = response.data.adresse;
            this.form.npa = response.data.npa;
            this.form.localite = response.data.localite;
            this.form.case_postale = response.data.case_postale;
            this.form.tel_fixe = response.data.tel_fixe;
            this.form.fax = response.data.fax;
            this.form.tel_portable = response.data.tel_portable;
            this.form.mail = response.data.mail;
            this.form.entree = response.data.entree;
            this.form.no_sap = response.data.no_sap;
            this.form.no_bdp_bdee = response.data.no_bdp_bdee;
          }
        })
        //Error 
        .catch(err => {
          this.sending = false
          alert("error : " + err.message);  
        });
      }
    },

    mounted: function(){
      checkLogged();
      this.initTypesClientsList();

      //Mode (new or edit)      
      if(this.$router && this.$router.currentRoute && this.$router.currentRoute.path === '/clients/new')
        this.mode = 'new';
      else
        this.mode = 'edit';


      //If mode = edit, get the client
      if(this.mode === 'edit'){
        var id = this.$route.params.id;
        this.initEditData(id);
      }
    }
  }

</script>

