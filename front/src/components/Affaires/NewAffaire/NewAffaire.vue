<style src="./newAffaire.css" scoped></style>
<template src="./newAffaire.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import { validationMixin } from "vuelidate";
import { handleException } from "@/services/exceptionsHandler";
import { required } from "vuelidate/lib/validators";
import { getCurrentDate } from "@/services/helper";
import Autocomplete from "vuejs-auto-complete";

const moment = require("moment");

export default {
  name: "NewAffaire",
  mixins: [validationMixin],
  props: {},
  components: {
    MapHandler,
    Autocomplete
  },
  data: () => {
    return {
      types_affaires_list: [],
      clients_list: [],
      search_clients_list: [],
      operateurs_list: [],
      cadastres_list: [],
      // affaires_list: [],
      sitn_search_categories: null,
      client_envoi: null,
      client_envoi_complement: null,
      client_facture: null,
      client_facture_complement: null,
      form: {
        nom: null,
        client_commande: null,
        client_commande_complement: null,
        technicien_id: null,
        type_id: null,
        cadastre_id: null,
        date_ouverture: getCurrentDate(),
        date_validation: null,
        date_cloture: null,
        localisation_E: null,
        localisation_N: null,
        localisation: null,
        vref: null,
        affaire_base: null,
        remarque: null,
        affaire_base_id: null,
        affaire_modif_type: null
      },
      dataSaved: false,
      sending: false,
      lastRecord: null,
      type_modification_bool: false,
      typesModficiationAffaire_list: []
    };
  },

  // Validations
  validations: {
    form: {
      type_id: {
        required
      },
      client_commande: {
        required
      },
      technicien_id: {
        required
      },
      cadastre_id: {
        required
      },
      date_ouverture: {
        required
      },
      localisation: {
        required
      }
    },

    client_envoi: {
      id: {
        required
      }
    },

    client_facture: {
      id: {
        required
      }
    }
  },

  methods: {
    /**
     * Get validation class par fieldname pour objet form
     */
    getValidationClass(field) {
      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    },

    /**
     * Init map
     */
    callInitMap: function() {
      var defaultCenter = JSON.parse(process.env.VUE_APP_MAP_DEFAULT_CENTER);
      this.$refs.mapHandler.initMap(
        defaultCenter,
        process.env.VUE_APP_MAP_DEFAULT_ZOOM
      );
      this.$refs.mapHandler.map.on("singleclick", this.onMapClick(this));
    },

    /**
     * Handle map click event
     */
    onMapClick: function(_this) {
      return function(evt) {
        _this.$refs.mapHandler.clearMarkers();
        if (evt.coordinate) {
          _this.form.localisation_E = evt.coordinate[0];
          _this.form.localisation_N = evt.coordinate[1];
          _this.form.localisation = [
            Math.round(_this.form.localisation_E),
            Math.round(_this.form.localisation_N)
          ].join(" / ");
          _this.$refs.mapHandler.addMarker(
            _this.form.localisation_E,
            _this.form.localisation_N
          );
        }
      };
    },

    /*
     * Init types affaires list
     */
    async initTypesAffairesList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.types_affaires_list = response.data;
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init clients list
     */
    async initClientsList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            var tmp = response.data;
            tmp.forEach(x => {
              x.nom_ = [
                x.entreprise,
                [x.nom, x.prenom].filter(Boolean).join(" "),
                x.adresse,
                [x.npa, x.localite].filter(Boolean).join(" ")
              ]
                .filter(Boolean)
                .join(", ");
            });

            this.clients_list = tmp.map(x => ({
              id: x.id,
              nom: x.nom_,
              toLowerCase: () => x.nom_.toLowerCase(),
              toString: () => x.nom_
            }));
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init operateurs list
     */
    async initOperateursList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            var tmp = response.data.map(x => ({
              id: x.id,
              nom: [x.prenom, x.nom].join(" "),
              responsable: x.responsable,
              toLowerCase: () => [x.prenom, x.nom].join(" ").toLowerCase(),
              toString: () => [x.prenom, x.nom].join(" ")
            }));
            this.operateurs_list = tmp;
            this.form.technicien_id = JSON.parse(
              localStorage.getItem("infolica_user")
            ).id;
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init cadastres list
     */
    async initCadastresList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.cadastres_list = response.data;
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Search Client par after 3 letters
     */
    searchClients(value) {
      let tmp = [];
      if (value !== null) {
        if (value.length >= 3) {
          tmp = this.clients_list.filter(x =>
            x.nom.toLowerCase().includes(value.toLowerCase())
          );
        }
      }
      this.search_clients_list = tmp;
    },

    /**
     * Save data
     */
    saveData() {
      this.sending = true;
      var formData = this.initPostData();

      var url =
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT;

      this.$http
        .post(url, formData, {
          withCredentials: true,
          headers: { Accept: "application/json" }
        })
        .then(response => {
          const _response = response;
          if (response && response.data) {

            var promises = [];
            // Enregistrer une facture vide
            promises.push(this.postFacture(_response.data));
            if (this.form.remarque !== null) promises.push(this.postRemarqueAffaire(_response.data));
            if (this.type_modification_bool) promises.push(this.postAffaireRelation(_response.data));

            Promise.all(promises)
            .then(() => {
              this.handleSaveDataSuccess(_response);
              this.$router.push({
                name: "AffairesDashboard",
                params: { id: _response.data }
              });
                
            }).catch(err => {
                handleException(err, this);
                this.sending = false;
              });
              
          }
        })
        //Error
        .catch(err => {
          this.sending = false;
          handleException(err, this);
        });
    },

    /**
     * Enregistre une facture vide avec l'adresse
     */
    postFacture(affaire_id) {
      return new Promise((resolve, reject) => {
        var formData = new FormData();
        formData.append("affaire_id", affaire_id);
        formData.append("client_id", this.client_facture.id);
        formData.append(
          "client_complement",
          this.client_facture_complement
        );

        this.$http
          .post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: { Accept: "applicatoin/json" }
            }
          )
          .then(response => {
            if (response && response.data) {
              this.$root.$emit(
                "ShowMessage",
                "Une facture a correctement été créée dans l'affaire"
              );
              resolve(response);
            }
          })
          .catch(err => reject(err));
      });
    },

    /**
     * Post affaires relation si affaire de type modification
     */
    postAffaireRelation(affaire_id) {
      var formData = new FormData();
      formData.append('affaire_id_mere', this.form.affaire_base_id);
      formData.append('affaire_id_fille', affaire_id);
      formData.append('type_id', this.form.affaire_modif_type.id);
      formData.append("date", moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_MODIFICATION_AFFAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * Post remarque affaire si remarque spécifiée
     */
    postRemarqueAffaire(affaire_id) {
      var formData = new FormData();
      formData.append("affaire_id", affaire_id);
      formData.append("remarque", this.form.remarque);
      formData.append("operateur_id", this.form.technicien_id);
      formData.append("date", moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_REMARQUES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },  

    /**
     * Handle save data success
     */
    initPostData() {
      var formData = new FormData();
      formData.append("type_id", this.form.type_id);

      if (this.form.nom) formData.append("nom", this.form.nom);
      if (this.form.client_commande)
        formData.append("client_commande_id", this.form.client_commande.id);
      if (this.form.client_commande_complement)
        formData.append(
          "client_commande_complement",
          this.form.client_commande_complement.id
        );
      if (this.client_envoi)
        formData.append("client_envoi_id", this.client_envoi.id);
      if (this.form.client_envoi_complement)
        formData.append(
          "client_envoi_complement",
          this.form.client_envoi_complement.id
        );
      if (this.form.technicien_id)
        formData.append("technicien_id", this.form.technicien_id);
      if (this.form.cadastre_id)
        formData.append("cadastre_id", this.form.cadastre_id);
      if (this.form.localisation_E)
        formData.append("localisation_E", this.form.localisation_E);
      if (this.form.localisation_N)
        formData.append("localisation_N", this.form.localisation_N);
      if (this.form.vref) formData.append("vref", this.form.vref);
      if (this.form.date_ouverture)
        formData.append(
          "date_ouverture",
          moment(
            this.form.date_ouverture,
            process.env.VUE_APP_DATEFORMAT_CLIENT
          ).format(process.env.VUE_APP_DATEFORMAT_WS)
        );
      if (this.form.date_validation)
        formData.append(
          "date_validation",
          moment(
            this.form.date_validation,
            process.env.VUE_APP_DATEFORMAT_CLIENT
          ).format(process.env.VUE_APP_DATEFORMAT_WS)
        );
      if (this.form.date_cloture)
        formData.append(
          "date_cloture",
          moment(
            this.form.date_cloture,
            process.env.VUE_APP_DATEFORMAT_CLIENT
          ).format(process.env.VUE_APP_DATEFORMAT_WS)
        );

      return formData;
    },

    /**
     * Handle save data success
     */
    handleSaveDataSuccess(response) {
      if (response && response.data) {
        this.lastRecord = `${this.form.nom}`;
        this.dataSaved = true;
        this.sending = false;
        this.clearForm();
      }
    },

    /**
     * Validate form
     */
    validateForm() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.saveData();
      }
    },

    /**
     * Cancel edit
     */
    cancelEdit() {
      this.$router.push({ name: "Affaires" });
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.$v.$reset();
      this.form.nom = null;
      this.form.nomclient_commande = { id: null, nom: null };
      this.form.nomclient_commande_complement = null;
      this.form.nomtechnicien_id = null;
      this.form.nomtype_id = null;
      this.form.nomcadastre_id = null;
      this.form.nomdate_ouverture = getCurrentDate(),
      this.form.nomdate_validation = null;
      this.form.nomdate_cloture = null;
      this.form.nomlocalisation_E = null;
      this.form.nomlocalisation_N = null;
      this.form.nomlocalisation = null;
      this.form.nomvref = null;
      this.client_envoi = null;
      this.client_envoi_complement = null;
      this.client_facture = null;
      this.client_facture_complement = null;
    },

    /**
     * User SITN search service
     */
    async doSearchSITN(input) {
      let result = await this.$http
        .get(process.env.VUE_APP_SITN_SEARCH_SERVICE_URL + input)
        .then(response => {
          return response;
        })
        //Error
        .catch(err => {
          this.sending = false;
          console.error(err);
        });
      return result;
    },

    /**
     * Search SITN endpoint
     */
    searchSITNEndpoint(input) {
      let cadastre = this.cadastres_list.filter(
        x => x.id === this.form.cadastre_id
      )[0].nom;
      return (
        process.env.VUE_APP_SITN_SEARCH_SERVICE_URL +
        [input, cadastre, "egrid"].filter(Boolean).join(" ")
      );
    },

    /**
     * Handle SITN search item
     */
    handleSelectSITNItem(feature) {
      if (
        feature &&
        feature.selectedObject &&
        feature.selectedObject.geometry
      ) {
        this.$refs.mapHandler.addGraphic(feature.selectedObject);
      }

      // access the autocomplete component methods from the parent
      this.$refs.autocomplete.clear();
    },

    /**
     * Handle display format
     */
    formattedDisplay(result) {
      return result.properties.label;
    },

    /**
     * Handle SITN search results
    
    handleSITNSearchResults (results) {
      console.log(results);
      document.getElementsByClassName('autocomplete__results')[0].innerHTML = "Tessssst";
    },*/

    /**
     * Complète par défaut les clients envoi et facture
     */
    defaultCompleteClients(client) {
      this.client_envoi = client;
      this.client_facture = client;
    },

    /**
     * openCreateClient
     */
    openCreateClient() {
      let routedata = this.$router.resolve({ name: "ClientsNew" });
      window.open(routedata.href, "_blank");
    },

    // /**
    //  * Get affaires
    //  */
    // async initAffaires() {
    //   this.$http.get(
    //     process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
    //     {
    //       withCredentials: true,
    //       headers: {Accept: "application/json"}
    //     }
    //   ).then(response => {
    //     if (response && response.data) {
    //       let tmp = response.data;
    //       tmp.filter(x => {
    //         x.date_cloture === null && x.cadastre_id === this.form.cadastre_id;
    //       })
    //       .map(x => ({
    //         id: x.id,
    //         nom: [x.id, x.no_access].filter(Boolean).join(" ")
    //       }))
    //       .map(x => ({
    //         id: x.id,
    //         nom: x.nom,
    //         toLowerCase: () => x.nom.toLowerCase(),
    //         toString: () => x.nom.toString()
    //       }));
    //       this.affaires_list = tmp;
    //     }
    //   }).catch(err => handleException(err, this));
    // },

    /**
     * On Select Type affaire
     */
    onSelectType() {
      if (this.form.type_id === Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIFICATION)){
        this.type_modification_bool = true;
      } else {
        this.type_modification_bool = false;
      }
    },

    /**
     * get Types de modifications d'affaire
     */
    async initTypesModficiationAffaire() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TYPES_MODIF_AFFAIRE_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.typesModficiationAffaire_list = response.data.map(x => ({
            id: x.id,
            nom: x.nom,
            toLowerCase: () => x.nom.toLowerCase(),
            toString: () => x.nom.toString()
          }));
        }
      }).catch(err => handleException(err, this));
    }

  },

  mounted: function() {
    //Init search SITN categories
    this.sitn_search_categories = JSON.parse(
      process.env.VUE_APP_SITN_SEARCH_CATEGORIES_ALIASES
    );

    //Init map component
    this.callInitMap();

    //Init lists
    this.initTypesAffairesList();
    this.initClientsList();
    this.initOperateursList();
    this.initCadastresList();
    // this.initAffaires();
    this.initTypesModficiationAffaire();
  }
};
</script>



