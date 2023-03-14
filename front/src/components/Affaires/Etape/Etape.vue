<style src="./etape.css" ></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./etape.html"></template>


<script>
import ClotureAffaire from "@/components/Affaires/ClotureAffaire/ClotureAffaire.vue";
import DateRangePicker from "@/components/Utils/DateRangePicker/DateRangePicker.vue";
import NewStepSetter from "@/components/Utils/NewStepSetter/NewStepSetter.vue";

import { handleException } from "@/services/exceptionsHandler";
import { logAffaireEtape, checkPermission } from '@/services/helper';


const moment = require('moment');

export default {
  name: "Etape",
  components: {
    ClotureAffaire,
    DateRangePicker,
    NewStepSetter
  },
  props: {
    affaire: Object,
    chefs_equipe_list: Array,
    etapes_affaire_conf: Object,
    typesAffaires_conf: Object
  },
  data: () => ({
    affaireEtapes: [],
    allowSaveNewStep: {
      ctrl_etape: false,
      logique_processus: false,
    },    
    art35Radio: "",
    cloreAffaire: false,
    controleEtape : [],
    dateperiod_start: null,
    etapeAffaire: {
      nb_jours_etape: 0,
      prochaine_id: null,
      remarque: null,
      showDialog: false,
    },
    final_decision: false,
    isAdmin: false,
    numerosReserves: [],
    periodClientStatus: false,
    updateAffaireDate: {
      text: "",
      value: false,
      date_type: "",
      show: false,
    },
    joursHorsSGRF: {
      from: null,
      to: null,
      enabled: false,
      show: false
    }
  }),

  methods: {
    /**
     * open New state dialog
     */
    async openNewStateDialog(){
      // set next step prediction
      this.etapeAffaire.prochaine_id = null;
      this.etapeAffaire.chef_equipe_id = this.affaire.technicien_id || null;
      this.etapeAffaire.remarque = null;

      let now_datetime = (new Date()).getTime();
      let etape_datetime = (new Date(moment(this.affaire.etape_datetime, process.env.VUE_APP_DATEFORMAT_CLIENT))).getTime();
      
      this.etapeAffaire.nb_jours_etape = Math.floor((now_datetime - etape_datetime)/3600000/24) + 1;
      

      // if step "chez le client" next step is "operateur_travail"
      if (this.affaire.etape_id === this.etapes_affaire_conf.chez_client) {
        this.etapeAffaire.prochaine_id = this.etapes_affaire_conf.travaux_chef_equipe;
      } 
      
      const etapes_jours_clients = [
        this.etapes_affaire_conf.coordination,
        this.etapes_affaire_conf.controle_technique,
        this.etapes_affaire_conf.travaux_chef_equipe,
        this.etapes_affaire_conf.servitudes,
        this.etapes_affaire_conf.controle_juridique
      ];

      const types_affaires_jours_clients = [
        this.typesAffaires_conf.mutation,
        this.typesAffaires_conf.cadastration,
        this.typesAffaires_conf.pcop,
        this.typesAffaires_conf.mpd,
        this.typesAffaires_conf.art35,
        this.typesAffaires_conf.revision_abornement,
        this.typesAffaires_conf.remaniement_parcellaire,
        this.typesAffaires_conf.servitude,
        this.typesAffaires_conf.retablissement_pfp3,
        this.typesAffaires_conf.modification_visa,
        this.typesAffaires_conf.modification_duplicata,
        this.typesAffaires_conf.modification_mutation
      ];

      this.joursHorsSGRF.from = null;
      this.joursHorsSGRF.to = null;
      if (etapes_jours_clients.includes(this.affaire.etape_id) && types_affaires_jours_clients.includes(this.affaire.type_id)) {
        this.joursHorsSGRF.enabled = true;
      } else {
        this.joursHorsSGRF.enabled = false;
      }

      // Update affaire dates
      this.saveDatesDiv();

      // Controles-étape en cours
      await this.getControleEtape();

      // update parameters based on new step prediction
      this.setNewEtapeParameters();

      this.etapeAffaire.showDialog = true;
    },

    /**
     * Enregistrer la nouvelle étape
     */
    async updateAffaireEtape() {
      // get date_from and date_to from DateRangePicker
      if (this.joursHorsSGRF.enabled && this.joursHorsSGRF.show && this.$refs.DateRangePicker.date_from && this.$refs.DateRangePicker.date_to) {
        this.joursHorsSGRF.date_from = this.$refs.DateRangePicker.date_from;
        this.joursHorsSGRF.date_to = this.$refs.DateRangePicker.date_to;
      } else {
        this.joursHorsSGRF.date_from = null;
        this.joursHorsSGRF.date_to = null;
      }

      if (!this.etapeAffaire.prochaine_id) {
        alert("Il faut renseigner le champ 'prochaine étape'.")
        return
      }
      if (this.joursHorsSGRF.enabled && this.joursHorsSGRF.show && !this.joursHorsSGRF.date_from && !this.joursHorsSGRF.date_to) {
        alert("Il faut renseigner la période durant laquelle l'affaire était chez le client.")
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
      this.etapeAffaire.chef_equipe_id = this.etapeAffaire.prochaine_id === this.etapes_affaire_conf.travaux_chef_equipe? this.etapeAffaire.chef_equipe_id: null;
      
      logAffaireEtape(this.affaire.id, this.etapeAffaire.prochaine_id, this.etapeAffaire.remarque, this.etapeAffaire.chef_equipe_id, this.joursHorsSGRF.date_from, this.joursHorsSGRF.date_to)
      .then(() => {
        this.$root.$emit("ShowMessage", "L'étape a bien été mise à jour");
        this.etapeAffaire.showDialog = false;

        // art35: set type in specificite.
        if (this.affaire.etape_id === this.etapes_affaire_conf.travaux_chef_equipe && this.affaire.type_id === this.typesAffaires_conf.art35) {
          this.updateAffaireSpecificite_art35();
        }


        // event emitter
        this.$router.push({ name: "Cockpit" });
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
    async updateAffaireSpecificite_art35() {
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
     * set Save Dates div
     */
    saveDatesDiv() {
      this.updateAffaireDate.show = (
        [this.etapes_affaire_conf.envoi, this.etapes_affaire_conf.validation].includes(this.affaire.etape_id) && this.affaire.type_id !== this.typesAffaires_conf.pcop) ||
        (this.etapes_affaire_conf.envoi_pcop === this.affaire.etape_id && this.affaire.type_id === this.typesAffaires_conf.pcop) || 
        this.etapeAffaire.prochaine_id === this.etapes_affaire_conf.fin_processus && this.affaire.type_id === this.typesAffaires_conf.cadastration;
      
      if (this.etapeAffaire.prochaine_id) {
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
        (this.etapeAffaire.prochaine_id === this.etapes_affaire_conf.fin_processus) &&
        ![this.typesAffaires_conf.ppe, this.typesAffaires_conf.modification_ppe, this.typesAffaires_conf.pcop].includes(this.affaire.type_id)
      ) {
        // update date_validation or date_cloture if next step is "fin de processus"
        if (
          (this.etapeAffaire.prochaine_id === this.etapes_affaire_conf.fin_processus) &&
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
        } else if (this.affaire.type_id === this.typesAffaires_conf.modification_visa) {
          this.updateAffaireDate = {
            text: "Mettre à jour la date d'envoi de l'affaire",
            value: true,
            date_type: "date_envoi",
            show: true
          };
          this.cloreAffaire = false;
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
        ([this.etapes_affaire_conf.validation, this.etapes_affaire_conf.signature_art35].includes(this.etapeAffaire.prochaine_id) ||
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
              if (x.force !== "INFO") {
                x.icon = "check_circle";
                x.icon_color = "green";
                x.icon_title = "Cette condition est vérifiée.";
              } else {
                x.icon = "info";
                x.icon_color = "blue";
                x.icon_title = "Information non bloquante pour le passage à la prochaine étape.";
              }
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
          this.allowSaveNewStep.ctrl_etape = response.data.final_decision.result;
        }
      }).catch(err => handleException(err, this));
    },

    /** get selected value for new step */
    setNewStepId(value) {
      this.etapeAffaire.prochaine_id = value;
      this.setNewEtapeParameters();
    },

    /**get next step authorization (autorize next step if it is ) */
    getNextStepAuthorization(value) {
      this.allowSaveNewStep.logique_processus = value;
    }

  },

  mounted: function() {
    this.$root.$on( "setEtapeNouveauxNumeros", (data) => this.setNumerosReserves(data) );

    // operateur is admin?
    this.isAdmin = checkPermission(process.env.VUE_APP_FONCTION_ADMIN);

    this.dateperiod_start = new Date(moment(this.affaire.etape_datetime, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
  }
};
</script>
