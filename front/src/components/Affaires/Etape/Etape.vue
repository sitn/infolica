<style src="./etape.css" scoped></style>
<template src="./etape.html"></template>


<script>
import ClotureAffaire from "@/components/Affaires/ClotureAffaire/ClotureAffaire.vue";

import { handleException } from "@/services/exceptionsHandler";
import { getTypesAffaires, stringifyAutocomplete2, logAffaireEtape, checkPermission } from '@/services/helper'

const moment = require('moment')

export default {
  name: "Etape",
  components: {
    ClotureAffaire
  },
  props: {
    affaire: Object,
    chefs_equipe_list: Array,
    etapes_affaire_conf: Object,
    typesAffaires_conf: Object
  },
  data() {
    return {
      affaireEtapes: [],
      allowSaveNewStep: false,
      art35Radio: "",
      cloreAffaire: false,
      controleEtape : [],
      etapeAffaire: {
        prochaine: null,
        remarque: null,
        showDialog: false,
      },
      final_decision: false,
      isAdmin: false,
      numerosReserves: [],
      suiviAffaireTheorique: [],
      updateAffaireDate: {
        text: "",
        value: false,
        date_type: "",
        show: false,
      },
    };
  },

  methods: {
    /**
     * Search affaire etapes
     */
    async searchAffaireEtapes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPES_INDEX_ENDPOINT,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        this.affaireEtapes = stringifyAutocomplete2(response.data.filter(x => x.ordre !== null));
        // get suivi d'affaire théorique
        this.typesAffaires = getTypesAffaires().then(response => {
          if (response && response.data) {
            try {
              this.suiviAffaireTheorique = response.data.filter(x => x.id === this.affaire.type_id)[0].logique_processus;
            }
            catch {
              this.suiviAffaireTheorique = [];
            }

          }
        })
      }).catch(err => handleException(err, this));
    },

    /**
     * open New state dialog
     */
    async openNewStateDialog(){
      // set next step prediction
      this.etapeAffaire.prochaine = null;
      this.etapeAffaire.chef_equipe_id = this.affaire.technicien_id || null;
      this.etapeAffaire.remarque = null;
      
      if (this.suiviAffaireTheorique.includes(this.affaire.etape_id)) {
        this.etapeAffaire.prochaine = this.affaireEtapes.filter(x => x.id === this.suiviAffaireTheorique[this.suiviAffaireTheorique.indexOf(this.affaire.etape_id)+1])[0];
      }

      // if step "chez le client" next step is "operateur_travail"
      if (this.affaire.etape_id === this.etapes_affaire_conf.chez_client) {
        this.etapeAffaire.prochaine = this.affaireEtapes.filter(x => x.id === this.etapes_affaire_conf.travaux_chef_equipe)[0];
      }

      // Update affaire dates
      this.saveDatesDiv();

      // Controles-étape en cours
      await this.getControleEtape();

      this.etapeAffaire.showDialog = true;
    },

    /**
     * Enregistrer la nouvelle étape
     */
    async updateAffaireEtape() {
      if (!this.etapeAffaire.prochaine || !this.etapeAffaire.prochaine.id) {
        return
      }

      // if updateAffaireDate.value is true, update date affaire
      if (this.updateAffaireDate.value) {
        this.updateAffaire(this.updateAffaireDate.date_type);

        if (this.cloreAffaire) {
          //Clore affaire
          setTimeout(() => {
            // timout pour éviter une erreur indéterminée
            this.$refs.clotureAffaire.onConfirmCloture(false);
            this.cloreAffaire = false;
          }, 200);
        }
      }

      // fix value of this.etapeAffaire.chef_equipe_id to null if another step is selected
      this.etapeAffaire.chef_equipe_id = this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.travaux_chef_equipe? this.etapeAffaire.chef_equipe_id: null;

      logAffaireEtape(this.affaire.id, this.etapeAffaire.prochaine.id, this.etapeAffaire.remarque, this.etapeAffaire.chef_equipe_id)
      .then(() => {
        this.$root.$emit("ShowMessage", "L'étape a bien été mise à jour");
        this.etapeAffaire.showDialog = false;

        // art35: set type in specificite.
        if (this.affaire.etape_id === this.etapes_affaire_conf.travaux_chef_equipe && this.affaire.type_id === this.typesAffaires_conf.art35) {
          this.updateAffaierSpecificite_art35();
        }


        // event emitter
        this.$emit('setAffaire');
        this.$root.$emit('getAffaireSuivi');
      });

      this.updateAffaireDate = {
        text: "",
        value: false,
        date_type: ""
      };
    },

    /**
     * update affaire specificite art 35
     */
    async updateAffaierSpecificite_art35() {
      let formData = new FormData();
      formData.append('id_affaire', this.affaire.id);
      formData.append("information", this.art35Radio + ". " + this.affaire.information);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.art35Radio = "";
        this.$emit('setAffaire');
      })
      .catch(err => handleException(err, this));
    },


    /**
     * updateAffaire
     */
    async updateAffaire(attr) {
      let formData = new FormData();
      formData.append('id_affaire', this.affaire.id);
      formData.append(attr, moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.$emit('setAffaire');
      })
      .catch(err => handleException(err, this));
    },

    /**
     * Set numéros réservés
     */
    setNumerosReserves(data) {
      this.numerosReserves = data;
    },

    /**
     * On select next step
     */
    onSelectNextStep(etape) {
      if (etape.id === this.etapes_affaire_conf.fin_processus) {
        this.updateAffaireDate = {
          text: "Mettre à jour la date de validation de l'affaire",
          value: true,
          date_type: "date_validation"
        };

        // Si aucun numéro n'est réservé dans l'affaire, clôre l'affaire
        if ((this.etapeAffaire.prochaine && this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.fin_processus) &&
            (![this.typesAffaires_conf.mutation, this.typesAffaires_conf.modification, this.typesAffaires_conf.remaniement_parcellaire,
               this.typesAffaires_conf.modification_visa, this.typesAffaires_conf.modification_mutation].includes(this.affaire.type_id)) &&
            (this.numerosReserves.length === 0)) {
          this.updateAffaireDate.text = "Mettre à jour les dates de validation et de clôture de l'affaire";
          this.cloreAffaire = true;
        }
      }

      // Il est possible de passer l'affaire à une étape inférieure ou chez le client même si les contrôles ne sont pas tous OK
      if ( (this.affaire.etape_ordre > etape.ordre) || ([Number(process.env.VUE_APP_ETAPE_CHEZ_CLIENT_ID), Number(process.env.VUE_APP_ETAPE_DEVIS_ID)].includes(etape.id)) ) {
        this.allowSaveNewStep = true;
      } else {
        this.allowSaveNewStep = this.final_decision;
      }

      this.saveDatesDiv();
    },

    /**
     * set Save Dates div
     */
    saveDatesDiv() {
      this.updateAffaireDate.show = (
        [this.etapes_affaire_conf.envoi, this.etapes_affaire_conf.validation].includes(this.affaire.etape_id) && this.affaire.type_id !== this.typesAffaires_conf.pcop) ||
        (this.etapes_affaire_conf.envoi_pcop === this.affaire.etape_id && this.affaire.type_id === this.typesAffaires_conf.pcop) || 
        this.etapeAffaire.prochaine && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.fin_processus && this.affaire.type_id === this.typesAffaires_conf.cadastration;
      
      if (this.etapeAffaire.prochaine && this.etapeAffaire.prochaine.id) {
        this.setNewEtapeParameters();
      }
    },

    /**
     * set New Etape
     */
    setNewEtapeParameters() {
      this.updateAffaireDate = {
        text: "",
        value: false,
        date_type: "",
        show: false
      };

      if (
        (this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.fin_processus) &&
        ![this.typesAffaires_conf.ppe, this.typesAffaires_conf.modification_ppe, this.typesAffaires_conf.pcop].includes(this.affaire.type_id)
      ) {
        // update date_validation if next step is "fin de processus"
        if (
          (this.etapeAffaire.prochaine && this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.fin_processus) &&
          (![this.typesAffaires_conf.mutation, this.typesAffaires_conf.modification, this.typesAffaires_conf.remaniement_parcellaire,
          this.typesAffaires_conf.modification_visa, this.typesAffaires_conf.modification_mutation].includes(this.affaire.type_id)) && (this.numerosReserves.length === 0)
        ) {
          // also close affaire if none number is reserved
          this.updateAffaireDate = {
            text: "Mettre à jour les dates de validation et de clôture de l'affaire",
            value: true,
            date_type: "date_validation",
            show: true
          };
          this.cloreAffaire = true;
        } else {
          this.updateAffaireDate = {
            text: "Mettre à jour la date de validation de l'affaire",
            value: true,
            date_type: "date_validation",
            show: true
          };
          this.cloreAffaire = false;
        }
      } else if (
        // Mise à jour de la date d'envoi
        ((this.affaire.etape_id === this.etapes_affaire_conf.envoi && ![this.typesAffaires_conf.pcop, this.typesAffaires_conf.cadastration].includes(this.affaire.type_id)) ||
        (this.affaire.etape_id === this.etapes_affaire_conf.envoi_pcop && this.affaire.type_id === this.typesAffaires_conf.pcop) ||
        (this.affaire.etape_id === this.etapes_affaire_conf.envoi_cadastration && this.affaire.type_id === this.typesAffaires_conf.cadastration)) &&
        ([this.etapes_affaire_conf.validation, this.etapes_affaire_conf.signature_art35].includes(this.etapeAffaire.prochaine.id) ||
        [this.typesAffaires_conf.ppe, this.typesAffaires_conf.modification_ppe, this.typesAffaires_conf.pcop].includes(this.affaire.type_id))
      ) {
        this.updateAffaireDate = {
          text: "Mettre à jour la date d'envoi de l'affaire",
          value: true,
          date_type: "date_envoi",
          show: true
        };
        this.cloreAffaire = false;
      }
    },

    /**
     * Controle étape
     */
    async getControleEtape() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_CONTROLE_ETAPE_ENDPOINT + "?affaire_id=" + this.affaire.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data.detail;
          tmp.forEach(x => {
            if (x.result === true) {
              x.icon = "check_circle";
              x.icon_color = "green";
              x.icon_title = "Cette condition est vérifiée.";
            } else {
              if (x.force === 'NOGO') {
                x.icon = "cancel";
                x.icon_color = "red";
                x.icon_title = "Cette condition n'est pas vérifiée et bloque le passage pour la prochaine étape.";
              } else if (x.force === 'WARNING'){
                x.icon = "warning";
                x.icon_color = "orange";
                x.icon_title = "Cette condition n'est pas vérifiée mais ne bloque pas le passage pour la prochaine étape.";
              }
            }
          });
          this.controleEtape = tmp;

          this.final_decision = response.data.final_decision.result;
          this.allowSaveNewStep = response.data.final_decision.result;
        }
      }).catch(err => handleException(err, this));
    }

  },

  mounted: function() {
    this.searchAffaireEtapes();
    this.$root.$on( "setEtapeNouveauxNumeros", (data) => this.setNumerosReserves(data) );

    // operateur is admin?
    this.isAdmin = checkPermission(process.env.VUE_APP_FONCTION_ADMIN);
  }
};
</script>
