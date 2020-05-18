<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
var numeral = require("numeral");
import { getCurrentDate, checkPermission, getCurrentUserRoleId } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'
import { validationMixin } from "vuelidate";
import { required, minLength } from "vuelidate/lib/validators";

const moment = require('moment')

export default {
  name: "Facturation",
  mixins: [validationMixin],
  props: {},
  data: () => ({
    affaireReadonly: true,
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
      client: null,
      client_id: null,
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
      // sap: { required },
      date: { required },
      client: {
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
      await this.searchClients();
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.affaire_factures = response.data.map(x => ({
              id: x.id,
              sap: x.sap,
              date: moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
              client_id: x.client_id,
              client: this.clients_liste
                .filter(obj => {
                  return obj.id === x.client_id;
                }).pop(),
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
          handleException(err, this);
        });
    },

    /**
     * Lier le nom du client à son id (facture.client_id) dans le tableau
     */
    async searchClients() {
      return new Promise((resolve, reject) => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
          )
          .then(response => {
            if (response.data) {
              this.clients_liste = response.data.map(x => ({
                id: x.id,
                nom: [x.entreprise, x.prenom, x.nom].filter(Boolean).join(" "),
                toLowerCase: () => x.nom.toLowerCase(),
                toString: () => x.nom
              }));
              resolve(this.client_liste)
            }
          })
          .catch(() => reject);
      });
    },

    /**
     * Crée la liste de sélection du client lors de la création de facture
     */
    getClientSearch() {
      this.clients_liste_select = [];
      if (this.selectedFacture.client != null) {
        if (this.selectedFacture.client.length < 3) {
          return;
        } else {
          this.clients_liste_select = this.clients_liste
            .filter(client_i => {
              return client_i.nom
                .toLowerCase()
                .includes(this.selectedFacture.client.toLowerCase());
            });
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
      console.log(this.selectedFacture)
      this.selectedFacture.client = this.clients_liste.filter(x => {
        return x.id === this.selectedFacture.client_id
      }).pop();
    },

    /**
     * Créer une nouvelle facture
     */
    newFacture() {
      this.selectedFacture = {
        id: null,
        sap: null,
        date: getCurrentDate(),
        client: null,
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
      var formData = new FormData();
      if (this.selectedFacture.id)
        formData.append("id", this.selectedFacture.id);
      if (this.selectedFacture.sap)
        formData.append("sap", this.selectedFacture.sap);
      if (this.selectedFacture.date)
        formData.append("date", moment(this.selectedFacture.date, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      if (this.selectedFacture.client.id) formData.append("client_id", this.selectedFacture.client.id);
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
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        );
      } else {
        req = this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
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
          handleException(err, this);
        });
      this.onCancelEditFacture();
    },

    /**
     * Annuler l'édition de la facture
     */
    onCancelEditFacture: function() {
      this.createFacture = false;
      this.showFactureDialog = false;
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
          { 
            data: formData,
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response.data) {
            this.searchAffaireFactures();
          }
        })
        .catch(err => {
          handleException(err, this);
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
    this.searchClients();
    this.searchAffaireFactures();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_FACTURE_EDITION) || this.$parent.parentAffaireReadOnly;

    //Check if role secretaire
    if(this.affaireReadonly){
      var role_id = getCurrentUserRoleId();

      if(role_id && !isNaN(role_id) && 
        Number(role_id) === Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID) &&
        checkPermission(process.env.VUE_APP_AFFAIRE_FACTURE_EDITION)){
          this.affaireReadonly = false;
      }
    }
  }
};
</script>



