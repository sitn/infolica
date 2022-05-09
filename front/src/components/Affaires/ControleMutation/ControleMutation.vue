<style src="./controleMutation.css" scoped></style>
<template src="./controleMutation.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {setDateFormatClient, logAffaireEtape} from '@/services/helper';

const moment = require('moment')

export default {
  name: "ControleMutation",
  props: {
    affaire: Object,
    permission: Object
  },
  data: () => ({
    showNewControleMutationBtn: false,
    needToCreateControleMutation: false,
    controleMutation: {},
    checkAll: {
      suivi_: false,
      bf_: false,
      cs_: false,
      od_: false,
      bat_: false,
      serv_: false,
      suiv_mut_: false,
      div_: false,
    }
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-ControleMutation
     */
    async searchControleMutation() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_CONTROLE_MUTATION_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.controleMutation = response.data;
            
            // set dates to client format
            this.controleMutation = setDateFormatClient(this.controleMutation);

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
     * Création d'un nouveau suivi
     */
    newControleMutation() {
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
            this.searchControleMutation();
            this.needToCreateControleMutation = false;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    onCancelEditControleMutation() {
      this.searchControleMutation();
    },

    /**
     * Stringify Date
     */
    stringifyDate(key) {
      this.controleMutation[key] = String(this.controleMutation[key]);
    },

    /**
     * set true-value
     */
    setTrueValue(element){
      if (this.controleMutation[element]) {
        return this.controleMutation[element];
      } else {
        return moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      }
    },

    /**
     * Save
     */  
    onConfirmEditControleMutation() {
      var formData = new FormData();
      formData.append("id", this.controleMutation.id);
      formData.append("affaire_id", this.controleMutation.affaire_id);
      formData.append("suivi_1", this.controleMutation.suivi_1? moment(this.controleMutation.suivi_1, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_2", this.controleMutation.suivi_2? moment(this.controleMutation.suivi_2, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_3", this.controleMutation.suivi_3? moment(this.controleMutation.suivi_3, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_4", this.controleMutation.suivi_4? moment(this.controleMutation.suivi_4, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_5", this.controleMutation.suivi_5? moment(this.controleMutation.suivi_5, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_6", this.controleMutation.suivi_6? moment(this.controleMutation.suivi_6, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_7", this.controleMutation.suivi_7? moment(this.controleMutation.suivi_7, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_8", this.controleMutation.suivi_8? moment(this.controleMutation.suivi_8, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_9", this.controleMutation.suivi_9? moment(this.controleMutation.suivi_9, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_10", this.controleMutation.suivi_10? moment(this.controleMutation.suivi_10, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_11", this.controleMutation.suivi_11? moment(this.controleMutation.suivi_11, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("suivi_12", this.controleMutation.suivi_12? moment(this.controleMutation.suivi_12, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("bf_1", this.controleMutation.bf_1);
      formData.append("bf_2", this.controleMutation.bf_2);
      formData.append("bf_3", this.controleMutation.bf_3);
      formData.append("bf_4", this.controleMutation.bf_4);
      formData.append("cs_1", this.controleMutation.cs_1);
      formData.append("cs_2", this.controleMutation.cs_2);
      formData.append("cs_3", this.controleMutation.cs_3);
      formData.append("cs_4", this.controleMutation.cs_4);
      formData.append("cs_5", this.controleMutation.cs_5);
      formData.append("od_1", this.controleMutation.od_1);
      formData.append("od_2", this.controleMutation.od_2);
      formData.append("od_3", this.controleMutation.od_3);
      formData.append("od_4", this.controleMutation.od_4);
      formData.append("od_5", this.controleMutation.od_5);
      formData.append("bat_1", this.controleMutation.bat_1);
      formData.append("bat_2", this.controleMutation.bat_2);
      formData.append("bat_3", this.controleMutation.bat_3);
      formData.append("bat_4", this.controleMutation.bat_4);
      formData.append("serv_1", this.controleMutation.serv_1);
      formData.append("serv_2", this.controleMutation.serv_2);
      formData.append("serv_3", this.controleMutation.serv_3);
      formData.append("nom_1", this.controleMutation.nom_1);
      formData.append("suiv_mut_1", this.controleMutation.suiv_mut_1);
      formData.append("suiv_mut_2", this.controleMutation.suiv_mut_2);
      formData.append("div_1", this.controleMutation.div_1);
      formData.append("div_2", this.controleMutation.div_2);
      formData.append("div_3", this.controleMutation.div_3);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      formData.append("visa", JSON.parse(localStorage.getItem("infolica_user")).id);
      
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
            this.searchControleMutation();

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CONTROLE_MUTATION_ID), "Edition du formulaire");
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Select all checkbox (subdomain)
     */
    selectAll(key_) {
      for (let key in this.controleMutation) {
        if (["suivi_", ].includes(key_)) {
          if (key.startsWith(key_)) {
            if (this.checkAll[key_]) {
              // Case desactivée
              this.controleMutation[key] = moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            } else {
              // Case activée
              this.controleMutation[key] = null;
            }
          }
        } else {
          if (key.startsWith(key_)) {  
            this.controleMutation[key] = this.checkAll[key_];
          }
        }
      }

    }
  },

  mounted: function() {
    this.searchControleMutation();
  }
};
</script>



