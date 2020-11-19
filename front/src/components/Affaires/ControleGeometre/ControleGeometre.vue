<style src="./controleGeometre.css" scoped></style>
<template src="./controleGeometre.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission} from '@/services/helper';

const moment = require('moment')

export default {
  name: "controleGeometre",
  props: {
    affaire: Object,
    typesAffaires_conf: Object
  },
  data: () => ({
    affaireReadonly: true,
    needToCreateControleMutation: false,
    chefsProjetMO_liste: [],
    controleGeometre: {}
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
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.controleGeometre = response.data;
            // Lier l'id du visa à son nom
            if (this.controleGeometre.visa) {
              this.controleGeometre.visa = this.chefsProjetMO_liste.filter(x => {
              return x.id == this.controleGeometre.visa
              })[0];
            }
            if (this.controleGeometre.date) {
              this.controleGeometre.date = moment(this.controleGeometre.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
          } else {
            // Il n'existe pas encore de suivi de mandat pour cette affaire
            this.needToCreateControleMutation = true;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
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
              this.chefsProjetMO_liste = response.data
                .filter(x => {
                  return x.responsable;
                })
                .map(x => ({
                  id: x.id,
                  nom: [x.nom, x.prenom].join(" "),
                  toLowerCase: () => [x.nom, x.prenom].join(" ").toLowerCase(),
                  toString: () => [x.nom, x.prenom].join(" ")
                }));
                resolve(this.chefsProjetMO_liste);
            }
          })
          .catch(() => reject);
      })
    },

    /**
     * Création d'un nouveau suivi
     */
    newControleGeometre() {
      var formData = new FormData();
      formData.append("affaire_id", this.$route.params.id);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_CONTROLE_MUTATION_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response) {
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été créé avec succès")
            this.searchControleGeometre();
            this.needToCreateControleMutation = false;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    onCancelEditControleGeometre() {
      this.searchControleGeometre();
    },

    onConfirmEditControleMutation() {
      var formData = new FormData();
      formData.append("id", this.controleGeometre.id);
      formData.append("affaire_id", this.controleGeometre.affaire_id);
      if (this.controleGeometre.bf_1) {
        formData.append("bf_1", this.controleGeometre.bf_1);
      }

      this.$http
        .put(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_CONTROLE_MUTATION_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response) {
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été mis à jour avec succès")
            this.searchControleGeometre();
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },
  },

  mounted: function() {
    this.searchControleGeometre();
    this.searchOperateurs();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_CONTROLE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



