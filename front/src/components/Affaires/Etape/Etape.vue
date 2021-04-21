<style src="./etape.css" scoped></style>
<template src="./etape.html"></template>


<script>
import ClotureAffaire from "@/components/Affaires/ClotureAffaire/ClotureAffaire.vue";

import { handleException } from "@/services/exceptionsHandler";
import { getTypesAffaires, stringifyAutocomplete, logAffaireEtape } from '@/services/helper'

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
      cloreAffaire: false,
      etapeAffaire: {
        prochaine: null,
        remarque: null,
        showDialog: false,
      },
      numerosReserves: [],
      suiviAffaireTheorique: [],
      updateAffaireDate: {
        text: "",
        value: false,
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
        this.affaireEtapes = stringifyAutocomplete(response.data.filter(x => x.ordre !== null));
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
    openNewStateDialog(){
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
      if ((this.affaire.etape_id === this.etapes_affaire_conf.envoi && this.affaire.type_id !== this.typesAffaires_conf.pcop) || (this.affaire.etape_id === this.etapes_affaire_conf.envoi_pcop && this.affaire.type_id === this.typesAffaires_conf.pcop)) {
        this.updateAffaireDate = {
          text: "Mettre à jour la date d'envoi de l'affaire",
          value: true
        };
      } else if (this.affaire.etape_id === this.etapes_affaire_conf.validation) {
        this.updateAffaireDate = {
          text: "Mettre à jour la date de validation de l'affaire",
          value: true
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

      this.etapeAffaire.showDialog = true;
    },

    /**
     * Enregistrer la nouvelle étape
     */
    async updateAffaireEtape() {
      // if updateAffaireDate.value is true, update date affaire
      if (this.updateAffaireDate.value) {
        if (this.affaire.etape_id === this.etapes_affaire_conf.envoi || this.affaire.etape_id === this.etapes_affaire_conf.envoi_pcop) {
          this.updateAffaire('date_envoi');
        
        } else if (this.affaire.etape_id === this.etapes_affaire_conf.validation) {
          this.updateAffaire('date_validation');
          
          if (this.cloreAffaire) {
            //Clore affaire
            this.$refs.clotureAffaire.onConfirmCloture(false);
            this.cloreAffaire = false;
          
          }
        }
      }
      

      // fix value of this.etapeAffaire.chef_equipe_id to null if another step is selected
      this.etapeAffaire.chef_equipe_id = this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.travaux_chef_equipe? this.etapeAffaire.chef_equipe_id: null;

      logAffaireEtape(this.affaire.id, this.etapeAffaire.prochaine.id, this.etapeAffaire.remarque, this.etapeAffaire.chef_equipe_id)
      .then(() => {
        this.$root.$emit("ShowMessage", "L'étape a bien été mise à jour");
        this.etapeAffaire.showDialog = false;

        // event emitter
        this.$emit('setAffaire');
        this.$root.$emit('getAffaireSuivi');
      });

      this.updateAffaireDate = {
        text: "",
        value: false
      };
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
    }


  },

  mounted: function() {
    this.searchAffaireEtapes();
    this.$root.$on( "setEtapeNouveauxNumeros", (data) => this.setNumerosReserves(data) );
  }
};
</script>
