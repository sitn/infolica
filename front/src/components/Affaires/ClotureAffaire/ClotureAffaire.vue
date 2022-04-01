<template src="./clotureAffaire.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import { getEtatsNumeros, stringifyAutocomplete, logAffaireEtape } from "@/services/helper.js";
import moment from "moment";

export default {
  name: "ClotureAffaire",
  props: {
    affaire: Object,
    typesAffaires_conf: Object
  },
  component: {},
  data: () => {
    return {
      showClotureDialog: false,
      affaire_numeros: [],
      numero_etats_liste: []
    };
  },
  methods: {
    /**
     * Open clotureDialog
     */
    openClotureDialog(){
      this.getNumerosAffaire();
      this.showClotureDialog = true;
    },

    /**
     * Charger les numéros dans l'affaire
     */
    async getNumerosAffaire() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" +
          this.affaire.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            let numeros_base_liste = this.getNumerosBaseList(response.data);
            let affaire_numeros_tmp = this.filterNumerosActiveInAffaire(response.data);
            this.affaire_numeros = this.setPredictedFutureState(affaire_numeros_tmp, numeros_base_liste);
          }
        })
        .catch(err => handleException(err, this));
    },

    /**
     * Récupérer les numéros de base pour les numéros DDP, PPE et PCOP
     */
    getNumerosBaseList(data) {
      let tmp = new Set(data.map(x => x.numero_base_id));
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
        supprime_id: Number(process.env.VUE_APP_NUMERO_SUPPRIME_ID),
        abandonne_id: Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
      };

      // Si le type d'affaire nécessite la suppression des biens-fonds de base (mutation ou modif de mutation)
      if (![
          this.typesAffaires_conf.mutation, 
          this.typesAffaires_conf.modification_mutation, 
          this.typesAffaires_conf.modification_visa, 
          this.typesAffaires_conf.modification_duplicata, 
          this.typesAffaires_conf.modification_retour_etat_juridique
        ].includes(this.affaire.type_id)) {
        data = data.filter(x => x.affaire_numero_type_id !== num_type.ancien_id);
      }

      data.forEach(element => {
        element.numero_etatFutur_id = element.numero_etat_id;

        // Cas des numéros projetés, non mat-diff, à passer de projet à validé
        if (element.affaire_numero_type_id === num_type.nouveau_id && 
            element.numero_etat_id === num_etat.projet_id) {
          
          // if retablissement etat juridique, reserved numbers must be abandouned
          if (this.affaire.type_id === this.typesAffaires_conf.modification_retour_etat_juridique) {
            element.numero_etatFutur_id = num_etat.abandonne_id;
          } else {
            element.numero_etatFutur_id = num_etat.vigueur_id;
          }
        } 
        // Cas des numéros référencés à supprimer, si le bf de base doit être supprimé
        else if (element.affaire_numero_type_id === num_type.ancien_id
                 && this.affaire.type_id !== this.typesAffaires_conf.modification_retour_etat_juridique) {
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
    onConfirmCloture(updateNumerosState=true) {
      this.showClotureDialog = false;

      if (updateNumerosState) {

        const _this = this;
        let promises = [];
  
        _this.affaire_numeros.forEach(num => {
          promises.push(_this.saveNewEtatNumero(num));
          promises.push(_this.saveNewEtatHistoryNumero(num));
        });
  
        Promise.all(promises)
        .then(response => {
          if (response) {
            this.AjoutDateClotureAffaire()
            .then(() => {
              this.$parent.setAffaire();
              this.$root.$emit("ShowMessage", "L'affaire " + this.affaire.id + " a été clôturées avec succès");
  
              //Log cloture affaire
              logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CLOTURE_ID))
              .then(() => this.$router.go(0));
            })
            .catch(err => handleException(err, this));
          }
        })
        .catch(err => {
          handleException(err, this);
        });

      } else {

        this.AjoutDateClotureAffaire().then(() => {
          this.$router.go(0);
          this.$root.$emit("setAffaire");
          this.$root.$emit("ShowMessage", "L'affaire " + this.affaire.id + " a été clôturées avec succès");

          //Log cloture affaire
          logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CLOTURE_ID));
        }).catch(err => handleException(err, this));

      }
      
    },

    /**
     * Ajout de la date de clôture de l'affaire
     */
    async AjoutDateClotureAffaire(){
      return new Promise((resolve, reject) => {
        var formData = new FormData();
        formData.append("id_affaire", this.affaire.id);
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