<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
import { getCurrentDate,
         getClients,
         filterList,
        //  stringifyAutocomplete,
         getDocument,
         logAffaireEtape } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

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
  data: () => {
    return {
      affaire_devis: [],
      affaire_factures: [],
      numeros_references: [],
      numeros_references_bk: [],
      numeros_references_restant: [],
      clients_liste: [],
      clients_liste_select: [],
      createFacture: false,
      configFactureTypeID: {
        devis: Number(process.env.VUE_APP_FACTURE_TYPE_DEVIS_ID),
        facture: Number(process.env.VUE_APP_FACTURE_TYPE_FACTURE_ID),
      },
      dataSaved: null,
      deleteFactureActive: false,
      deleteFactureId: null,
      deleteFactureMessage: "",
      lastRecordSAP: null,
      selectedFacture: {
        id: null,
        client: null,
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
    // const objectValidation = (client) => client && client.id && client.nom;

    let selectedFacture = {
      // date: { required },
      // client: { objectValidation },
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
          this.$route.params.id,
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
              x.date = x.date !== null? moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT): null;
              x.montant_mo = numeral(x.montant_mo).format("0.00");
              x.montant_mat_diff = numeral(x.montant_mat_diff).format("0.00");
              x.montant_rf = numeral(x.montant_rf).format("0.00");
              x.montant_tva = numeral(x.montant_tva).format("0.00");
              x.montant_total = numeral(x.montant_total).format("0.00");
              if (x.numeros === undefined || x.numeros === null) {
                x.numeros_id = [];
                x.numeros = [];
              } else {
                x.numeros_id = x.numeros;
                // Met à jour les numéros restant pour la facturation
                x.numeros_id.forEach(y => {
                  this.numeros_references_restant = this.numeros_references_restant.filter(z => z.numero_id !== y);
                });
                // Récupère le numéro du BF par l'id
                let tmp2 = [];
                x.numeros.forEach(y => tmp2.push(this.numeros_references.filter(z => z.numero_id === y)[0].numero));
                x.numeros = tmp2;
              }

              // Composer l'adresse de facturation
              let adresse_ = ""
              if (x.client_type_id === this.clientTypes_conf.moral) {
                adresse_ = [
                  x.client_premiere_ligne,
                  [(x.client_premiere_ligne? "Par" : null), x.client_entreprise].filter(Boolean).join(" "),
                  x.client_co,
                  x.client_adresse,
                  x.client_case_postale,
                  [x.client_npa, x.client_localite].filter(Boolean).join(" ")
                ].filter(Boolean);
              } else {
                adresse_ = [
                  x.client_premiere_ligne,
                  [x.client_premiere_ligne? "Par" : null, x.client_titre, x.client_prenom, x.client_nom].filter(Boolean).join(" "),
                  x.client_co,
                  x.client_adresse,
                  x.client_case_postale,
                  [x.client_npa, x.client_localite].filter(Boolean).join(" ")
                ].filter(Boolean);
              }
              
              x.adresse_facturation_ = adresse_.join(", ");
              
            });

            this.affaire_devis = tmp.filter(x => x.type_id === this.configFactureTypeID.devis);
            this.affaire_factures = tmp.filter(x => x.type_id === this.configFactureTypeID.facture);
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Liste des clients
     */
    async searchClients() {
      getClients()
        .then(response => {
          if (response && response.data) {
            this.clients_liste = response.data.map(x => ({
              id: x.id,
              nom: x.adresse_,
              type_id: x.type_client,
              besoin_vref_facture: x.besoin_vref_facture,
              toLowerCase: () => x.adresse_.toLowerCase(),
              toString: () => x.adresse_
            }));
          }
        }).catch(err => handleException(err, this));
    },

    /**
     * Crée la liste de sélection du client lors de la création de facture
     */
    getClientSearch(term) {
      this.clients_liste_select = filterList(this.clients_liste, term, 3);
    },

    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      return new Promise((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" + this.$route.params.id,
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
    openFactureEdition(data, type) {
      let tmp = {};
      if (type === 'devis') {
        tmp = this.affaire_devis.filter(x => x.id === data.id)[0];
      } else if (type === 'facture') {
        tmp = this.affaire_factures.filter(x => x.id === data.id)[0];
      } else {
        this.$root.$emit('ShowError', 'Une erreur est survenue, contacter le développeur.')
      }

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
      }

      // récupère le client de la facture
      let client_facture_tmp = this.clients_liste.filter(x => x.id === data.client_id);
      if (client_facture_tmp && client_facture_tmp.length > 0) {
        this.selectedFacture.client = client_facture_tmp[0];
      } else {
        this.selectedFacture.client = {
          id: data.client_id,
          nom: data.adresse_facturation_,
          type_id: data.client_type_id,
          toString: () => data.adresse_facturation_,
          toLowerCase: () => data.adresse_facturation_.toLowerCase()
        };
      }
        this.selectedClient = this.selectedFacture.client;
        this.selectedFacture.client = null;

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
    newFacture(facture_type) {
      // set automatically date facture only if affaire etape is in edition facture 
      let dateFacture = null;
      if (this.affaire.etape_id === Number(process.env.VUE_APP_ETAPE_FACTURE_ID)) {
        dateFacture = getCurrentDate();
      }

      this.selectedFacture = {
        id: null,
        sap: null,
        date: dateFacture,
        client: null,
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
        this.selectedFacture.client = this.clients_liste.filter(x => x.id === Number(process.env.VUE_APP_CLIENT_CADASTRATION_ID))[0];
      }
      
      if (facture_type === 'devis') {
        this.selectedFacture.type_id = this.configFactureTypeID.devis;
      } else if (facture_type === 'facture') {
        this.selectedFacture.type_id = this.configFactureTypeID.facture;
      }
      
      this.showReferenceNumeroFacture = true;
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
      let formData = new FormData();
      formData.append("affaire_id", this.$route.params.id);
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
      if (this.selectedFacture.client && this.selectedFacture.client.id) {
        formData.append("client_id", this.selectedFacture.client.id);
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
        "ADRESSE_PROPRIETAIRE": facture.adresse_facturation_.replace(/, /gi, "\n"),
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
     * set selected Client object if not the case
     * workaround to get client object in md-select
     */
    setSelectedClientObject(client) {
      this.selectedFacture.client = {...client};
    }

  },

  mounted: function() {
    this.searchClients();
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



