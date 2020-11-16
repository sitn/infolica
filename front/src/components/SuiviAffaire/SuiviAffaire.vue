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
        affaireEtapes: [],
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
            remarque: null,
            mailadress: null,
        },
        dialogEtape: null,
        mailAdressList: [],
        showMailChefEquipe: false,
        showNewAffaireDialog: false,
        showNewEtapeDialog: false,
        suiviAffaires: [],
        suiviAffaires_bk: [],
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
                this.suiviAffaires_bk = response.data;
                this.suiviAffaires_bk.forEach(x => x.datetime = x.datetime.replace("T", ", "));
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
                    for (let i=0; i<17; i++) {
                        x["dashboard_" + i.toString()] = i === x.etape_id-1? x.affaire_nom: null;
                    }
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
                let tmp = response.data;
                tmp.forEach(x => {
                    if (x.mail !== null) {
                        x.mail = x.mail.replace(/\s/g, '').split(",");
                    }
                });
                this.affaireEtapes = tmp;
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
            remarque: null,
            mailadress: null
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
        formData.append("datetime_ouverture", moment(new Date()).format("YYYY-MM-DD HH:mm:ss"));
        if (this.affaire.remarque) {
            formData.append("remarque", this.affaire.remarque);
        }

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
     * Set new state right before save
     */
    setNewState(affaire_id=null, etape_id=null) {
        this.etape.id = null;
        this.etape.operateur_id = JSON.parse(localStorage.getItem("infolica_user")).id;
        this.etape.affaire_id = affaire_id === null? this.affaire.id: affaire_id;
        this.etape.datetime = moment(new Date()).format("YYYY-MM-DD HH:mm:ss");
        this.etape.etape = this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.actuelle_etape_id)[0];
        if (etape_id !== null) {
            this.etape.etape = this.affaireEtapes_autocomplete.filter(x => x.id === etape_id)[0];
        }
    },

    /**
     * Post new state
     */
    async postNewState() {
        if (this.etape.etape.id === 2) {
            this.etape.remarque = this.etape.remarque? this.etape.remarque + " - ": "";
            this.etape.remarque += "Attribué à : " + this.etape.mailadress;
        }

        let formData = new FormData();
        formData.append("operateur_id", this.etape.operateur_id);
        formData.append("affaire_id", this.etape.affaire_id);
        formData.append("datetime", this.etape.datetime);
        formData.append("etape_id", this.etape.etape.id);
        if (this.etape.remarque) {
            formData.append("remarque", this.etape.remarque);
        }

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
        this.initFormEtape();
        this.affaire = this.affaires.filter(x => x.affaire_id === data.affaire_id)[0];
        this.affaire.prochaine_etape_id = this.affaire.affaire_type_logique_etapes[this.affaire.affaire_type_logique_etapes.indexOf(this.affaire.etape_id)+1];
        this.setProchaineEtapeId({id: this.affaire.prochaine_etape_id});

        this.affaire.actuelle_etape = this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.etape_id)[0];
        this.affaire.prochaine_etape = this.affaireEtapes_autocomplete.filter(x => x.id === this.affaire.prochaine_etape_id)[0];
        
        this.suiviAffaires = this.suiviAffaires_bk.filter(x => x.affaire_id === data.affaire_id);

        this.showNewEtapeDialog = true;
    },
    
    /**
     * set prochaine etape_id
     */
    setProchaineEtapeId(data) {
        this.affaire.prochaine_etape_id = data.id;

        if (data.id === 2) {
            this.mailAdressList = this.affaireEtapes[1].mail;
            this.etape.mailadress = this.mailAdressList[0];
            this.showMailChefEquipe = true;
        } else {
            this.showMailChefEquipe = false;
            this.etape.mailadress = null;
            this.mailAdressList = [];
        }
    },

    /**
     * Update affaire with new actual_etape_id
     */
    async updateAffaire() {
        let formData = new FormData();
        formData.append("id", this.affaire.affaire_id);
        formData.append("actuelle_etape_id", this.affaire.prochaine_etape_id);
        if (this.affaire.prochaine_etape_id == 14 || this.affaire.prochaine_etape_id == 15 || this.affaire.prochaine_etape_id == 17) {
            formData.append("datetime_cloture", moment(new Date()).format("YYYY-MM-DD HH:mm:ss"))
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
            this.sendMail(this.affaire.affaire_nom, this.etape.etape.id);

            this.getAffaire();
            this.getSuiviAffaire();
        }).catch(err => handleException(err, this));
    },

    /**
     * Send e-mail @ new etape
     */
    async sendMail(affaire_nom, etape_id) {
        let formData = new FormData();
        formData.append("affaire_nom", affaire_nom);
        formData.append("etape_id", etape_id);
        if (etape_id === 2) {
            formData.append("email_adresse", this.etape.mailadress)
        }

        this.$http.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPE_AFFAIRE_MAIL_TELE_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(()=> {})
        .catch(err => handleException(err, this));
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

    setInterval(() => {
            this.getAffaire();
            this.getSuiviAffaire();
        },
        60000); // Recharge le tableau toutes les minutes

  }
};
</script>

