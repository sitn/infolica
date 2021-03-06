<style src="./suiviAffaire.css" scoped></style>
<template src="./suiviAffaire.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
import { stringifyAutocomplete } from '@/services/helper'

const moment = require('moment')

export default {
  name: "SuiviAffaire",
  data: () => {
    return {
        affaires: [],
        affaireTypes: [],
        affaireTypes_autocomplete: [],
        affaireEtapes_autocomplete: [],
        affaire: {
            id: null,
            nom: null,
            type: null,
            actuelle_etape_id: null,
            remarque: null
        },
        etape: {
            id: null,
            operateur_id: null,
            affaire: null,
            datetime: null,
            etape: null,
            remarque: null
        },
        dialogEtape: null,
        showNewAffaireDialog: false,
        showNewEtapeDialog: false,
        suiviAffaires: [],
    }
  },

  methods: {
    /**
     * get affaire types
     */
    async getAffaireTypes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TYPE_TELE_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.affaireTypes = response.data;
                this.affaireTypes_autocomplete = stringifyAutocomplete(response.data);
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * get Suivi Affaire
     */
    async getSuiviAffaire() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_SUIVI_AFFAIRE_TELE_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.suiviAffaires = response.data;
            }
        }).catch(err => handleException(err, this));
    },
    
    /**
     * get Affaires
     */
    async getAffaire() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TELE_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = response.data;
                tmp.forEach(x => {
                    x.dashboard = new Array(15);
                    x.dashboard[x.etape_id-1] = x.affaire_nom;
                });
                this.affaires = tmp;
            }
        }).catch(err => handleException(err, this));
    },
    
    /**
     * get Etapes
     */
    async getEtapes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_ETAPE_TELE_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.getSuiviAffaire();
                this.affaireEtapes_autocomplete = stringifyAutocomplete(response.data);
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Init form affaire
     */
    initFormAffaire() {
        this.showNewAffaireDialog = false;
        this.showNewEtapeDialog = false;
        this.affaire = {
            id: null,
            nom: null,
            type: null,
            actuelle_etape_id: null,
            remarque: null
        };
    },
    
    /**
     * Init form Etape
     */
    initFormEtape() {
        this.showNewEtapeDialog = false;
        this.etape = {
            id: null,
            operateur_id: null,
            affaire: null,
            datetime: null,
            etape: null,
            remarque: null
        };
    },

    /**
     * Get première étape de l'affaire selon le parcours d'affaire du type d'affaire
     */
    getPremiereEtapeAffaire() {
        if (this.affaire.type !== null && this.affaire.type.id) {
            this.affaire.actuelle_etape_id = this.affaireTypes.filter(x => x.id === this.affaire.type.id)[0].logique_etapes[0];
        }
    },

    /**
     * Post new affaire
     */
    async postNewAffaire() {
        let formData = new FormData();
        formData.append("nom", this.affaire.nom);
        formData.append("type_id", this.affaire.type.id);
        formData.append("actuelle_etape_id", this.affaire.actuelle_etape_id);
        formData.append("datetime_ouverture", moment(new Date()).format("YYYY-MM-DD hh:mm:ss"));
        formData.append("remarque", this.affaire.remarque);

        this.$http.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TELE_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.affaire.id = response.data;
                this.$root.$emit("ShowMessage", "L'affaire a bien été créée.");
                // this.initFormAffaire();
                this.showNewAffaireDialog = false;
                this.setNewState();
                this.postNewState();
                this.getAffaire();
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Set new state
     */
    setNewState(affaire_id=null, etape_id=null) {
        this.etape = {
            id: null,
            operateur_id: JSON.parse(localStorage.getItem("infolica_user")).id,
            affaire_id: affaire_id === null? this.affaire.id: affaire_id,
            datetime: moment(new Date()).format("YYYY-MM-DD hh:mm:ss"),
            etape: this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.actuelle_etape_id)[0],
            remarque: null
        };
        if (etape_id !== null) {
            this.etape.etape = {id: etape_id};
        }
    },

    /**
     * Post new state
     */
    async postNewState() {
        let formData = new FormData();
        formData.append("operateur_id", this.etape.operateur_id);
        formData.append("affaire_id", this.etape.affaire_id);
        formData.append("datetime", this.etape.datetime);
        formData.append("etape_id", this.etape.etape.id);
        formData.append("remarque", this.etape.remarque);

        this.$http.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_SUIVI_AFFAIRE_TELE_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.$root.$emit("ShowMessage", "L'étape a bien été enregistrée.");
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * open new etape dialog
     */
    openNewEtapeDialog(data) {
        this.affaire = this.affaires.filter(x => x.affaire_id === data.affaire_id)[0];
        this.affaire.prochaine_etape_id = this.affaire.affaire_type_logique_etapes[this.affaire.affaire_type_logique_etapes.indexOf(this.affaire.etape_id)+1];
        
        this.affaire.actuelle_etape = this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.etape_id)[0];
        this.affaire.prochaine_etape = this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.prochaine_etape_id)[0];
        
        this.showNewEtapeDialog = true;
    },
    
    /**
     * set prochaine etape_id
     */
    setProchaineEtapeId(data) {
        this.affaire.prochaine_etape_id = data.id;
    },

    /**
     * Update affaire with new actual_etape_id
     */
    async updateAffaire() {
        let formData = new FormData();
        formData.append("id", this.affaire.affaire_id);
        formData.append("actuelle_etape_id", this.affaire.prochaine_etape_id);
        if (this.affaire.prochaine_etape_id > 13) {
            formData.append("datetime_cloture", moment(new Date()).format("YYYY-MM-DD hh:mm:ss"))
        }

        this.$http.put(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TELE_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(() => {
            this.$root.$emit("ShowMessage", "La nouvelle étape a bien été saisie.");
            this.showNewEtapeDialog = false

            this.setNewState(this.affaire.affaire_id, this.affaire.prochaine_etape_id);
            this.postNewState();

            this.getAffaire();
        }).catch(err => handleException(err, this));
    },

    // /**
    //  * open infolica test
    //  */
    // openInfolicaTest() {
    //     this.$router.push({ name: "Affaires"});
    //     document.getElementById("header").style.display = "initial";
    // }


  },

  mounted: function() {
    let header = document.getElementById("header");
    if (header !== null) {
        header.style.display = "none";
    }
    this.getAffaireTypes();
    this.getAffaire();
    this.getEtapes();
    this.getSuiviAffaire();

  }
};
</script>

