<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
var numeral = require("numeral");
import checkLogged from "@/services/helper";


export default {
  name: "Facturation",
  props: {},
  data: () => ({
    affaire_factures: [],
    showFactureDialog: false,
    selectedFacture: {
      id: null,
      sap: null,
      client_id: null,
      montant_mo: null,
      montant_mat_diff: null,
      montant_rf: null,
      montant_tva: null,
      montant_total: null,
    },
  }),

  methods: {

    /*
     * SEARCH AFFAIRE FACTURES
     */
    async searchAffaireFactures() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response && response.data) {
            this.affaire_factures = response.data.map(x => ({
              id: x.id,
              sap: x.sap,
              date: x.date,
              client_id: x.client_id,
              montant_mo: numeral(x.montant_mo).format('0.00'),
              montant_mat_diff: numeral(x.montant_mat_diff).format('0.00'),
              montant_rf: numeral(x.montant_rf).format('0.00'),
              montant_tva: numeral(x.montant_tva).format('0.00'),
              montant_total: numeral(x.montant_total).format('0.00'),
            }))
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

    /**
     * Edit facture
     */
    openFactureEdition(data) {
      this.showFactureDialog = true;
      this.selectedFacture = data;
    },

    /**
     * Confirmer l'édition de la facture et l'enregistrer
     */
    onConfirmEditFacture (){
      var formData = new FormData();
      if (this.selectedFacture.id) formData.append("id", this.selectedFacture.id);
      if (this.selectedFacture.sap) formData.append("sap", this.selectedFacture.sap);
      if (this.selectedFacture.date) formData.append("date", this.selectedFacture.date);
      if (this.selectedFacture.client_id) formData.append("client_id", this.selectedFacture.client_id);
      if (this.selectedFacture.montant_mo) formData.append("montant_mo", this.selectedFacture.montant_mo);
      if (this.selectedFacture.montant_mat_diff) formData.append("montant_mat_diff", this.selectedFacture.montant_mat_diff);
      if (this.selectedFacture.montant_rf) formData.append("montant_rf", this.selectedFacture.montant_rf);
      if (this.selectedFacture.montant_tva) formData.append("montant_tva", this.selectedFacture.montant_tva);
      if (this.selectedFacture.montant_total) formData.append("montant_total", this.selectedFacture.montant_total);
      if (this.selectedFacture.indice_tva) formData.append("indice_tva", this.selectedFacture.indice_tva);
      if (this.selectedFacture.indice_application_mo) formData.append("indice_application_mo", this.selectedFacture.indice_application_mo);
      // formData.append("indice_tva", undefined);
      // formData.append("indice_application_mo", undefined);
      formData.append("affaire_id", this.$route.params.id);

      this.$http
        .put(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_FACTURE_ENDPOINT,
            formData,
            {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            .then( response => {
              if (response.data) {
              this.searchAffaireFactures()
              }
            })
            .catch(err => {
              alert("error: " + err)
            });

      this.showFactureDialog = false;
    },


    /**
     * Delete facture
     */
    doDeleteFacture (facture_id) {
      var formData = new FormData()
      formData.append("id", facture_id);
      
      this.$http.delete(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_FACTURE_ENDPOINT,
        {data: formData}
      ).then( response => {
        if (response.data) {
        this.searchAffaireFactures()
      }
      }).catch(err => {
        alert("error: " + err)
      })
    },


     /**
     * Annuler l'édition de la facture
     */
    onCancelEditFacture: function(){
      this.showFactureDialog = false;
    }

  },

  mounted: function() {
    checkLogged();
    this.searchAffaireFactures();
  }
};
</script>



