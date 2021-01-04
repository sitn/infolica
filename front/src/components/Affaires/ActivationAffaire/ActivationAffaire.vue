<template src="./activationAffaire.html"></template>

// PROCESSUS
//  - SUPPRIMER NUMEROS RELATIONS

<script>
import { handleException } from "@/services/exceptionsHandler";
import { getEtatsNumeros, stringifyAutocomplete, logAffaireEtape } from "@/services/helper.js";
import moment from "moment";

export default {
  name: "ActivationAffaire",
  props: {
    affaire: Object
  },
  component: {},
  data: () => {
    return {
      affaire_numeros: [],
      numero_etats_liste: [],
      showActivationDialog: false,
      showBalanceAlertDialog: false,
    };
  },
  methods: {
    openActivationDialog(){
      this.getNumerosAffaire();

      this.showActivationDialog = true;
    },


    /**
     * Réactivation de l'affaire
     */
    async activateAffaire() {
      let promises = [];
      promises.push(this.updateAffaire());
      promises.push(this.resetNumeroEtat());

      Promise.all(promises).then(() => {
        this.$root.$emit("showMessage", "L'affaire " + this.affaire.id + " a bien été réactivée");
        //Log edition facture
        logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_ACTIVATION_ID));
        this.showActivationDialog = false;
        this.$router.go(0);

        this.getAffaireNumerosRelation()
        .then(response => {
          if (response && response.data && response.data.length > 0) {
            this.showBalanceAlertDialog = true;
          }
        }).catch(err => handleException(err, this));

      }).catch(err => handleException(err, this));
    },


    /**
     * Supprimer mention ABABDON et date clôture de l'affaire
     */
    async updateAffaire() {
      let formData = new FormData();
      formData.append('id_affaire', this.affaire.id);
      formData.append('date_cloture', null);
      formData.append('abandon', false);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * Charger les numéros dans l'affaire
     */
    async getNumerosAffaire() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" +
          this.affaire.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.affaire_numeros = response.data;
          }
        })
        .catch(err => handleException(err, this));
    },

    /**
     * Reset numeros affaires
     */
    async resetNumeroEtat() {
      let promises = [];

      return new Promise((resolve, reject) => {

        if (this.affaire_numeros.length > 0) {
          this.affaire_numeros.forEach(x => {
            if (x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID)) {
              // Ancien état
            if (x.numero_etat_id === Number(process.env.VUE_APP_NUMERO_SUPPRIME_ID)) {
              promises.push(this.updateNumeroEtat(x.numero_id, Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID)));
              promises.push(this.updateNumeroEtatHisto(x.numero_id, Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID)));
            }
          } else {
            // Nouvel etat
            if (x.numero_etat_id === Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)) {
              promises.push(this.updateNumeroEtat(x.numero_id, Number(process.env.VUE_APP_NUMERO_PROJET_ID)));
              promises.push(this.updateNumeroEtatHisto(x.numero_id, Number(process.env.VUE_APP_NUMERO_PROJET_ID)));
            }
          }
        })
      }

      Promise.all(promises)
      .then(response => resolve(response))
      .catch(err => reject(err));
      });
    },

    /**
     * updateNumeroEtat
     */
    async updateNumeroEtat(numero_id, etat_id) {
      let formData = new FormData();
      formData.append("id", numero_id);
      formData.append("etat_id", etat_id);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * Update numero etat histo
     */
    async updateNumeroEtatHisto(numero_id, etat_id) {
      let formData = new FormData();
      formData.append("numero_id", numero_id);
      formData.append("numero_etat_id", etat_id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
        
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ETAT_HISTO_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * Get affaire numeros relation
     */
    async getAffaireNumerosRelation() {
      return new Promise((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_RELATIONS_BY_AFFAIREID_ENDPOINT + this.affaire.id,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * Delete numeros relation in db
     */
    async deleteRelation(rel) {
      return new Promise((resolve, reject) => {
        this.$http.delete(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT + "?numero_relation_id=" +  rel.relation_id,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      })
    },


















    /**
     * Open clotureDialog
     */
    openClotureDialog(){
      this.getNumerosAffaire();
      this.showActivationDialog = true;
    },



    /**
     * Récupérer les numéros de base pour les numéros DDP, PPE et PCOP
     */
    getNumerosBaseList(data) {
      var tmp = new Set(data.map(x => x.numero_base_id));
      tmp.delete(null);
      return Array.from(tmp);
    },

    /**
     * Filtrer les numéros actifs dans l'affaire
     */
    filterNumerosActiveInAffaire(numeros) {
      return numeros.filter(x => x.affaire_destination_id === null);
    },

    /**
     * Créer la prédiction de l'état du numéro
     */
    setPredictedFutureState(data, base) {
      
      let num_type = {
        ancien_id: Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID),
        nouveau_id: Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID)
      };
      
      let num_etat = {
        projet_id: Number(process.env.VUE_APP_NUMERO_PROJET_ID),
        vigueur_id: Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID),
        supprime_id: Number(process.env.VUE_APP_NUMERO_SUPPRIME_ID)
      };

      data.forEach(element => {
        element.numero_etatFutur_id = element.numero_etat_id;

        // Cas des numéros projetés, non mat-diff, à passer de projet à validé
        if (element.affaire_numero_type_id === num_type.nouveau_id && 
            element.numero_etat_id === num_etat.projet_id) {
          element.numero_etatFutur_id = num_etat.vigueur_id;
        } 
        // Cas des numéros référencés à supprimer
        else if (element.affaire_numero_type_id === num_type.ancien_id) {
          if (~base.includes(element.numero_id)) {
            element.numero_etatFutur_id = num_etat.supprime_id;
          }
        }
      });
      return data;
    },

    /**
     * Récupérer les états des numéros
     */
    async getNumeroEtats() {
      getEtatsNumeros()
      .then(response => {
        if (response && response.data) {
          this.numero_etats_liste = stringifyAutocomplete(response.data);
        }
      })
      .catch(err => handleException(err, this));
    },

    /**
     * update Affaire_Numeros when new etat selected
     */
    updateAffaireNumero(num_id, etat_id) {
      this.affaire_numeros.map(x => {
        if (x.numero_id == num_id) {
          x.numero_etatFutur_id = etat_id;
        } 
      })
    },


    /**
     * Confirmer la clôture d'affaire
     */
    onConfirmCloture() {
      this.showActivationDialog = false;
      
      const _this = this;
      var promises = [];

      _this.affaire_numeros.forEach(num => {
        promises.push(_this.saveNewEtatNumero(num));
        promises.push(_this.saveNewEtatHistoryNumero(num));
      });

      Promise.all(promises)
      .then(response => {
        if (response) {
          this.AjoutDateClotureAffaire()
          .then(() => {
            this.$router.go(0);
            this.$parent.setAffaire();
            this.$root.$emit("ShowMessage", "L'affaire " + this.$route.params.id + " a été clôturées avec succès");

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CLOTURE_ID));
          })
          .catch(err => handleException(err, this));
        }
      })
      .catch(err => {
        handleException(err, this);
      });
    },

    /**
     * Ajout de la date de clôture de l'affaire
     */
    async AjoutDateClotureAffaire(){
      return new Promise((resolve, reject) => {
        var formData = new FormData();
        formData.append("id_affaire", this.$route.params.id);
        formData.append("date_cloture",  moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

        this.$http
          .put(
            process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRES_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
          ).then(response => {
            if (response) {
              resolve(response);
            }
          }).catch(err => reject(err));
        })
    },


    /**
     * Enregistrer le nouvel état des numéros
     */
    async saveNewEtatNumero(num) {
      var formData = new FormData();
      formData.append("id", num.numero_id);
      formData.append("etat_id", num.numero_etatFutur_id);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        )
        .then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * Enregistrer l'historique du changement d'état du numéro
     */
    async saveNewEtatHistoryNumero(num) {
      var formData = new FormData();
      formData.append("numero_id", num.numero_id);
      formData.append("numero_etat_id", num.numero_etatFutur_id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_ETAT_HISTO_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        )
        .then(response => resolve(response))
        .catch(err => reject(err));
      })
    },


  },
  mounted: function() {
    this.getNumeroEtats();
  }
};
</script>