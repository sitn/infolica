<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
var numeral = require("numeral");
import { checkLogged, getCurrentDate } from "@/services/helper";

export default {
  name: "Facturation",
  props: {},
  data: () => ({
    clients_liste: [],
    clients_liste_select: [],
    affaire_factures: [],
    showFactureDialog: false,
    createFacture: false,
    txtSearchClient: null,
    selectedFacture: {
      id: null,
      sap: null,
      date: null,
      client_id: null,
      client_obj: {},
      montant_mo: null,
      montant_mat_diff: null,
      montant_rf: null,
      montant_tva: null,
      montant_total: null,
      remarque: null
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
        )
        .then(response => {
          if (response && response.data) {
            this.affaire_factures = response.data.map(x => ({
              id: x.id,
              sap: x.sap,
              date: x.date,
              client_id: x.client_id,
              client_obj: this.clients_liste
                .filter(obj => {
                  return obj.id === x.client_id;
                })
                .pop(),
              montant_mo: numeral(x.montant_mo).format("0.00"),
              montant_mat_diff: numeral(x.montant_mat_diff).format("0.00"),
              montant_rf: numeral(x.montant_rf).format("0.00"),
              montant_tva: numeral(x.montant_tva).format("0.00"),
              montant_total: numeral(x.montant_total).format("0.00"),
              remarque: x.remarque
            }));
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /**
     * Lier le nom du client à son id (facture.client_id)
     */
    async searchClients() {
      this.$http
        .get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT)
        .then(response => {
          if (response.data) {
            this.clients_liste = response.data;
            this.searchAffaireFactures();
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /**
     * Crée la liste de sélection du client lors de la création de facture
     */
    getClientSearch() {
      this.clients_liste_select = [];
      if (this.txtSearchClient != null) {
        if (this.txtSearchClient.length < 3) {
          return
        } else {
          this.clients_liste_select = this.clients_liste
            .filter(data => {
              return data.nom.toLowerCase().includes(this.txtSearchClient.toLowerCase());
            })
            .map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
        }
      }
    },

    /**
     * Calcul le montant total de la facture à la volée lors de l'édition
     */
    computeTotal() {
      this.selectedFacture.montant_total =
        Number(this.selectedFacture.montant_mo) +
        Number(this.selectedFacture.montant_mat_diff) +
        Number(this.selectedFacture.montant_rf) +
        Number(this.selectedFacture.montant_tva);
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
    onConfirmEditFacture() {
      var formData = new FormData();
      if (this.selectedFacture.id)
        formData.append("id", this.selectedFacture.id);
      if (this.selectedFacture.sap)
        formData.append("sap", this.selectedFacture.sap);
      if (this.selectedFacture.date)
        formData.append("date", this.selectedFacture.date);
      if (this.clients_liste_select[0].id)
        formData.append("client_id", this.clients_liste_select[0].id);
      if (this.selectedFacture.montant_mo)
        formData.append("montant_mo", this.selectedFacture.montant_mo);
      if (this.selectedFacture.montant_mat_diff)
        formData.append(
          "montant_mat_diff",
          this.selectedFacture.montant_mat_diff
        );
      if (this.selectedFacture.montant_rf)
        formData.append("montant_rf", this.selectedFacture.montant_rf);
      if (this.selectedFacture.montant_tva)
        formData.append("montant_tva", this.selectedFacture.montant_tva);
      if (this.selectedFacture.montant_total)
        formData.append("montant_total", this.selectedFacture.montant_total);
      if (this.selectedFacture.indice_tva)
        formData.append("indice_tva", this.selectedFacture.indice_tva);
      if (this.selectedFacture.indice_application_mo)
        formData.append(
          "indice_application_mo",
          this.selectedFacture.indice_application_mo
        );
      if (this.selectedFacture.remarque)
        formData.append("remarque", this.selectedFacture.remarque);
      formData.append("affaire_id", this.$route.params.id);

      // Type de requête selon si c'est une création ou une modification de facture
      if (this.createFacture) {
        var req;
        req = this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
          formData
        );
      } else {
        req = this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
          formData
        );
      }
      req
        .then(response => {
          if (response.data) {
            this.searchAffaireFactures();
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
      this.createFacture = false;
      this.showFactureDialog = false;
    },

    /**
     * Annuler l'édition de la facture
     */
    onCancelEditFacture: function() {
      this.createFacture = false;
      this.showFactureDialog = false;
    },

    /**
     * Delete facture
     */
    doDeleteFacture(facture_id) {
      var formData = new FormData();
      formData.append("id", facture_id);

      this.$http
        .delete(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
          { data: formData }
        )
        .then(response => {
          if (response.data) {
            this.searchAffaireFactures();
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
    },

    /**
     * Créer une nouvelle facture
     */
    newFacture() {
      this.selectedFacture = {
        id: null,
        sap: null,
        date: getCurrentDate(),
        client_id: null,
        client_obj: {},
        montant_mo: 0,
        montant_mat_diff: 0,
        montant_rf: 0,
        montant_tva: 0,
        montant_total: 0,
        remarque: null
      };
      this.showFactureDialog = true;
      this.createFacture = true;
    }
  },

  mounted: function() {
    checkLogged();
    this.searchClients();
  }
};
</script>



