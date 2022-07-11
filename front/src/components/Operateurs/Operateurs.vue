<style src="./operateurs.css" scoped></style>
<template src="./operateurs.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission, stringifyAutocomplete2} from '@/services/helper';
const moment = require('moment');

export default {
  name: 'Operateurs',
  props: {},
  data: () => ({
    currentDeleteId: null,
      deleteOperateurActive: false,
      deleteMessage: '',
      editionOperateursAllowed: false,
      form: {
        id: null,
        nom: null,
        prenom: null,
        initiales: null,
        login: null,
        responsable: false,
        chef_equipe: false,
        mail: null,
        service: {},
        entree: null,
        sortie: null,
        role_id: null,
        service_id: null,
        ldap_domain: null
      },
      operateurs: [],
      search: {
        nom: null,
        prenom: null,
        login: null
      },
      services: [],
      roles: [],
      divEditUser: {
        title: "",
        show: false,
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
          headers: {"Accept": "application/json"}
        }
      )
      .then(response =>{
        if(response && response.data){
          let tmp = response.data;

          tmp.forEach(x => {
            x.entree = x.entree === null? null: moment(x.entree, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            x.sortie = x.sortie === null? null: moment(x.sortie, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
          });

          this.operateurs = tmp;
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
    callEditOperateur (op) {
      for (const elem in this.form) {
        this.form[elem] = op[elem];
      }

      this.divEditUser.title = "Modifier un·e opérateur·rice existant·e";
      this.divEditUser.show = true;
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

      this.$http.delete(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT + "?id=" +  this.currentDeleteId,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      )
      .then(response =>{
        if(response && response.data){
          this.searchOperateurs();
          this.$root.$emit('ShowMessage', "L'opérateur a bien été supprimé.");
        }
      })
      //Error
      .catch(err => {
        handleException(err, this);
      })
    },

    /**
    * Cancel Delete operateur
    */
    onCancelDelete () {
      this.currentDeleteId = null;
    },

    /**
     * Create user
     */
    createUser() {
      this.clearFormEditClient();
      this.divEditUser.title = "Enregistrer un·e nouvel·le opérateur·rice";
      this.divEditUser.show = true;
    },

    /**
     * On cancel edition
     */
    onCancelNewOperateur() {
      this.divEditUser.show = false;
      this.clearFormEditClient();
    },

    /**
     * Clear form edit operateur
     */
    clearFormEditClient() {
      this.form = {
        id: null,
        nom: null,
        prenom: null,
        initiales: null,
        login: null,
        responsable: false,
        chef_equipe: false,
        mail: null,
        service_id: null,
        role_id: null,
        ldap_domain: null,
        entree: null,
        sortie: null,
      };
    },

    /**
     * On save edition
     */
    onSaveNewOperateur() {
      let formData = new FormData();

      let errors = [];
      for (const elem in this.form) {
        if ( (this.form[elem] !== null && this.form[elem] !== "") || (elem !== "service_id" || elem !== "sortie")) {
          if (elem === 'entree') {
            formData.append(elem, moment(this.form[elem], process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
          } else if (elem === 'sortie') {
            formData.append(elem, this.form[elem]? moment(this.form[elem], process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
          } else {
            formData.append(elem, this.form[elem]);
          }
        } else {
          if (elem !== "id") {
            errors.push(elem);
          }
        }
      }

      // afficher les erreurs
      if (errors.length > 0) {
        alert("Certains éléments n'ont pas été renseignés. Merci d'apporter les modifications nécessaire(s) aux champ(s) suivant(s):  " + errors.join(", "));
        return;
      }

      formData.append("entree", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

      let request = null;
      let success_msg = "";
      if (this.form.id) {
        // modifier un opérateur existant
        request = this.putOperateur(formData);
        success_msg = "L'opérateur a bien été modifié.";
      } else {
        // Créer un nouvel opérateur
        request = this.postOperateur(formData);
        success_msg = "L'opérateur a bien été créé.";
      }

      // apply callbacks
      request.then(response => {
        if (response && response.data) {
          this.onCancelNewOperateur();
          this.searchOperateurs();
          this.$root.$emit('ShowMessage', success_msg);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * post operateur
     */
    async postOperateur(formData) {
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * put operateur
     */
    async putOperateur(formData) {
      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * get services
     */
    async getService() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICES_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {

          this.services = stringifyAutocomplete2(response.data, ['abreviation']);
        }
      })
      .catch(err => handleException(err, this));
    },


    /**
     * get services
     */
    async getRoles() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_USER_ROLE_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {

          this.roles = stringifyAutocomplete2(response.data, ['nom']);

        }
      })
      .catch(err => handleException(err, this));
    },

    textUpperCase() {
      this.form.ldap_domain = this.form.ldap_domain.toUpperCase();
    }


  },

  mounted: function(){
    this.getService();
    this.getRoles();
    this.searchOperateurs();
    this.editionOperateursAllowed = checkPermission(process.env.VUE_APP_FONCTION_ADMIN);
  }
}
</script>

