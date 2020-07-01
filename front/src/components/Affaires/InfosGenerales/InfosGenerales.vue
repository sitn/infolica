<style src="./infosGenerales.css" scoped></style>
<template src="./infosGenerales.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission, stringifyAutocomplete} from '@/services/helper';

const moment = require("moment");

export default {
  name: "InfosGénérales",
  props: {
    affaire: {type: Object}
    },
  components: {},
  data() {
    return {
      affaire_backup: {},
      infoGenReadonly: true,
      affaireReadonly: true,
      operateursListe: [],
      typesAffairesListe: [],
      affaires_source: [],
      affaires_destination: [],
      form: {
        technicien: null,
        responsable: null,
        typeAffaire: null
      }
    };
  },

  methods: {
    /**
     * Ouvre la page de consultation/édition de client
     */
    openClientEditor(field_name) {
      let routedata = this.$router.resolve({name: 'ClientsEdit', params: {id: this.affaire[field_name]}});
      window.open(routedata.href, "_blank");
    },
    /*
     * CREATE COPY OF AFFAIRE
     */
    copyAffaire() {
      Object.assign(this.affaire_backup, this.affaire);
    },

    /**
     * Annuler l'édition du formulaire
     */
    onCancelEdit() {
      Object.assign(this.affaire, this.affaire_backup);
      this.infoGenReadonly = true;
    },

    /**
     * Enregistrer les modifications
     */
    async onConfirmEdit() {
      var formData = new FormData();
      formData.append("id_affaire", this.affaire.id);
      formData.append("technicien_id", this.form.technicien.id);
      formData.append("type_id", this.form.typeAffaire.id);
      if (this.form.responsable !== null) formData.append("responsable_id", this.form.responsable.id);
      if (this.affaire.nom !== "-") formData.append("nom", this.affaire.nom || null);
      if (this.affaire.information !== "-")
        formData.append("information", this.affaire.information || null);
      if (this.affaire.vref !== "-") formData.append("vref", this.affaire.vref || null);
      if (this.affaire.date_validation)
        formData.append(
          "date_validation", this.affaire.date_validation?
          moment(this.affaire.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      else
        formData.append("date_validation", null);
      if (this.affaire.date_envoi)
        formData.append(
          "date_envoi", this.affaire.date_envoi? 
          moment(this.affaire.date_envoi, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      else
        formData.append("date_cloture", null);
      if (this.affaire.date_cloture)
        formData.append(
          "date_cloture", this.affaire.date_cloture? 
          moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      else
        formData.append("date_cloture", null);
        
      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => { //response =>{
          this.infoGenReadonly = true;
          this.$parent.setAffaire();
          this.copyAffaire();
        })
        //Error 
        .catch(err => {
          handleException(err, this); 
        });
    },

    /**
     * Initialiser la liste des opérateurs
     */
    async initOperateursListe() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.operateursListe = response.data
          .map(x => ({
            id: x.id,
            nom: [x.prenom, x.nom].filter(Boolean).join(" ")
          }))
          .map(x => ({
            id: x.id,
            nom: x.nom,
            toLowerCase: () => x.nom.toLowerCase(),
            toString: () => x.nom.toString()
          }));
        }
      }).catch(err => handleException(err, this))
    },

    /**
     * Open Edit mode
     */
    openEditMode() {
      this.form.technicien = this.operateursListe
      .filter(x => x.id === this.affaire.technicien_id)[0];
      
      if (this.form.responsable !== null){
        this.form.responsable = this.operateursListe
        .filter(x => x.id === this.affaire.responsable_id)[0];
      }

      this.form.typeAffaire = this.typesAffairesListe
      .filter(x => x.id === this.affaire.type_id)[0];

      this.infoGenReadonly = false;
    },

    /**
     * get cadastres
     */
    async initTypesAffairesListe() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) 
          this.typesAffairesListe = stringifyAutocomplete(response.data);
      }).catch(err => handleException(err, this))
    },

    /**
     * Récupère l'affaire mère
     */
    async searchAffaireSource() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_MODIFICATION_AFFAIRE_BY_AFFAIRE_MERE_ENDPOINT + 
        this.$route.params.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          var tmp = [];
          response.data.forEach(x => {
            tmp.push(x.affaire_id_mere)
          });
          this.affaires_source = tmp;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Récupère l'affaire fille
     */
    async searchAffaireDestination() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_MODIFICATION_AFFAIRE_BY_AFFAIRE_FILLE_ENDPOINT + 
        this.$route.params.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          var tmp = [];
          response.data.forEach(x => {
            tmp.push(x.affaire_id_fille)
          });
          this.affaires_destination = tmp;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * On click provenance
     */
    onClickProvenance(item) {
      alert(item)
    },

  },

  mounted: function() {
    this.copyAffaire();
    this.initOperateursListe();
    this.initTypesAffairesListe();
    this.searchAffaireSource();
    this.searchAffaireDestination();
    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



