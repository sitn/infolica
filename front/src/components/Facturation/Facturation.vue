<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
var numeral = require("numeral");
import { checkLogged, getCurrentDate } from "@/services/helper";
import { validationMixin } from "vuelidate";
import { required, minLength } from "vuelidate/lib/validators";

export default {
  name: "Facturation",
  mixins: [validationMixin],
  props: {},
  data: () => ({
    showNewFactureBtn: false,
    deleteFactureActive: false,
    deleteFactureMessage: "",
    deleteFactureId: null,
    clients_liste: [],
    clients_liste_select: [],
    affaire_factures: [],
    showFactureDialog: false,
    createFacture: false,
    lastRecordSAP: null,
    dataSaved: null,
    selectedFacture: {
      id: null,
      sap: null,
      date: null,
      txtSearchClient: null,
      client_id: null,
      client_obj: {},
      montant_mo: null,
      montant_mat_diff: null,
      montant_rf: null,
      montant_tva: null,
      montant_total: null,
      remarque: null
    }
  }),

  // Validations
  validations: {
    selectedFacture: {
      sap: { required },
      date: { required },
      txtSearchClient: {
        required,
        minLength: minLength(3)
      },
      montant_mo: { required },
      montant_mat_diff: { required },
      montant_rf: { required },
      montant_tva: { required },
      montant_total: { required }
    }
  },

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
     * Lier le nom du client à son id (facture.client_id) dans le tableau
     */
    async searchClients() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
        )
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
      if (this.selectedFacture.txtSearchClient != null) {
        if (this.selectedFacture.txtSearchClient.length < 3) {
          return;
        } else {
          this.clients_liste_select = this.clients_liste
            .filter(client_i => {
              return [client_i.entreprise, client_i.prenom, client_i.nom]
                .join(" ")
                .toLowerCase()
                .includes(this.selectedFacture.txtSearchClient.toLowerCase());
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
     * Créer une nouvelle facture
     */
    newFacture() {
      this.selectedFacture = {
        id: null,
        sap: null,
        date: getCurrentDate(),
        txtSearchClient: null,
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
    },

    /**
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      const field = this.$v.selectedFacture[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    },

    /**
     * Confirmer l'édition de la facture et l'enregistrer
     */
    onConfirmEditFacture() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.saveData();
      }
    },

    /**
     * Save data
     */
    saveData() {
      // Récupère l'id du client selon si il provient d'une modif de facture ou d'une création de facture
      var client_id;
      if (this.clients_liste_select[0]) {
        client_id = this.clients_liste_select[0].id;
      } else {
        client_id = this.selectedFacture.client_id;
      }

      var formData = new FormData();
      if (this.selectedFacture.id)
        formData.append("id", this.selectedFacture.id);
      if (this.selectedFacture.sap)
        formData.append("sap", this.selectedFacture.sap);
      if (this.selectedFacture.date)
        formData.append("date", this.selectedFacture.date);
      if (client_id) formData.append("client_id", client_id);
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
            this.lastRecordSAP = this.selectedFacture.sap;
            this.dataSaved = true;
            this.searchAffaireFactures();
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
      this.onCancelEditFacture();
    },

    /**
     * Annuler l'édition de la facture
     */
    onCancelEditFacture: function() {
      this.createFacture = false;
      this.showFactureDialog = false;
      this.selectedFacture.txtSearchClient = null;
      this.$v.$reset();
    },

    /**
     * Confirmer suppression facture
     */
    callDeleteFacture(facture) {
      this.deleteFactureActive = true;
      this.deleteFactureMessage =
        "Confirmer la suppression de la facture SAP '<strong>" +
        facture.sap +
        "<strong>' ?";
      this.deleteFactureId = facture.id;
    },

    /**
     * Delete facture
     */
    onConfirmDelete() {
      var formData = new FormData();
      formData.append("id", this.deleteFactureId);

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
      this.deleteFactureId = null;
    },

    /**
     * Annuler la suppression de facture
     */
    onCancelDelete() {
      this.deleteFactureId = null;
    }
  },

  mounted: function() {
    checkLogged();
    this.searchClients();
  }
};
</script>



