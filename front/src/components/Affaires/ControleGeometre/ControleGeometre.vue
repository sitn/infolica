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

            if (this.controleGeometre.ctrl_juridique_date) {
              this.controleGeometre.ctrl_juridique_date = moment(this.controleGeometre.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
            if (this.controleGeometre.signature_date) {
              this.controleGeometre.signature_date = moment(this.controleGeometre.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
          } 
        })
        .catch(err =>  handleException(err, this));
    },


    /**
     * update controle
     */
    updateControleGeometre() {
      var formData = new FormData();
      formData.append("id", this.controleGeometre.id);
      formData.append("affaire_id", this.controleGeometre.affaire_id);
      formData.append("remarque", this.controleGeometre.remarque || null);
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      formData.append("check_1", this.controleGeometre.check_1);
      formData.append("check_2", this.controleGeometre.check_2);
      formData.append("check_3", this.controleGeometre.check_3);
      formData.append("check_4", this.controleGeometre.check_4);
      formData.append("check_5", this.controleGeometre.check_5);
      formData.append("check_6", this.controleGeometre.check_6);
      formData.append("check_7", this.controleGeometre.check_7);
      formData.append("check_8", this.controleGeometre.check_8);
      formData.append("check_9", this.controleGeometre.check_9);
      formData.append("check_10", this.controleGeometre.check_10);
      formData.append("check_11", this.controleGeometre.check_11);
      formData.append("check_12", this.controleGeometre.check_12);
      formData.append("check_13", this.controleGeometre.check_13);
      formData.append("check_14", this.controleGeometre.check_14);
      formData.append("check_15", this.controleGeometre.check_15);
      formData.append("check_16", this.controleGeometre.check_16);
      formData.append("check_17", this.controleGeometre.check_17);
      formData.append("check_18", this.controleGeometre.check_18);
      formData.append("check_19", this.controleGeometre.check_19);
      formData.append("check_20", this.controleGeometre.check_20);
      formData.append("check_21", this.controleGeometre.check_21);
      formData.append("check_22", this.controleGeometre.check_22);
      formData.append("check_23", this.controleGeometre.check_23);
      formData.append("check_24", this.controleGeometre.check_24);
      formData.append("check_25", this.controleGeometre.check_25);
      formData.append("check_26", this.controleGeometre.check_26);
      formData.append("check_27", this.controleGeometre.check_27);
      formData.append("check_28", this.controleGeometre.check_28);
      formData.append("check_29", this.controleGeometre.check_29);
      formData.append("check_30", this.controleGeometre.check_30);
      formData.append("check_31", this.controleGeometre.check_31);
      formData.append("check_32", this.controleGeometre.check_32);
      formData.append("check_33", this.controleGeometre.check_33);
      formData.append("check_34", this.controleGeometre.check_34);
      formData.append("check_35", this.controleGeometre.check_35);
      formData.append("check_36", this.controleGeometre.check_36);
      formData.append("check_37", this.controleGeometre.check_37);
      formData.append("check_38", this.controleGeometre.check_38);
      formData.append("check_39", this.controleGeometre.check_39);
      formData.append("check_40", this.controleGeometre.check_40);
      formData.append("check_41", this.controleGeometre.check_41);
      formData.append("check_42", this.controleGeometre.check_42);
      formData.append("check_43", this.controleGeometre.check_43);
      formData.append("check_44", this.controleGeometre.check_44);
      formData.append("check_45", this.controleGeometre.check_45);
      formData.append("check_46", this.controleGeometre.check_46);
      formData.append("check_47", this.controleGeometre.check_47);
      formData.append("check_48", this.controleGeometre.check_48);
      formData.append("check_49", this.controleGeometre.check_49);
      formData.append("check_50", this.controleGeometre.check_50);
      formData.append("check_51", this.controleGeometre.check_51);
      formData.append("check_52", this.controleGeometre.check_52);
      formData.append("check_53", this.controleGeometre.check_53);
      formData.append("check_54", this.controleGeometre.check_54);
      formData.append("check_55", this.controleGeometre.check_55);
      formData.append("check_56", this.controleGeometre.check_56);
      formData.append("check_57", this.controleGeometre.check_57);
      formData.append("check_58", this.controleGeometre.check_58);
      formData.append("check_59", this.controleGeometre.check_59);
      formData.append("check_60", this.controleGeometre.check_60);
      formData.append("check_61", this.controleGeometre.check_61);
      formData.append("check_62", this.controleGeometre.check_62);
      formData.append("check_63", this.controleGeometre.check_63);
      formData.append("check_64", this.controleGeometre.check_64);
      formData.append("check_65", this.controleGeometre.check_65);
      formData.append("check_66", this.controleGeometre.check_66);

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



