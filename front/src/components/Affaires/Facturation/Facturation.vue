<style src="./facturation.css" scoped></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./facturation.html"></template>


<script>
import { getCurrentDate,
         stringifyAutocomplete2,
         getDocument,
         logAffaireEtape,
         downloadGeneratedDocument,
         deleteGeneratedDocument } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import Emoluments from "@/components/Affaires/Facturation/Emoluments/Emoluments.vue";
import ClientSearch from "@/components/Utils/ClientSearch/ClientSearch.vue";

const numeral = require("numeral");
const moment = require('moment')

export default {
  name: "Facturation",
  mixins: [validationMixin],
  props: {
    affaire: Object,
    typesAffaires_conf: Object,
    permission: Object,
    clientTypes_conf: Object
    },
  components: {
    ClientSearch,
    Emoluments
  },
  data: () => {
    return {
      affaire_devis: [],
      affaire_factures: [],
      numeros_references: [],
      numeros_references_bk: [],
      numeros_references_restant: [],
      createFacture: false,
      configFactureTypeID: {
        devis: Number(process.env.VUE_APP_FACTURE_TYPE_DEVIS_ID),
        facture: Number(process.env.VUE_APP_FACTURE_TYPE_FACTURE_ID),
      },
      dataSaved: null,
      deleteFactureActive: false,
      deleteFactureId: null,
      deleteFactureMessage: "",
      factureTypes: [],
      lastRecordSAP: null,
      selectedFacture: {
        id: null,
        client_id: null,
        client_premiere_ligne: null,
        date: null,
        montant_mat_diff: null,
        montant_mo: null,
        montant_rf: null,
        montant_total: null,
        montant_tva: null,
        numeros: null,
        remarque: null,
        sap: null
      },
      selectedClient: null, // workaround to get client object in md-select
      showNewFactureBtn: false,
      showFactureDialog: false,
      showReferenceNumeroFacture: false,
    }
  },

  // Validations
  validations() {

    let selectedFacture = {
      montant_mo: { required },
      montant_mat_diff: { required },
      montant_rf: { required },
      montant_tva: { required },
      montant_total: { required }
    };

    return { selectedFacture };
  },

  methods: {
    /**
     * Validation of objects
     */

    /*
     * SEARCH AFFAIRE FACTURES
     */
    async searchAffaireFactures() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT +
          this.affaire.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            let tmp = response.data;
            // copy numeros_references backup to get complete liste
            this.numeros_references_restant = [...this.numeros_references_bk];
            tmp.forEach(x => {
              // Met à jour les numéros restant pour la facturation
              x.numeros_id.forEach(y => {
                this.numeros_references_restant = this.numeros_references_restant.filter(z => z.numero_id !== y);
              });
            });

            this.affaire_devis = tmp.filter(x => x.type_id === this.configFactureTypeID.devis);
            this.affaire_factures = tmp.filter(x => x.type_id === this.configFactureTypeID.facture);
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      return new Promise((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" + this.affaire.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.numeros_references = response.data.filter(x => x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID));
            this.numeros_references_restant = [...this.numeros_references];
            this.numeros_references_bk = [...this.numeros_references];
            resolve(this.numeros_references);
          }
        })
        .catch(err => {
          handleException(err, this);
          reject(err);
        });
      });
    },

    /**
     * Calcul le montant total de la facture à la volée lors de l'édition
     */
    computeTotal() {
      this.selectedFacture.montant_total = numeral(
        Number(this.selectedFacture.montant_mo) +
        Number(this.selectedFacture.montant_mat_diff) +
        Number(this.selectedFacture.montant_rf) +
        Number(this.selectedFacture.montant_tva)).format('0.00');
    },

    /**
     * Edit facture
     */
    openFactureEdition(data, type, newMontants=false) {
      let tmp = {};
      if (type === 'devis') {
        tmp = this.affaire_devis.filter(x => x.id === data.id)[0];
      } else if (type === 'facture') {
        tmp = this.affaire_factures.filter(x => x.id === data.id)[0];
      } else {
        this.$root.$emit('ShowError', 'Une erreur est survenue, contacter le développeur.')
      }

      if (newMontants) {
        this.selectedFacture = {
          id: tmp.id,
          sap: tmp.sap,
          date: tmp.date !== null? tmp.date: moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
          client_premiere_ligne: tmp.client_premiere_ligne,
          montant_mo: numeral(data.montant_mo).format('0.00'),
          montant_mat_diff: numeral(data.montant_mat_diff).format('0.00'),
          montant_rf: numeral(data.montant_rf).format('0.00'),
          montant_tva: numeral(data.montant_tva).format('0.00'),
          montant_total: numeral(data.montant_total).format('0.00'),
          numeros: tmp.numeros,
          numeros_obj: [],
          remarque: tmp.remarque,
          type_id: tmp.type_id,
          client_id: tmp.client_id,
        }
      } else {
        this.selectedFacture = {
          id: tmp.id,
          sap: tmp.sap,
          date: tmp.date !== null? tmp.date: moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
          client_premiere_ligne: tmp.client_premiere_ligne,
          montant_mo: numeral(tmp.montant_mo).format('0.00'),
          montant_mat_diff: numeral(tmp.montant_mat_diff).format('0.00'),
          montant_rf: numeral(tmp.montant_rf).format('0.00'),
          montant_tva: numeral(tmp.montant_tva).format('0.00'),
          montant_total: numeral(tmp.montant_total).format('0.00'),
          numeros: tmp.numeros,
          numeros_obj: [],
          remarque: tmp.remarque,
          type_id: tmp.type_id,
          client_id: tmp.client_id,
        }
      }


      if (this.affaire.type_id === this.typesAffaires_conf.cadastration) {
        this.selectedFacture.numeros_id = [];
        tmp.numeros_id.forEach(x => this.selectedFacture.numeros_obj.push(this.numeros_references.filter(y => y.numero_id === x)[0]));
        this.selectedFacture.numeros_obj.forEach(x => this.selectedFacture.numeros_id.push(x.numero_id));
      }

      this.showReferenceNumeroFacture = false;
      this.showFactureDialog = true;
    },

    /**
     * Créer une nouvelle facture
     */
    async newFacture(facture_type) {
      let dateFacture = null;
      if (this.affaire.etape_id === Number(process.env.VUE_APP_ETAPE_FACTURE_ID)) {
        dateFacture = getCurrentDate();
      }

      this.selectedFacture = {
        id: null,
        sap: null,
        date: dateFacture,
        client_id: null,
        client_premiere_ligne: null,
        montant_mo: numeral(0).format('0.00'),
        montant_mat_diff: numeral(0).format('0.00'),
        montant_rf: numeral(0).format('0.00'),
        montant_tva: numeral(0).format('0.00'),
        montant_total: numeral(0).format('0.00'),
        numeros: null,
        remarque: null
      };

      // Set default client if affaire type is cadastration
      if (this.affaire.type_id === this.typesAffaires_conf.cadastration) {
        this.selectedFacture.client_id = process.env.VUE_APP_CLIENT_CADASTRATION_ID;
      }

      if (facture_type === 'devis') {
        this.selectedFacture.type_id = this.configFactureTypeID.devis;
      } else if (facture_type === 'facture') {
        this.selectedFacture.type_id = this.configFactureTypeID.facture;
      }

      this.showReferenceNumeroFacture = true;
      this.showFactureDialog = true;
      this.createFacture = true;
      this.selectedClient = null;
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
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("id", this.selectedFacture.id);
      formData.append("sap", this.selectedFacture.sap || null);
      formData.append("remarque", this.selectedFacture.remarque || null);
      formData.append("client_premiere_ligne", this.selectedFacture.client_premiere_ligne || null);

      if (this.selectedFacture.type_id) {
        formData.append("type_id", this.selectedFacture.type_id);
      }
      if (this.selectedFacture.date) {
        formData.append("date", moment(this.selectedFacture.date, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }
      if (this.selectedFacture.client_id) {
        formData.append("client_id", this.selectedFacture.client_id);
      }

      if (this.selectedFacture.montant_mo) {
        formData.append("montant_mo", this.selectedFacture.montant_mo);
      }
      if (this.selectedFacture.montant_mat_diff) {
        formData.append("montant_mat_diff", this.selectedFacture.montant_mat_diff);
      }
      if (this.selectedFacture.montant_rf) {
        formData.append("montant_rf", this.selectedFacture.montant_rf);
      }
      if (this.selectedFacture.montant_tva) {
        formData.append("montant_tva", this.selectedFacture.montant_tva);
      }
      if (this.selectedFacture.montant_total) {
        formData.append("montant_total", this.selectedFacture.montant_total);
      }
      if (this.selectedFacture.numeros_id) {
        formData.append("numeros", JSON.stringify(this.selectedFacture.numeros_id));
      } else {
        formData.append("numeros", null);
      }

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

            //Log edition facture
            let facture_type = "";
            let showMessage = "";
            if (this.selectedFacture.type_id === this.configFactureTypeID.facture) {
              facture_type = "facture";
              showMessage = "La facture a été enregistrée avec succès";
            } else if (this.selectedFacture.type_id === this.configFactureTypeID.devis) {
              facture_type = "devis";
              showMessage = "Le devis a été enregistré avec succès";
            }
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_FACTURE_SECONDAIRE_ID), "Édition de " + facture_type);

            this.searchAffaireFactures();
            this.$root.$emit('reloadClientFactureInfosGen');
            this.$root.$emit("ShowMessage", showMessage);
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
      this.selectedClient = null;
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

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_FACTURE_SECONDAIRE_ID), "Suppression");
            this.$root.$emit("getEmolumentsGeneral");

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
    },

    /**
     * Set finance format for numbers in facture
     */
    setFinanceFormat(key) {
      this.selectedFacture[key] = numeral(this.selectedFacture[key]).format('0.00');
    },

    /**
     * openCreateClient
     */
    openCreateClient() {
      let routedata = this.$router.resolve({ name: "ClientsNew" });
      window.open(routedata.href, "_blank");
    },


    /**
     * Générer lettre propriétaire (Cadastration)
     */
    async generateLettreProprietaire(facture) {
      let numeros = [];
      if (facture.numeros.length > 0) {
        facture.numeros.forEach(facture_numero => numeros.push(facture_numero));

        if (numeros.length > 1) {
          numeros = numeros.sort((a, b) => {a-b});
        }
      }
      facture.numeros_ = numeros.join(", ");

      let formData = this.fillDataLettreProprietaire(facture);
      getDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le fichier '" + response + "' se trouve dans le dossier 'Téléchargement'")
      }).catch(err => handleException(err, this));
    },

    /**
     * Remplir le formulaire pour la lettre au propriétaire (cadastration)
     */
    fillDataLettreProprietaire(facture) {
      let formData = new FormData();
      formData.append("template", "LettreCad");
      formData.append("values", JSON.stringify({
        "ADRESSE_PROPRIETAIRE": facture.client_compiled_adress,
        "NREF": this.affaire.id,
        "DATE_ENVOI": facture.date,
        "TITRE": "Madame, Monsieur",
        "BIEN_FONDS": facture.numeros_,
        "CADASTRE": this.affaire.cadastre,
        "NO_NOTE_FRAIS": facture.sap,
        "MONTANT": facture.montant_total
      }));

      return formData;
    },

    /**
     * Générer réquisition pour le RF (Cadastration)
     */
    async generateReqRF(facture) {
      let numeros = [];
      if (facture.numeros.length > 0) {
        facture.numeros.forEach(facture_numero => numeros.push(facture_numero));

        if (numeros.length > 1) {
          numeros = numeros.sort((a, b) => {a-b});
        }
      }
      facture.numeros_ = numeros.join(", ");

      let formData = this.fillDataReqRF(facture);
      getDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le fichier '" + response + "' se trouve dans le dossier 'Téléchargement'")
      }).catch(err => handleException(err, this));
    },


    /**
     * Générer lettre d'accompagnement (rétablissement de PFP)
     */
    async generateLettrePFP(facture) {
      let formData = new FormData();
      formData.append('facture_id', facture.id);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_COURRIER_TEMPLATE_PFP_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          const filename = response.data.filename;

          downloadGeneratedDocument(filename).then(
            response => {
              deleteGeneratedDocument(response)
              .catch(err => handleException(err, this));
          }).catch(err => handleException(err, this));
        }
      }).catch(err => handleException(err, this));


    },

    /**
     * Remplir le formulaire pour la requisition au RF (cadastration)
     */
    fillDataReqRF(facture) {
      let formData = new FormData();
      formData.append("template", "ReqCad");
      formData.append("values", JSON.stringify({
        "ANNEE": new Date().getFullYear(),
        "DATE_PLAN_ORIGINE": facture.date,
        "BIEN_FONDS": facture.numeros_,
        "CADASTRE": this.affaire.cadastre,
        "DATE": facture.date,
      }));

      return formData;
    },

    onSelectNumeroReference(data) {
      this.selectedFacture.numeros_id = [];
      this.selectedFacture.numeros = [];
      data.forEach(x => {
        this.selectedFacture.numeros_id.push(x.numero_id);
        this.selectedFacture.numeros.push(x.numero_id);
      });
    },


    /**
     * open emolument dialog
     */
    async openEmolumentsDialog() {
      await this.$refs.emoluments.getTableauEmolumentsNew();
      await this.$refs.emoluments.initForm();
      this.$refs.emoluments.initFactureRepartition([]);
      this.$refs.emoluments.showEmolumentsDialog = true;
    },


    /**
     * get facture_types
     */
    getFactureTypes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_TYPE_ENDPOINT,
        {
          withCredentials: true,
          Headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.factureTypes = stringifyAutocomplete2(response.data);
        }
      }).catch(err => handleException(err, this));
    }

  },

  mounted: function() {
    this.getFactureTypes();
    this.searchAffaireNumeros().then(() => {
      this.searchAffaireFactures();
    });

    this.$root.$on("updateNumerosFactureList", () => this.searchAffaireNumeros());
    this.$root.$on("searchAffaireFactures", () => {
      setTimeout(() => {  this.searchAffaireFactures() }, 500);
    });
  }
};
</script>



