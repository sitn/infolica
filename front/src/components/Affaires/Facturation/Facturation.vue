<style src="./facturation.css" scoped></style>
<template src="./facturation.html"></template>


<script>
var numeral = require("numeral");
import { getCurrentDate,
         checkPermission,
         getCurrentUserRoleId,
         getClients,
         filterList,
         stringifyAutocomplete,
         getDocument,
         logAffaireEtape } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

const moment = require('moment')

export default {
  name: "Facturation",
  mixins: [validationMixin],
  props: {
    affaire: Object,
    typesAffaires_conf: Object
    },
  data: () => {
    return {
      affaire_devis: [],
      affaire_factures: [],
      numeros_references:[],
      affaireReadonly: true,
      clients_liste: [],
      clients_liste_type: [],
      clients_liste_select: [],
      clients_types_config: {
        personne_physique: Number(process.env.VUE_APP_TYPE_CLIENT_PHYSIQUE_ID),
        personne_morale: Number(process.env.VUE_APP_TYPE_CLIENT_MORAL_ID)
      },
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
        client_co: null,
        client_complement: null,
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
      show_co: false,
      showNewFactureBtn: false,
      showFactureDialog: false
    }
  },

  // Validations
  validations() {
    let selectedFacture = {};

    if (this.show_co) {
      selectedFacture = {
        date: { required },
        client: { required },
        montant_mo: { required },
        montant_mat_diff: { required },
        montant_rf: { required },
        montant_tva: { required },
        montant_total: { required },
        client_co: {required}
      };
    } else {
      selectedFacture = {
        date: { required },
        client: { required },
        montant_mo: { required },
        montant_mat_diff: { required },
        montant_rf: { required },
        montant_tva: { required },
        montant_total: { required }
      };
    }

    return { selectedFacture };
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
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            let tmp = response.data;
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
                let tmp2 = [];
                x.numeros.forEach(y => tmp2.push(this.numeros_references.filter(z => z.numero_id === y)[0].numero));
                x.numeros = tmp2;
              }

              // Composer l'adresse de facturation
              x.adresse_facturation_ = "";
              if (x.client_premiere_ligne !== null) {
                // Cas hoirie, PPE ou personne représentée (par)
                x.adresse_facturation_ = [
                  x.client_premiere_ligne,
                  x.client_entreprise !== null?
                    ["Par " + x.client_entreprise, x.client_complement !== null? x.complement:
                      [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" ")].filter(Boolean).join(", "):
                    "Par " + [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                  x.client_co,
                  x.client_adresse,
                  x.client_case_postale,
                  [x.client_npa, x.client_localite].filter(Boolean).join(" ")
                ].filter(Boolean).join(", ");
              } else if (x.client_co_id !== null) {
                // Cas envoi adresse différente de celle du débiteur
                x.adresse_facturation_ = [
                  [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                  ["c/o", x.client_co_titre, x.client_co_nom, x.client_co_prenom].filter(Boolean).join(" "),
                  x.client_co_co,
                  x.client_co_adresse,
                  x.client_co_case_postale,
                  [x.client_co_npa, x.client_co_localite].filter(Boolean).join(" ")
                ].filter(Boolean).join(", ");
              } else {
                // Cas adresse facturation = adresse débiteur
                x.adresse_facturation_ = [
                  x.client_entreprise,
                  x.client_complement? x.client_complement: [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                  x.client_co,
                  x.client_adresse,
                  x.client_case_postale,
                  [x.client_npa, x.client_localite].filter(Boolean).join(" ")
                ].filter(Boolean).join(", ");
              }

              
              x.client_ = [
                x.client_entreprise,
                x.client_complement,
                [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                x.client_co,
                x.client_adresse,
                x.client_case_postale,
                [x.client_npa, x.client_localite].filter(Boolean).join(" ")
              ].filter(Boolean).join(", ");
              
              x.client_co_ = [
                [x.client_co_titre, x.client_co_nom, x.client_co_prenom].filter(Boolean).join(" "),
                x.client_co_entreprise,
                x.client_co_co,
                x.client_co_adresse,
                x.client_co_case_postale,
                [x.client_co_npa, x.client_co_localite].filter(Boolean).join(" ")
              ].filter(Boolean).join(", ");
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
            this.clients_liste = stringifyAutocomplete(response.data, "adresse_");
            this.clients_liste_type = response.data.map(x => ({
              id: x.id,
              type_id: x.type_client
            }));
          }
        })
    },

    /**
     * Crée la liste de sélection du client lors de la création de facture
     */
    getClientSearch(term) {
      this.clients_liste_select = filterList(this.clients_liste, term, 3)
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
    openFactureEdition(data) {
      let tmp = this.affaire_factures.filter(x => x.id === data.id).pop();
      this.show_co = tmp.client_co_id !== null? true: false;
      this.selectedFacture = {
        id: tmp.id,
        sap: tmp.sap,
        date: tmp.date !== null? tmp.date: moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        client: this.clients_liste.filter(x => x.id === data.client_id).pop(),
        client_: tmp.client_,
        client_co: data.client_co_id? this.clients_liste.filter(x => x.id === data.client_co_id).pop(): null,
        client_complement: tmp.client_complement,
        client_premiere_ligne: tmp.client_premiere_ligne,
        montant_mo: numeral(tmp.montant_mo).format('0.00'),
        montant_mat_diff: numeral(tmp.montant_mat_diff).format('0.00'),
        montant_rf: numeral(tmp.montant_rf).format('0.00'),
        montant_tva: numeral(tmp.montant_tva).format('0.00'),
        montant_total: numeral(tmp.montant_total).format('0.00'),
        numeros: tmp.numeros,
        remarque: tmp.remarque,
      }
      this.showFactureDialog = true;
    },

    /**
     * Créer une nouvelle facture
     */
    newFacture(facture_type) {
      this.selectedFacture = {
        id: null,
        sap: null,
        date: getCurrentDate(),
        client: null,
        client_co: null,
        client_complement: null,
        client_premiere_ligne: null,
        montant_mo: numeral(0).format('0.00'),
        montant_mat_diff: numeral(0).format('0.00'),
        montant_rf: numeral(0).format('0.00'),
        montant_tva: numeral(0).format('0.00'),
        montant_total: numeral(0).format('0.00'),
        numeros: null,
        remarque: null
      };
      
      if (facture_type === 'devis') {
        this.selectedFacture.type_id = this.configFactureTypeID.devis;
      } else if (facture_type === 'facture') {
        this.selectedFacture.type_id = this.configFactureTypeID.facture;
      }
      
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
      formData.append("affaire_id", this.$route.params.id);
      formData.append("id", this.selectedFacture.id);
      formData.append("sap", this.selectedFacture.sap || null);
      formData.append("remarque", this.selectedFacture.remarque || null);
      formData.append("client_complement", this.selectedFacture.client_complement || null);
      formData.append("client_premiere_ligne", this.selectedFacture.client_premiere_ligne || null);
      
      if (this.selectedFacture.type_id) {
        formData.append("type_id", this.selectedFacture.type_id);
      }
      if (this.selectedFacture.date) {
        formData.append("date", moment(this.selectedFacture.date, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }
      if (this.selectedFacture.client.id) {
        formData.append("client_id", this.selectedFacture.client.id);
      }
      
      if (this.selectedFacture.client_co !== null && this.selectedFacture.client_co.id) {
        formData.append("client_co_id", this.selectedFacture.client_co.id);
      } else {
        formData.append("client_co_id", null);
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
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_FACTURE_ID), "Édition de " + facture_type);

            this.searchAffaireFactures();
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
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_FACTURE_ID), "Suppression");

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
     * Affiche le complément client si le client est une entreprise
     */
    showClientComplement(client) {
      if (client && client.id) {
        let tmp = this.clients_liste_type.filter(x => x.id === client.id).pop();
        if (tmp.type_id === this.clients_types_config.personne_morale) {
          return true;
        }
      }
      return false;
    },

    /**
     * Generate documents cadastration
     */
    generateDocuments(facture) {
      this.generateLettreProprietaire(facture);
      this.generateReqRF();
    },

    /**
     * Générer lettre propriétaire (Cadastration)
     */
    async generateLettreProprietaire(facture) {
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
        "VREF": "__A_MODIFIER__",
        "DATE_ENVOI": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        "TITRE": facture.client_titre,
        "BIEN_FONDS": "__A_MODIFIER__",
        "CADASTRE": this.affaire.cadastre,
        "NO_NOTE_FRAIS": facture.sap,
        "MONTANT": facture.montant_total
      }));

      return formData;
    },

    /**
     * Générer réquisition pour le RF (Cadastration)
     */
    async generateReqRF() {
      let formData = this.fillDataReqRF();
      getDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le fichier '" + response + "' se trouve dans le dossier 'Téléchargement'")
      }).catch(err => handleException(err, this));
    },

    /**
     * Remplir le formulaire pour la requisition au RF (cadastration)
     */
    fillDataReqRF() {
      let formData = new FormData();
      formData.append("template", "ReqCad");
      formData.append("values", JSON.stringify({
        "ANNEE": new Date().getFullYear(),
        "DATE_PLAN_ORIGINE": "JJ.MM.AAAA",
        "DATE_PLAN_CADASTRATION": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        "BIEN_FONDS": "__A_MODIFIER__",
        "CADASTRE": this.affaire.cadastre,
        "DATE": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
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
    }
  },

  mounted: function() {
    this.searchClients();
    this.searchAffaireNumeros().then(() => {
      this.searchAffaireFactures();
    });

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



