<style src="./controleGeometre.css" scoped></style>
<template src="./controleGeometre.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission, logAffaireEtape} from '@/services/helper';

const moment = require('moment')

export default {
  name: "controleGeometre",
  props: {
    affaire: Object,
    typesAffaires_conf: Object
  },
  data: () => ({
    affaireReadonly: true,
    operateurs_liste: [],
    controleGeometre: {},
    operateur: {
      id: null,
      nom: null
    },
    showNewControleGeometreBtn: false,
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-ControleMutation
     */
    async searchControleGeometre() {
      await this.searchOperateurs();
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

            // Lier l'id du visa à son nom
            if (this.controleGeometre.operateur_id === null) {
              this.controleGeometre.operateur_id = JSON.parse(localStorage.getItem("infolica_user")).id;
            }
            this.operateur = this.operateurs_liste.filter(x => x.id === this.controleGeometre.operateur_id)[0];
            
            if (this.controleGeometre.date) {
              this.controleGeometre.date = moment(this.controleGeometre.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            } else {
              this.controleGeometre.date = moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
          } 
        })
        .catch(err =>  handleException(err, this));
    },

    /**
     * Cherche les opérateurs
     */
    async searchOperateurs() {
      return new Promise((resolve, reject) => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
          )
          .then(response => {
            if (response.data) {
              this.operateurs_liste = response.data
                .filter(x => x.responsable)
                .map(x => ({
                  id: x.id,
                  nom: [x.nom, x.prenom].join(" "),
                  toLowerCase: () => [x.nom, x.prenom].join(" ").toLowerCase(),
                  toString: () => [x.nom, x.prenom].join(" ")
                }));
                resolve(response);
            }
          })
          .catch(() => reject);
      })
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
    }

  },

  mounted: function() {
    this.searchControleGeometre();
    this.searchOperateurs();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_CONTROLE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



