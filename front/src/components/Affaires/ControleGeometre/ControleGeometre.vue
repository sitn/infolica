<style src="./controleGeometre.css" scoped></style>
<template src="./controleGeometre.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {logAffaireEtape} from '@/services/helper';

const moment = require('moment')

export default {
  name: "controleGeometre",
  props: {
    affaire: Object,
    typesAffaires_conf: Object,
    permission: Object
  },
  data: () => ({
    checkAll: {
      ctrl_jur: false,
      sign: false
    },
    controleGeometre: {},
    showNewControleGeometreBtn: false,
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-ControleMutation
     */
    async searchControleGeometre() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_CONTROLE_GEOMETRE_ENDPOINT +
          this.affaire.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.controleGeometre = response.data;

            if (this.controleGeometre.date) {
              this.controleGeometre.date = moment(this.controleGeometre.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
          } 
        })
        .catch(err =>  handleException(err, this));
    },


    /**
     * update controle
     */
    updateControleGeometre() {
      let formData = new FormData();
      formData.append("id", this.controleGeometre.id);
      for (let elem in this.controleGeometre) {
        if (elem === 'date') {
          formData.append(elem, moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
        } else if (elem === 'operateur_id') {
          formData.append(elem, JSON.parse(localStorage.getItem("infolica_user")).id);
        } else {
          formData.append(elem, this.controleGeometre[elem]);
        }
      }
      
      this.$http
        .put(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_CONTROLE_GEOMETRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response) {
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été mis à jour avec succès")
            
            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CONTROLE_GEOMETRE_ID), "Edition du formulaire");
            
            this.searchControleGeometre();
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Create new controle geometre
     */
    async createControleGeometre() {
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_CONTROLE_GEOMETRE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.$root.$emit("ShowMessage", "Le formulaire de contrôle a bien été créé");
          this.searchControleGeometre();
        }
      })
      .catch(err => handleException(err, this));
    },

  },

  mounted: function() {
    this.searchControleGeometre();
  }
};
</script>



