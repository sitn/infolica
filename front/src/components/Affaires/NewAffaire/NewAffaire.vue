<style src="./newAffaire.css" scoped></style>
<template src="./newAffaire.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import { validationMixin } from "vuelidate";
import { handleException } from "@/services/exceptionsHandler";
import { required } from "vuelidate/lib/validators";
import { getCurrentDate } from "@/services/helper";

const moment = require("moment");

export default {
  name: "NewAffaire",
  mixins: [validationMixin],
  props: {},
  components: {
    MapHandler
  },
  data: () => {
    return {
      types_affaires_list: [],
      clients_list: [],
      search_clients_list: [],
      operateurs_list: [],
      responsables_list: [],
      cadastres_list: [],

      form: {
        nom: null,
        client_commande_id: null,
        client_commande_par_id: null,
        responsable_id: null,
        technicien_id: null,
        type_id: null,
        cadastre_id: null,
        information: null,
        date_ouverture: getCurrentDate(),
        date_validation: null,
        date_cloture: null,
        localisation_E: null,
        localisation_N: null,
        vref: null
      },
      dataSaved: false,
      sending: false,
      lastRecord: null
    };
  },

  // Validations
  validations: {
    form: {
      type_id: {
        required
      },
      client_commande_id: {
        required
      },
      responsable_id: {
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
      localisation_E: {
        required
      },
      localisation_N: {
        required
      }
    }
  },

  methods: {
    /**
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      const field = this.$v.form[fieldName];

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
    initTypesAffairesList() {
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
    initClientsList() {
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
            this.clients_list = response.data.map(x => ({
              id: x.id,
              nom: x.entreprise ? x.entreprise : x.nom + " " + x.prenom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
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
    initOperateursList() {
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
            this.responsables_list = tmp.filter(x => x.responsable);
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
    initCadastresList() {
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
          this.handleSaveDataSuccess(response);
          this.$router.push("/affaires/" + response.data);
        })
        //Error
        .catch(err => {
          this.sending = false;
          handleException(err, this);
        });
    },

    /**
     * Handle save data success
     */
    initPostData() {
      var formData = new FormData();
      formData.append("type_id", this.form.type_id);

      if (this.form.nom) formData.append("nom", this.form.nom);
      if (this.form.client_commande_id)
        formData.append("client_commande_id", this.form.client_commande_id.id);
      if (this.form.client_commande_par_id)
        formData.append(
          "client_commande_par_id",
          this.form.client_commande_par_id.id
        );
      if (this.form.responsable_id)
        formData.append("responsable_id", this.form.responsable_id);
      if (this.form.technicien_id)
        formData.append("technicien_id", this.form.technicien_id);
      if (this.form.cadastre_id)
        formData.append("cadastre_id", this.form.cadastre_id);
      if (this.form.information)
        formData.append("information", this.form.information);
      if (this.form.localisation_E)
        formData.append("localisation_E", this.form.localisation_E);
      if (this.form.localisation_N)
        formData.append("localisation_N", this.form.localisation_N);
      if (this.form.vref) formData.append("vref", this.form.vref);
      if (this.form.date_ouverture)
        formData.append(
          "date_ouverture",
          moment(new Date(new Date(this.form.date_ouverture))).format(
            "YYYY-MM-DD"
          )
        );
      if (this.form.date_validation)
        formData.append(
          "date_validation",
          moment(new Date(new Date(this.form.date_validation))).format(
            "YYYY-MM-DD"
          )
        );
      if (this.form.date_cloture)
        formData.append(
          "date_cloture",
          moment(new Date(new Date(this.form.date_cloture))).format(
            "YYYY-MM-DD"
          )
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
      this.$router.push("/affaires");
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.$v.$reset();
      this.form.nom = null;
      this.form.nomclient_commande_id = null;
      this.form.nomclient_commande_par_id = null;
      this.form.nomresponsable_id = null;
      this.form.nomtechnicien_id = null;
      this.form.nomtype_id = null;
      this.form.nomcadastre_id = null;
      this.form.nominformation = null;
      this.form.nomdate_ouverture = getCurrentDate();
      this.form.nomdate_validation = null;
      this.form.nomdate_cloture = null;
      this.form.nomlocalisation_E = null;
      this.form.nomlocalisation_N = null;
      this.form.nomvref = null;
    }
  },

  mounted: function() {
    //Init map component
    this.callInitMap();

    //Init lists
    this.initTypesAffairesList();
    this.initClientsList();
    this.initOperateursList();
    this.initCadastresList();
  }
};
</script>



