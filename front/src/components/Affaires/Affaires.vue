<style src="./affaires.css" scoped></style>
<template src="./affaires.html"></template>


<script>
import {
  getCadastres,
  getTypesAffaires,
  getClients,
  getEtapesAffaire,
  getOperateurs,
  filterList,
  stringifyAutocomplete,
  stringifyAutocomplete2,
  checkPermission,
  adjustColumnWidths
} from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler';

const moment = require('moment');

export default {
  name: "Affaires",
  props: {},
  data: () => ({
    affaires: [],
    clients: [],
    operateurs_liste: [],
    cadastre_liste: [],
    etapes_liste: [],
    newAffaireAllowed: false,
    search: {
      id: null,
      nom: null,
      cadastre: "",
      type: "",
      client: null,
      operateur: null,
      dateFrom: null,
      dateTo: null,
      etape: null,
      limitNbResults: true,
    },
    searchClientsListe: [],
    types_affaires: []
  }),

  methods: {

    /*
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init Types affaires list
     */
    async initTypesAffairesList() {
      getTypesAffaires()
        .then(response => {
          if (response && response.data) {
            this.types_affaires = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },
   
    /**
     * init clients liste
     */
    async initClientsListe() {
      getClients()
      .then(response => {
        if (response && response.data) {
          this.clients = stringifyAutocomplete(response.data, "adresse_");
        }
      }).catch(err => handleException(err, this));
    },
   
    /**
     * init operateurs liste
     */
    async initOperateursListe() {
      getOperateurs()
      .then(response => {
        if (response && response.data) {
          this.operateurs_liste = stringifyAutocomplete2(response.data, ["prenom", "nom"], " ");
        }
      }).catch(err => handleException(err, this));
    },
   
    /**
     * init operateurs liste
     */
    async initEtapesListe() {
      getEtapesAffaire()
      .then(response => {
        if (response && response.data) {
          this.etapes_liste = stringifyAutocomplete2(response.data);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * filter clients liste by search term
     */
    filterClients(searchTerm) {
      if (searchTerm && typeof searchTerm === "string") {
        this.searchClientsListe = filterList(this.clients, searchTerm, 3).slice(0,20);
      } else {
        this.searchClientsListe = [null];
      }
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.search.id = null;
      this.search.nom = null;
      this.search.cadastre = "";
      this.search.type = "";
      this.search.client = null;
      this.search.operateur = null;
      this.search.dateFrom = null;
      this.search.dateTo = null;
      this.search.etape = null;
      this.search.limitNbResults = true;
    },
    
    /*
     * SEARCH AFFAIRE
     */
    async searchAffaires() {
      let formData = new FormData();

      formData.append("limitNbResults", this.search.limitNbResults);

      if (this.search.id) {
        formData.append("id", this.search.id);
      }
      
      if (this.search.nom) {
        formData.append("no_access", this.search.nom);
      }
      
      if (this.search.cadastre) {
        formData.append("cadastre", this.search.cadastre);
      }
      
      if (this.search.type) {
        formData.append("type_affaire", this.search.type);
      }
      
      if (this.search.client && this.search.client.id !== null) {
        formData.append("client_id", this.search.client.id);
      }

      if (this.search.operateur && this.search.operateur.id !== null) {
        formData.append("technicien_id", this.search.operateur.id);
      }

      if (this.search.etape && this.search.etape.id !== null) {
        formData.append("etape_id", this.search.etape.id);
      }

      if (this.search.dateFrom) {
        formData.append("date_from", moment(this.search.dateFrom, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }

      if (this.search.dateTo) {
        formData.append("date_to", moment(this.search.dateTo, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RECHERCHE_AFFAIRES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            let tmp = response.data;
            tmp.forEach(x => {
              if (x.client_commande_id) {
                x.client_commande_ = x.client_commande_entreprise? x.client_commande_entreprise: [x.client_commande_titre, x.client_commande_prenom, x.client_commande_nom].filter(Boolean).join(" ");
              }
              if (x.client_envoi_id) {
                x.client_envoi_ = x.client_envoi_entreprise? x.client_envoi_entreprise: [x.client_envoi_titre, x.client_envoi_prenom, x.client_envoi_nom].filter(Boolean).join(" ");
              }
              if (x.client_facture.length > 0) {
                let tmp_ = [];
                for (const cf of x.client_facture) {
                  tmp_.push(cf.entreprise? cf.entreprise: [cf.titre, cf.prenom, cf.nom].filter(Boolean).join(" "));
                }
                x.client_facture_ = tmp_.filter(Boolean).join(', ');
              }
            });

            this.affaires = tmp;
          }
        }).catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenAffaire(id) {
      this.$router.push({ name: "AffairesDashboard", params: {id}});
    },

    /**
     * Set permissions
     */
    setPermissions() {
      this.newAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PPE_EDITION) ||
                               checkPermission(process.env.VUE_APP_AFFAIRE_REVISION_ABORNEMENT_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_CADASTRATION_EDITION) ||
                               checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PCOP_EDITION) ||
                               checkPermission(process.env.VUE_APP_AFFAIRE_AUTRE_EDITION);
    },

    disabledStartDates (date) {
      if (this.search.dateTo && moment(this.search.dateTo, process.env.VUE_APP_DATEFORMAT_CLIENT)) {
        return date > moment(this.search.dateTo, process.env.VUE_APP_DATEFORMAT_CLIENT) || date > new Date();
      }
      if (date > new Date()) {
        return true;
      }
      return false;
    },

    disabledEndDates (date) {
      if (this.search.dateFrom && moment(this.search.dateFrom, process.env.VUE_APP_DATEFORMAT_CLIENT)) {
        return date < moment(this.search.dateFrom, process.env.VUE_APP_DATEFORMAT_CLIENT) || date > new Date();
      }
      if (date > new Date()) {
        return true;
      }
      return false;
    },

  },

  mounted: function() {
    this.initCadastresList();
    this.initTypesAffairesList();
    this.searchAffaires();
    this.initClientsListe();
    this.initOperateursListe();
    this.initEtapesListe();
    this.setPermissions();
    adjustColumnWidths();
  }
};
</script>



