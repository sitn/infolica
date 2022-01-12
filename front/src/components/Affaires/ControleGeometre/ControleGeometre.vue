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

    /**
     * Select all
     */
    selectAll(type_ctrl) {
      let items = [];

      if (type_ctrl === "ctrl_jur" && [this.typesAffaires_conf.mutation,
                                       this.typesAffaires_conf.modification,
                                       this.typesAffaires_conf.modification_duplicata,
                                       this.typesAffaires_conf.modification_mutation,
                                       this.typesAffaires_conf.modification_visa].includes(this.affaire.type_id)) {
        items = [48, 49, 12, 2, 50, 14, 3, 51, 10, 1, 52, 5, 6, 53, 9, 8, 54, 4, 55, 56];
        for (const item of items) {
          this.controleGeometre["check_" + String(item)] = this.checkAll.ctrl_jur;
        }
      }

      if (type_ctrl === "sign") {
        if (![this.typesAffaires_conf.cadastration, this.typesAffaires_conf.ppe, this.typesAffaires_conf.modification_ppe].includes(this.affaire.type_id)) {
          if (this.affaire.type_id === this.typesAffaires_conf.revision_abornement) {
            items = [57, 26, 27, 23, 25, 44, 45, 15, 18, 19, 17, 58, 59, 21, 22];
          } else if (this.affaire.type_id === this.typesAffaires_conf.retablissement_pfp3) {
            items = [57, 26, 27, 23, 25, 46, 47, 15, 18, 19, 17, 58, 59, 21, 22];
          } else if (this.affaire.type_id === this.typesAffaires_conf.modification_duplicata) {
            items = [57, 26, 27, 23, 25, 15, 18, 19, 17, 58, 59, 40, 21, 22, 39];
          } else if ([this.typesAffaires_conf.modification_visa, this.typesAffaires_conf.modification_mutation, this.typesAffaires_conf.modification].includes(this.affaire.type_id)) {
            items = [57, 26, 27, 23, 25, 15, 18, 19, 17, 58, 59, 42, 21, 22, 41];
          } else if (this.affaire.type_id === this.typesAffaires_conf.art35) {
            items = [57, 26, 27, 23, 25, 15, 18, 19, 17, 58, 59, 20, 21, 22];
          } else if (this.affaire.type_id === this.typesAffaires_conf.servitude) {
            items = [57, 26, 27, 23, 25, 15, 18, 19, 17, 58, 59, 21, 22, 43];
          } else  {
            items = [57, 26, 27, 23, 25, 15, 18, 19, 17, 58, 59, 21, 22];
          }
        } else if(this.affaire.type_id === this.typesAffaires_conf.cadastration) {
          items = [60, 29, 31, 28, 32, 61, 57, 23, 25, 1, 37, 18, 19, 20, 34, 17, 35, 36, 38, 21, 22];
        } else {
          items = [48, 49, 62, 57, 26, 27, 23, 25, 61, 62, 63, 50, 64, 65, 66];
        }

        for (const item of items) {
          this.controleGeometre["check_" + String(item)] = this.checkAll.sign;
        }
      }

    }

  },

  mounted: function() {
    this.searchControleGeometre();
  }
};
</script>



