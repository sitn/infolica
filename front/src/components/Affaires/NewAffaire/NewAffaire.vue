<style src="./newAffaire.css" scoped></style>
<template src="./newAffaire.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import { validationMixin } from "vuelidate";
import { handleException } from "@/services/exceptionsHandler";
import { required } from "vuelidate/lib/validators";
import { getCurrentDate,
         getClients,
         filterList,
         stringifyAutocomplete,
         checkPermission,
         getCurrentUserRoleId } from "@/services/helper";
import Autocomplete from "vuejs-auto-complete";
import ReferenceNumeros from "@/components/Affaires/NumerosAffaire/ReferenceNumeros/ReferenceNumeros.vue";

const moment = require("moment");

export default {
  name: "NewAffaire",
  mixins: [validationMixin],
  props: {},
  components: {
    Autocomplete,
    MapHandler,
    ReferenceNumeros
  },
  data: () => {
    return {
      affaire_numeros_anciens: [],
      affaire_numeros_nouveaux: [],
      cadastres_list: [],
      client_facture: null,
      client_facture_complement: null,
      client_facture_premiere_ligne: null,
      clients_list: [],
      clients_liste_type: [],
      client_moral_personnes: {
        commande: [],
        envoi: [],
        facture: []
      },
      clients_types_config: {
        personne_morale: Number(process.env.VUE_APP_TYPE_CLIENT_MORAL_ID),
        personne_physique: Number(process.env.VUE_APP_TYPE_CLIENT_PHYSIQUE_ID)
      },
      dataSaved: false,
      form: {
        affaire_base: null,
        affaire_base_id: null,
        affaire_modif_type: null,
        cadastre: {
            id: null,
            nom: "",
            toString: () => "",
            toLowerCase: () => ""
          },
        client_commande: null,
        client_commande_complement: null,
        client_envoi: null,
        client_envoi_complement: null,
        date_cloture: null,
        date_ouverture: moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        date_validation: null,
        localisation: null,
        localisation_E: null,
        localisation_N: null,
        nom: null,
        plan: null,
        information: null,
        technicien_id: JSON.parse(localStorage.getItem("infolica_user")).id,
        type: null,
        vref: null
      },
      lastRecord: null,
      numerosReferences: [],
      operateurs_list: [],
      permission: {
        editClientAllowed: false
      },
      plansMOListe: [],
      plansMOListe_cadastre: [],
      search_clients_list: [],
      selectedAnciensNumeros: [],
      selectedModificationAffaire: null,
      selectedNouveauxNumeros: [],
      sending: false,
      showClientsForm: true,
      showReferenceNumeros: false,
      sitn_search_categories: null,
      types_affaires_list_bk: [],
      types_affaires_list: [],
      type_modification_bool: false,
      typesModficiationAffaire_list: [],
      typesModficiationAffaire_list_bk: [],

      typesAffaires_conf: {
        mutation: Number(process.env.VUE_APP_TYPE_AFFAIRE_DIVISION),
        cadastration: Number(process.env.VUE_APP_TYPE_AFFAIRE_CADASTRATION),
        ppe: Number(process.env.VUE_APP_TYPE_AFFAIRE_PPE),
        pcop: Number(process.env.VUE_APP_TYPE_AFFAIRE_PCOP),
        mpd: Number(process.env.VUE_APP_TYPE_AFFAIRE_MPD),
        art35: Number(process.env.VUE_APP_TYPE_AFFAIRE_ART35),
        mat_diff: Number(process.env.VUE_APP_TYPE_AFFAIRE_MAT_DIFF),
        modification: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIFICATION),
        revision_abornement: Number(process.env.VUE_APP_TYPE_AFFAIRE_REVISION_ABORNEMENT),
        remaniement_parcellaire: Number(process.env.VUE_APP_TYPE_AFFAIRE_REMANIEMENT_PARCELLAIRE),
        servitude: Number(process.env.VUE_APP_TYPE_AFFAIRE_SERVITUDE),
        retablissement_pfp3: Number(process.env.VUE_APP_TYPE_AFFAIRE_RETABLISSEMENT_PFP3),
        autre: Number(process.env.VUE_APP_TYPE_AFFAIRE_AUTRE),
        modification_visa: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_VISA),
        modification_duplicata: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_DUPLICATA),
        modification_abandon_partiel: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_ABANDON_PARTIEL),
        modification_mutation: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_MUTATION),
        modification_ppe: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_PPE),
      },
      role_conf: {
        ppe_user_id: Number(process.env.VUE_APP_PPE_ROLE_ID),
        mo_user_id: Number(process.env.VUE_APP_MO_ROLE_ID),
        secretariat_user_id: Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID)
      }
    };
  },
  // Validations
  validations() {
    let form = {};
    let client_facture = {};

    if (this.showClientsForm) {
      form = {
        type: {required},
        cadastre: {required},
        nom: {required},
        technicien_id: {required},
        date_ouverture: {required},
        localisation: {required},
        client_commande: {required},
        client_envoi: {required}
      };

      if (this.form.type && this.form.type.id && this.typesAffaires_conf.pcop !== this.form.type.id) {
        client_facture = {
          id: {required}
        };
      }

    } else {
      form = {
        type: {required},
        cadastre: {required},
        nom: {required},
        technicien_id: {required},
        date_ouverture: {required},
        localisation: {required}
      };
    }

    if (this.type_modification_bool) {
      form.affaire_modif_type = {required}  
    }

    return {form, client_facture}
  },

  methods: {
    /**
     * Init mask (what is shown or not)
     */
    initMask() {
      // empty numerosReferences array
      this.numerosReferences = [];

      if (this.form.type && this.form.type.id) {
        this.showReferenceNumeros = [
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.pcop,
          this.typesAffaires_conf.mat_diff,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.servitude,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.modification_abandon_partiel
        ].includes(this.form.type.id)
      } else {
        this.showReferenceNumeros = false;
      }
    },

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
      this.$refs.mapHandler.modify.on("modifyend", this.onFeatureChange(this));
    },

    /**
     * Handle map feature change event
     */
    onFeatureChange: function(_this) {
      return function(modify) {
        const features = modify.features.getArray();
        if (features) {
          const feature = features[0];
          const coordinates = feature.getGeometry().getCoordinates();
          _this.form.localisation_E = coordinates[0];
          _this.form.localisation_N = coordinates[1];
          _this.handleLocalisation(_this.form.localisation_E, _this.form.localisation_N);
        }
      };
    },

    /**
     * Handle map click event
     */
    onMapClick: function(_this) {
      return function(evt) {
        if (evt.coordinate) {
          _this.form.localisation_E = evt.coordinate[0];
          _this.form.localisation_N = evt.coordinate[1];
          _this.handleLocalisation(_this.form.localisation_E, _this.form.localisation_N);
        }
      };
    },

    /**
     * Handle localisation
     */
    handleLocalisation: function(localisation_E, localisation_N, zoom) {
      this.$refs.mapHandler.clearMarkers();
      this.form.localisation = [
        Math.round(localisation_E),
        Math.round(localisation_N)
      ].join(" / ");
      this.$refs.mapHandler.addMarker(
        localisation_E,
        localisation_N,
        zoom
      );
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
            let tmp = response.data.filter(x => x.ordre < Number(process.env.VUE_APP_AFFAIRE_MODIF_THR));
            let type_filter = [];
            // Only suggest affaire types to which user has rights
            let userRoleID = getCurrentUserRoleId()
            if (userRoleID && [this.role_conf.secretariat_user_id, this.role_conf.mo_user_id, this.role_conf.ppe_user_id].includes(userRoleID)) {
              if (checkPermission(process.env.VUE_APP_AFFAIRE_PPE_EDITION)) {
                type_filter.push(this.typesAffaires_conf.ppe);
                type_filter.push(this.typesAffaires_conf.modification);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_REVISION_ABORNEMENT_EDITION)) {
                type_filter.push(this.typesAffaires_conf.revision_abornement);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_CADASTRATION_EDITION)) {
                type_filter.push(this.typesAffaires_conf.cadastration);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION)) {
                type_filter.push(this.typesAffaires_conf.retablissement_pfp3);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_PCOP_EDITION)) {
                type_filter.push(this.typesAffaires_conf.pcop);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_MPD_EDITION)) {
                type_filter.push(this.typesAffaires_conf.mpd);
              }
              if (checkPermission(process.env.VUE_APP_AFFAIRE_AUTRE_EDITION)) {
                type_filter.push(this.typesAffaires_conf.autre);
              }
              if (type_filter.length>0) {
                tmp = tmp.filter(x => type_filter.includes(x.id));
              }
              
            }
            this.types_affaires_list_bk = tmp;
            this.types_affaires_list = stringifyAutocomplete(tmp);
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
      getClients()
      .then(response => {
        if (response && response.data) {
          this.clients_list = stringifyAutocomplete(response.data, "adresse_");
          this.clients_liste_type = response.data.map(x => ({
            id: x.id,
            type_id: x.type_client
          }));
          
          this.updateContact();
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
            let tmp = response.data.filter(x => x.chef_equipe).map(x => ({
              id: x.id,
              nom: [x.prenom, x.nom].filter(Boolean).join(" "),
            }));
            tmp.sort((a,b) => (a.nom > b.nom) ? 1 : ((b.nom > a.nom) ? -1 : 0));
            this.operateurs_list = tmp;
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
            this.cadastres_list = stringifyAutocomplete(response.data);
          }
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Search Client after 3 letters
     */
    searchClients(value) {
      this.search_clients_list = filterList(this.clients_list, value, 3);
    },

    /**
     * Save data
     */
    saveData() {
      this.sending = true;
      let formData = this.initPostData();
      let url =
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT;
      this.$http
        .post(url, formData, {
          withCredentials: true,
          headers: { Accept: "application/json" }
        })
        .then(response => {
          const _response = response;
          const id_new_affaire = response.data;
          if (response && response.data) {
            let promises = [];
            
            // Si l'affaire est de type modification ...
            if (this.type_modification_bool) {
              promises.push(this.postAffaireRelation(id_new_affaire));
              if ((this.selectedAnciensNumeros.length + this.selectedNouveauxNumeros.length) > 0 ) {
                //désactiver la relation numéro-affaire, créer une liaison sur la nouvelle affaire et mise à jour de la relation des numéros dans la nouvelle affaire
                promises.push(this.updateNumerosAffaire(id_new_affaire));
              }
              if (this.selectedAnciensNumeros.length === this.affaire_numeros_anciens.length && this.selectedNouveauxNumeros.length === this.affaire_numeros_nouveaux.length) {
                // Si tous les numéros sont sélectionnés, clôre l'affaire de base !
                promises.push(this.cloreAffaireBase());
              }
              if (this.form.affaire_modif_type.id === this.typesAffaires_conf.modification_abandon_partiel) {
                // supprimer les bf référencés à l'affaire
                promises.push(this.abandonPartiel(id_new_affaire));
              }
            }

            // Si des numéros sont référencés à l'affaire
            if (this.numerosReferences.length>0) {
              promises.push(this.saveReferenceNumeros(id_new_affaire));
            }

            Promise.all(promises)
            .then(() => {
              this.handleSaveDataSuccess(_response);
              this.$router.push({
                name: "AffairesDashboard",
                params: { id: id_new_affaire }
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
     * Handle save data success for affaire
     */
    initPostData() {
      let formData = new FormData();
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);

      if (this.form.type.id === this.typesAffaires_conf.modification) {
        // enregistre le type d'affaire correspondant au type de modification
        let type_id = this.typesModficiationAffaire_list_bk.filter(x => x.id === this.form.affaire_modif_type.id)[0].affaire_destination_type_id;
        formData.append("type_id", type_id);
      } else {
        formData.append("type_id", this.form.type.id);
      }
      
      if (this.form.nom) {
        formData.append("nom", this.form.nom);
      }
      if (this.form.information) {
        formData.append("information", this.form.information);
      }
      if (this.form.client_commande && this.form.client_commande.id) {
        formData.append("client_commande_id", this.form.client_commande.id);
      }
      if (this.form.client_commande_complement && this.showClientComplement(this.form.client_commande)) {
        formData.append("client_commande_complement", this.form.client_commande_complement);
      }
      if (this.form.client_envoi && this.form.client_envoi.id) {
        formData.append("client_envoi_id", this.form.client_envoi.id);
      }
      if (this.form.client_envoi_complement && this.showClientComplement(this.form.client_envoi)) {
        formData.append("client_envoi_complement", this.form.client_envoi_complement);
      }
      if (this.form.technicien_id) {
        formData.append("technicien_id", this.form.technicien_id);
      }
      if (this.form.cadastre && this.form.cadastre.id) {
        formData.append("cadastre_id", this.form.cadastre.id);
      }
      if (this.form.localisation_E) {
        formData.append("localisation_E", this.form.localisation_E);
      }
      if (this.form.localisation_N) {
        formData.append("localisation_N", this.form.localisation_N);
      }
      if (this.form.vref) {
        formData.append("vref", this.form.vref);
      }
      if (this.form.date_ouverture) {
        formData.append("date_ouverture",
          moment(this.form.date_ouverture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS)
        );
      }
      if (this.form.date_validation) {
        formData.append("date_validation",
          moment(this.form.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS)
        );
      }
      if (this.form.date_cloture) {
        formData.append("date_cloture",
          moment(this.form.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS)
        );
      }
      if (this.form.plan && this.form.type && this.form.type.id && this.form.type.id === this.typesAffaires_conf.mpd) {
        formData.append("no_access", "MPD_" + this.form.cadastre.id + "_" + this.form.plan + "_" + new Date().getFullYear());
      }

      // FACTURE
      if (this.client_facture && this.client_facture.id &&
          this.form.type && this.form.type.id && this.form.type.id !== this.typesAffaires_conf.pcop){
        formData.append("facture_client_id", this.client_facture.id);
        if (this.client_facture_complement !== null) {
          formData.append("facture_client_complement", this.client_facture_complement);
        }
        if (this.client_facture_premiere_ligne !== null) {
          formData.append("facture_client_premiere_ligne", this.client_facture_premiere_ligne);
        }
      }

      return formData;
    },

    /**
     * Update numeros_affaire
     */
    updateNumerosAffaire(affaire_destination_id) {
      let promises = [];
      this.selectedAnciensNumeros.forEach(x => {
        promises.push(this.deactivateNumeroAffaires(x, affaire_destination_id));
        promises.push(this.postAffaireNumero(x, affaire_destination_id));
      });
      this.selectedNouveauxNumeros.forEach(x => {
        promises.push(this.deactivateNumeroAffaires(x, affaire_destination_id));
        promises.push(this.postAffaireNumero(x, affaire_destination_id));
        promises.push(this.updateNumeroRelation(x.numero_base_id, x.numero_id, x.affaire_id, affaire_destination_id));
      });

      Promise.all(promises)
      .then(() => this.$root.$emit("ShowMessage", "Les numéros ont bien été récupérés de l'affaire de base"))
      .catch(err => handleException(err, this));
    },

    /**
     * desactiver_numeros_affaires dans affaire base
     */
    async deactivateNumeroAffaires(affnum, affaire_destination_id) {
      let formData = new FormData();
      formData.append("id", affnum.id);
      formData.append("actif", false);
      formData.append("affaire_destination_id", affaire_destination_id);

      return new Promise ((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT,
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
     * Update numero_relation
     */
    async updateNumeroRelation(num_base_id, num_associe_id, old_affaire_id, new_affaire_id) {
      let formData = new FormData();
      formData.append("numero_id_base", num_base_id);
      formData.append("numero_id_associe", num_associe_id);
      formData.append("affaire_old_id", old_affaire_id);
      formData.append("affaire_new_id", new_affaire_id);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT,
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
     * Create new numero_affaire relation
     */
    async postAffaireNumero(affnum, affaire_destination_id) {
      var formData = new FormData();
      formData.append("affaire_id", affaire_destination_id);
      formData.append("numero_id", affnum.numero_id);
      formData.append("type_id", affnum.affaire_numero_type_id);
      formData.append("actif", true);

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT,
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
     * Affaire de modification: tous les numéros sont récupérés par l'affaire fille:
     * cloturer l'affaire de base
     */
    async cloreAffaireBase() {
      let formData = new FormData();
      formData.append("id_affaire", this.form.affaire_base_id);
      formData.append("date_cloture", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      
      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
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
     * Abandonner numeros_references à une affaire (abandon partiel)
     */
    async abandonPartiel(affaire_fille_id) {
      return new Promise((resolve, reject) => {
        let affaire_mere_id = Number(this.form.affaire_base_id);
        
        let affaire_numerosRelations = [];
        this.getNumerosRelationInAffaire(affaire_mere_id)
        .then(response => affaire_numerosRelations = response.data)
        .catch(err => handleException(err, this));

        let promises = [];
        let tmp = [];
        this.selectedAnciensNumeros.forEach(x => {
          // mise à jour de la relation affaire-numéro
          // promises.push(this.deleteNumeroAffaire(x.numero_id, affaire_mere_id));
          // mise à jour de la relation entres numéros si elle existe
          tmp = affaire_numerosRelations.filter(numrel => numrel.numero_base_id === x.numero_id && numrel.affaire_id === affaire_mere_id);
          if (tmp.length > 0) {
            promises.push(this.deleteNumeroRelation(x.numero_id, affaire_mere_id));
          }
        });
        promises.push(this.clotureAffaire(affaire_fille_id));
        
        Promise.all(promises)
        .then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

  /**
   * Get numeros relations in affaire mere
   */
  async getNumerosRelationInAffaire(affaire_id) {
    return new Promise((resolve, reject) => {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_RELATIONS_BY_AFFAIREID_ENDPOINT + affaire_id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => resolve(response))
      .catch(err => reject(err));
    });
  },

  // /**
  //  * Supprimer la relation numéro-affaire pour une affaire modif suppression partielle
  //  */
    // async deleteNumeroAffaire(numero_id, affaire_id) {
    //   return new Promise((resolve, reject) => {
    //     this.$http.delete(
    //       process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT +
    //       "?numero_id=" + numero_id + "&affaire_id=" + affaire_id,
    //       {
    //         withCredentials: true,
    //         headers: {Accept: "application/json"}
    //       }
    //     ).then(response => resolve(response))
    //     .catch(err => reject(err));
    //   });
    // },

    /**
     * Delete numero relation in case of affaire modif suppression partielle
     */
    async deleteNumeroRelation(numero_base_id, affaire_id) {
      return new Promise((resolve, reject) => {
        this.$http.delete(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT +
          "?numero_base_id=" + numero_base_id + "&affaire_id=" + affaire_id,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

    /**
     * Cloture affaire de suppression partielle
     */
    async clotureAffaire(affaire_id) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("id_affaire", affaire_id);
        formData.append("date_cloture", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
  
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
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
     * Handle save data success
     */
    handleSaveDataSuccess(response) {
      if (response && response.data) {
        this.lastRecord = `${this.form.nom}`;
        this.dataSaved = true;
        this.sending = false;
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
      let cadastre_ = null;
      if (this.form.cadastre && this.form.cadastre.id !== null) {
        cadastre_ = this.form.cadastre.nom;
        
        // only keep first part of cadastre name (problems with '-' and '/')
        cadastre_ = cadastre_.split(/[-/ ]/)[0];
      }

      return (
        process.env.VUE_APP_SITN_SEARCH_SERVICE_URL +
        [cadastre_, input, "egrid"].filter(Boolean).join(" ")
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
     * Complète par défaut les clients envoi et facture
     */
    defaultCompleteClients(client) {
      this.initClientMoralPersonnes(client.id, 'commande').then(() => {
        if (this.form.client_envoi === null || this.form.client_envoi === "") {
          this.form.client_envoi = client;
          this.client_moral_personnes.envoi = this.client_moral_personnes.commande;
        }
        if ((this.client_facture === null || this.client_facture === "") && 
             this.form.type && this.form.type.id && this.form.type.id !== this.typesAffaires_conf.pcop) {
          this.client_facture = client;
          this.client_moral_personnes.facture = this.client_moral_personnes.commande;
        }
      });
    },

    /**
     * openCreateClient
     */
    openCreateClient() {
      let routedata = this.$router.resolve({ name: "ClientsNew" });
      window.open(routedata.href, "_blank");
    },

    /**
     * On Select Type affaire
     */
    onSelectType() {
      if (this.form.type.id === Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIFICATION)){
        this.type_modification_bool = true;
      } else {
        this.type_modification_bool = false;
      }
      // this.showClientsForm = this.form.type_id === Number(process.env.VUE_APP_TYPE_AFFAIRE_CADASTRATION)? false: true;
      if (this.form.type.id === this.typesAffaires_conf.cadastration) {
        this.showClientsForm = false;
        let defaultClient = this.clients_list.filter(x => x.id === Number(process.env.VUE_APP_CLIENT_CADASTRATION_ID))[0];
        this.form.client_commande = defaultClient;
        this.form.client_envoi = defaultClient;
        this.form.client_envoi_complement = null;
        this.client_facture = null;
        this.client_facture_complement = null;
        this.client_facture_premiere_ligne = null;
        this.form.nom = "Cadastration sur "
      } else if (this.form.type.id === this.typesAffaires_conf.mpd) {
        let defaultClient = this.clients_list.filter(x => x.id === Number(process.env.VUE_APP_CLIENT_CADASTRATION_ID))[0];
        this.form.client_commande = defaultClient;
        this.form.client_envoi = defaultClient;
        this.form.client_envoi_complement = null;
        this.client_facture_premiere_ligne = null;
        this.client_facture = defaultClient;
        this.client_facture_complement = null;
        this.client_facture_premiere_ligne = null;
        this.form.nom = "Mise à jour périodique"
      } else {
        this.showClientsForm = true;
        this.form.nom = "";
        this.form.client_commande = null;
        this.form.client_envoi = null;
        this.form.client_envoi_complement = null;
        this.client_facture = null;
        this.client_facture_complement = null;
        this.client_facture_premiere_ligne = null;
      }

      this.initMask();
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
          this.typesModficiationAffaire_list_bk = response.data;
          this.typesModficiationAffaire_list = stringifyAutocomplete(response.data);
        }
      }).catch(err => handleException(err, this));
    },

    /*
     * Open affaire modification in new tab
     */
    doOpenAffaireModification() {
      const routeData = this.$router.resolve({ name: "AffairesDashboard", params: {id: this.form.affaire_base_id}});
      window.open(routeData.href, '_blank');
    },

     /**
     * Select affaire modification
     */
    doSelectAffaireModification() {
      let _this = this;
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
            this.form.affaire_base_id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
        if (response && response.data) {
          _this.selectedModificationAffaire = response.data;

          //Fill values
          this.fillValuesFromModificationAffaire();

          //Expand numéros card
          this.$refs.expandCollapseBtn.$el.click();

          //Search numéros immeubles
          _this.setModificationAffaireNuméros();
        }
        else{
          handleException({msg : "Affaire non trouvée"}, this);
        }
      })
      //Error
      .catch(err => {
        handleException(err, this);
      });
    },

    /**
     * Fill values from modification affaire
     */
    fillValuesFromModificationAffaire(){
      if(this.selectedModificationAffaire){
        let modif_type = "";
        if (this.form.affaire_modif_type !== null && this.form.affaire_modif_type.nom) {
          modif_type = this.form.affaire_modif_type.nom + " : ";
        }

        this.form.cadastre = this.cadastres_list.filter(x => x.id === this.selectedModificationAffaire.cadastre_id)[0];
        this.form.nom = modif_type + this.selectedModificationAffaire.nom;
        this.form.nom_ = this.selectedModificationAffaire.nom; // garder le nom pas modifié en mémoire
        this.form.vref = this.selectedModificationAffaire.vref;
        this.form.client_commande = this.clients_list.filter(x => x.id === this.selectedModificationAffaire.client_commande_id)[0];
        this.form.client_commande_complement = this.selectedModificationAffaire.client_commande_complement;
        this.form.client_envoi = this.clients_list.filter(x => x.id === this.selectedModificationAffaire.client_envoi_id)[0];
        this.form.client_envoi_complement = this.selectedModificationAffaire.client_envoi_complement;
        this.form.date_ouverture =  moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
        this.form.localisation_E = this.selectedModificationAffaire.localisation_e;
        this.form.localisation_N = this.selectedModificationAffaire.localisation_n;

        //Handle localisation
        if(this.selectedModificationAffaire.localisation_e && this.selectedModificationAffaire.localisation_n)
          this.handleLocalisation(this.selectedModificationAffaire.localisation_e, this.selectedModificationAffaire.localisation_n, true);

        // Update lists contacts in clients
        this.updateContact();
      }
    },

    /**
     * On select type modif update nom_affaire
     */
    typeModifSelected() {
      this.form.nom = (this.form.affaire_modif_type.id?
                       this.typesModficiationAffaire_list.filter(x => x.id === this.form.affaire_modif_type.id) + " : " : null) + this.form.nom_;
    },

    /**
     * Récupère les numéros référencés, réservés et le client de la facture
     */
    setModificationAffaireNuméros() {
      this.$http
      .get(
        process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" +
          this.form.affaire_base_id + "?affaire_numero_actif=true",
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      )
      .then(response => {
        if (response && response.data) {
          this.affaire_numeros_all = response.data;
          this.affaire_numeros_nouveaux = response.data.filter(
            x => x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID)
          );
          this.affaire_numeros_anciens = response.data.filter(
            x => x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID)
          );
          this.affaire_numeros_nouveaux.forEach(function(element) {
            if (element.numero_etat_id === Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)) {
              element.active = false;
            } else {
              element.active = true;
            }
          });

          // get client_affaire
          const url = process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT + this.form.affaire_base_id;
          this.$http.get(url,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }).then(response => {
            if(response && response.data)
              var affaire_factures = response.data;
              this.client_facture = this.clients_list.filter(x => x.id === affaire_factures[0].client_id)[0];
          }).catch(err => handleException(err, this));
        }
      })
      .catch(err => {
        handleException(err, this);
      });
    },

    /**
     * Récupérer la sélection des anciens numéros
     */
    onSelectNumsAnciens(items) {
      this.selectedAnciensNumeros = items;
    },

    /**
     * Récupérer la sélection des nouveaux numéros
     */
    onSelectNumsNouveux(items) {
      this.selectedNouveauxNumeros = items;
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
     * Init liste of people working in an entreprise
     */
    async initClientMoralPersonnes(client_id, client_type) {
      return new Promise((resolve) => {
        if (client_id) {
          this.$http.get(
            process.env.VUE_APP_API_URL +
            process.env.VUE_APP_CLIENT_MORAL_PERSONNES_ENDPOINT + "/" +
            client_id,
            {
              withCredentials: true,
              headers: {Accept: "application/json"}
            }
          ).then(response => {
            if (response && response.data) {
              let tmp = [];
              response.data.forEach(x => tmp.push([x.titre, x.prenom, x.nom].filter(Boolean).join(" ")));
              this.client_moral_personnes[client_type] = tmp;
              resolve(tmp);
            }
          }).catch(err => this.handleException(err, this));
        }
      });
    },

    /**
     * open create contact
     */
    openCreateContact(client_id) {
      let routeData = this.$router.resolve({name: "ClientsEdit", params: {id: client_id}});
      window.open(routeData.href, "_blank");
    },

    /**
     * Update contact when 
     */
    async updateContact() {
      if (this.form.client_commande !== null && this.form.client_commande.id !== null) {
        this.initClientMoralPersonnes(this.form.client_commande.id, 'commande');
      }
      if (this.form.client_envoi !== null && this.form.client_envoi.id !== null) {
        this.initClientMoralPersonnes(this.form.client_envoi.id, 'envoi');
      }
      if (this.client_facture !== null && this.client_facture.id !== null &&
          this.form.type && this.form.type.id && this.form.type.id !== this.typesAffaires_conf.pcop) {
        this.initClientMoralPersonnes(this.client_facture.id, 'facture');
      }
    },

    /**
     * Get plans MO
     */
    async getPlansMO() {
      this.$http.get(
        process.env.VUE_APP_API_URL + 
        process.env.VUE_APP_PLANS_MO_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.plansMOListe = response.data;
        }
      })
    },

    /**
     * set plans_MO of selected cadastre
     */
    setPlanMoCadastre(){
      if (this.form.cadastre && this.form.cadastre.id) {
        this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
      }
    },

    /**
     * Ouvrir la boîte de dialogue de référence de numéros
     */
    callOpenReferenceDialog() {
      this.$refs.formReference.openReferenceDialog();
    },

    /**
     * Numéros référencés (pour les affaires qui le nécessitent)
     */
    referenceNumeros(items) {
      this.numerosReferences = items;
      return new Promise((resolve, reject) => {
        resolve(null);
        reject(null);
      })
    },

    /**
     * Remove entree from referenced numbers
     */
    deleteNumeroReference(item){
      this.numerosReferences = this.numerosReferences.filter(x => x !== item);
    },

    /**
     * Enregistrer les numéros référencés à l'affaire 
     */
    async saveReferenceNumeros(affaire_id) {
      let numeros_ = this.numerosReferences.map(x => ({
        numero_id: x.id,
        etat_id: x.etat_id
      }));

      let formData = new FormData();
      formData.append("affaire_id", affaire_id);
      formData.append("numeros_liste", JSON.stringify(numeros_));

      return new Promise((resolve, reject) => {
        this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_REFERENCE_NUMEROS_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => resolve(response))
          .catch(err => reject(err));
      });
    },

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
    this.initTypesModficiationAffaire();
    this.getPlansMO();
    this.initMask();

    //permissions
    this.permission.editClientAllowed = checkPermission(process.env.VUE_APP_CLIENT_EDITION);
  }
};
</script>
