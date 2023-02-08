<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
import Etape from "@/components/Affaires/Etape/Etape.vue";
import InfosGenerales from "@/components/Affaires/InfosGenerales/InfosGenerales.vue";
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import NumerosAffaire from "@/components/Affaires/NumerosAffaire/NumerosAffaire.vue";
import Documents from "@/components/Affaires/Documents/Documents.vue";
import Suivi from "@/components/Affaires/Suivi/Suivi.vue";
import Preavis from "@/components/Affaires/Preavis/Preavis.vue";
import Facturation from "@/components/Affaires/Facturation/Facturation.vue";
import ControleMutation from "@/components/Affaires/ControleMutation/ControleMutation.vue";
import ControleGeometre from "@/components/Affaires/ControleGeometre/ControleGeometre.vue";
import ControlePPE from "@/components/Affaires/ControlePPE/ControlePPE.vue";
import SuiviMandat from "@/components/Affaires/SuiviMandat/SuiviMandat.vue";
import ClotureAffaire from "@/components/Affaires/ClotureAffaire/ClotureAffaire.vue";
import ActivationAffaire from "@/components/Affaires/ActivationAffaire/ActivationAffaire.vue";
import EmptyPage from "@/components/Utils/EmptyPage/EmptyPage.vue";

import { handleException } from "@/services/exceptionsHandler";
import { getOperateurs, checkPermission, getDocument, logAffaireEtape, getCurrentUserRoleId } from '@/services/helper'

import moment from "moment";

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
    Etape,
    InfosGenerales,
    MapHandler,
    NumerosAffaire,
    Documents,
    Suivi,
    Preavis,
    Facturation,
    ControleMutation,
    ControleGeometre,
    ControlePPE,
    SuiviMandat,
    ClotureAffaire,
    ActivationAffaire,
    EmptyPage
  },
  data() {
    return {
      affaire: {},
      affaireAttribution: {
        checked: false,
        show: false,
        text: ""
      },
      affaireLoaded: false,
      affaireDashboardLayout: null,
      chefs_equipe_list: [],
      emptyPage: false,
      mapLoaded: false,
      numerosReserves: [],
      parentAffaireReadOnly: false,
      permission: {
        abandonAffaireEnabled: false,
        admin_permissions: false,
        cloreAffaireEnabled: false,
        cloreEmolumentEnabled: false,
        editAffaireAllowed: false,
        editAffaireTypeAllowed: false,
        editClientAllowed: false,
        editControleGeometreAllowed: false,
        editEmolumentAllowed: false,
        editFactureAllowed: false,
        editNumerosReferencesAllowed: false,
        editNumerosAllowed: false,
        editNumerosMOAllowed: false,
        editSuiviMandatAllowed: false,
        editEmolumentIndiceApplication: false,
        editEmolumentTva: false,
        editEmolumentFreeze: false,
        showRemaniementParcellaireLoadingBtn: false,
        showEmolumentRepartition_saveToFactures_btn: false,
      },
      showConfirmAbandonAffaireDialog: false,
      showConfirmAbandonErrorAffaireDialog: false,
      typesAffaires: [],
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
        modification_retour_etat_juridique: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIF_RETABLISSEMENT_ETAT_JURIDIQUE),
      },
      etapes_affaire_conf: {
        coordination: Number(process.env.VUE_APP_ETAPE_COORDINATION_ID),
        controle_technique: Number(process.env.VUE_APP_CONTROLE_TECHNIQUE_ID),
        chez_client: Number(process.env.VUE_APP_ETAPE_CHEZ_CLIENT_ID),
        travaux_chef_equipe: Number(process.env.VUE_APP_ETAPE_TRAVAUX_CHEF_EQUIPE_ID),
        servitudes: Number(process.env.VUE_APP_REPORT_SERVITUDES_ID),
        controle_juridique: Number(process.env.VUE_APP_CONTROLE_JURIDIQUE_ID),
        validation: Number(process.env.VUE_APP_ETAPE_VALIDATION_ID),
        envoi: Number(process.env.VUE_APP_ETAPE_ENVOI_ID),
        envoi_cadastration: Number(process.env.VUE_APP_ETAPE_ENVOI_CADASTRATION_ID),
        envoi_pcop: Number(process.env.VUE_APP_ETAPE_ENVOI_PCOP_ID),
        signature_art35: Number(process.env.VUE_APP_ETAPE_SIGNATURE_ART35_ID),
        fin_processus: Number(process.env.VUE_APP_FIN_PROCESSUS_ID),
      },
      clientTypes_conf: {
        physique: Number(process.env.VUE_APP_TYPE_CLIENT_PHYSIQUE_ID),
        moral: Number(process.env.VUE_APP_TYPE_CLIENT_MORAL_ID),
      },
      showMovePointComment: false,
      cssHeaderWidth: 'width: calc(100% - 80px)',
    };
  },

  methods: {
    /*
     * AFFAIRE TYPE LAYOUT
     */
    async searchAffaireTypeLayout() {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append('affaire_id', this.$route.params.id);

        this.$http
          .post(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRE_DASHBOARD_LAYOUT_ENDPOINT,
              formData,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          ).then(response => {
            this.affaireDashboardLayout = response.data;
            resolve(response);
          }).catch(err => reject(err))
      });
    },


    /*
     * SEARCH AFFAIRE
     */
    async searchAffaire() {
      return new Promise((resolve, reject) => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
              this.$route.params.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response.data) {
              let obj = response.data;

              obj["client_commande_nom_"] = [
                obj.client_commande_entreprise,
                obj.client_commande_complement? "(" + obj.client_commande_complement.replace("À l'att. de ", '') + ")": [obj.client_commande_titre, obj.client_commande_prenom, obj.client_commande_nom].filter(Boolean).join(" "),
                obj.client_commande_co,
                obj.client_commande_adresse,
                obj.client_commande_case_postale,
                [obj.client_commande_npa, obj.client_commande_localite].filter(Boolean).join(" ")]
                .filter(Boolean).join("\n");

              // Client d'envoi
              let adresse_ = ""
              if (obj.client_envoi_type_id === this.clientTypes_conf.moral) {
                adresse_ = [
                  obj.client_envoi_entreprise,
                  obj.client_envoi_complement? "À l'att. de " + obj.client_envoi_complement.replace("À l'att. de ", ''): null,
                  obj.client_envoi_co,
                  obj.client_envoi_adresse,
                  obj.client_envoi_case_postale,
                  [obj.client_envoi_npa, obj.client_envoi_localite].filter(Boolean).join(" ")
                ].filter(Boolean);
              } else {
                adresse_ = [
                  [obj.client_envoi_titre, obj.client_envoi_prenom, obj.client_envoi_nom].filter(Boolean).join(" "),
                  obj.client_envoi_co,
                  obj.client_envoi_adresse,
                  obj.client_envoi_case_postale,
                  [obj.client_envoi_npa, obj.client_envoi_localite].filter(Boolean).join(" ")
                ].filter(Boolean);
              }

              obj["client_envoi_nom_"] = adresse_.join("\n");

              obj["technicien"] = [obj.technicien_prenom, obj.technicien_nom]
                .filter(Boolean).join(" ");

              Object.keys(obj).forEach(function(key) {
                // Formater la date en DD.MM.YYYY
                if ((key.includes("date") || key.includes("echeance")) && obj[key] !== null && obj[key] !== "") {
                  obj[key] = moment(obj[key], process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
                }
              });

              obj.urgent_echeance_reste = null;
              if (obj.urgent_echeance !== null) {
                obj.urgent_echeance_reste = Math.ceil(Math.max(0, moment(obj.urgent_echeance, process.env.VUE_APP_DATEFORMAT_CLIENT)-new Date())/1000/3600/24)+1;
              }

              // reset emptyPage
              this.emptyPage = false;

              resolve(obj);
            } else {
              this.emptyPage = true;
            }
          })
          .catch(() => reject);
      });
    },

    /**
     * Set affaire
     */
    async setAffaire() {
        let _this = this;
        this.searchAffaire().then(function(obj){
          _this.affaire = obj;
          _this.affaireLoaded = true;

          _this.parentAffaireReadOnly = ((_this.affaire.date_cloture !== null && _this.affaire.date_cloture !== undefined) || (_this.affaire.date_envoi !== null && _this.affaire.date_envoi !== undefined));
          _this.permission.admin_permissions = false;
          _this.permission.abandonAffaireEnabled = (_this.affaire.date_cloture === null || _this.affaire.date_cloture === undefined);
          _this.permission.cloreAffaireEnabled = (_this.affaire.date_cloture === null || _this.affaire.date_cloture === undefined) && (_this.affaire.date_envoi !== null && _this.affaire.date_envoi !== undefined);
          _this.permission.editNumerosAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_NUMERO_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.editNumerosMOAllowed = checkPermission(process.env.VUE_APP_NUMERO_MO_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.editControleGeometreAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_CONTROLE_GEOMETRE_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.editSuiviMandatAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_SUIVI_EDITION) && !(_this.affaire.date_validation !== null && _this.affaire.date_validation !== undefined);
          _this.permission.editEmolumentAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_FACTURE_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.editFactureAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_FACTURE_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.affaireCloture = checkPermission(process.env.VUE_APP_AFFAIRE_CLOTURE);
          _this.permission.affaireReactivation = checkPermission(process.env.VUE_APP_AFFAIRE_REACTIVATION);
          _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) && !_this.parentAffaireReadOnly;
          _this.permission.editClientAllowed = checkPermission(process.env.VUE_APP_CLIENT_EDITION) && !_this.parentAffaireReadOnly;


          if (_this.affaire.type_id === _this.typesAffaires_conf.ppe) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_PPE_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.revision_abornement) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_REVISION_ABORNEMENT_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.cadastration) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.retablissement_pfp3) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_CADASTRATION_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.pcop) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_PCOP_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.mpd) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_MPD_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.autre) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_AUTRE_EDITION) && !_this.parentAffaireReadOnly;
          } else if (_this.affaire.type_id === _this.typesAffaires_conf.remaniement_parcellaire) {
            _this.permission.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_REMANIEMENT_PARCELLAIRE_EDITION) && !_this.parentAffaireReadOnly;
          }

          //Check role_id
          let role_id = getCurrentUserRoleId();
          
          // Secrétariat peut modifier des factures à tout moment, éditer les informations des affaires et référencer des numéros à l'affaire
          if(role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID)) {
            _this.permission.editAffaireAllowed = true;
            _this.permission.editFactureAllowed = true;
            _this.permission.editEmolumentAllowed = true;
            _this.permission.editClientAllowed = true;
            _this.permission.cloreEmolumentEnabled = true;
            _this.permission.editEmolumentTva = true;
            _this.permission.showEmolumentRepartition_saveToFactures_btn = true;
            _this.permission.editNumerosReferencesAllowed = !_this.parentAffaireReadOnly;
            _this.permission.affaireCloture = _this.affaire.type_id === _this.typesAffaires_conf.pcop;
          }

          // Opérateur MO peut modifier les informations générales de l'affaire
          if(role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_MO_ROLE_ID)) {
            _this.permission.editFactureAllowed = _this.permission.editFactureAllowed && _this.affaire.type_id === _this.typesAffaires_conf.cadastration;
            _this.permission.editNumerosReferencesAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireAllowed = !_this.parentAffaireReadOnly;
          }
          
          // Opérateur ppe peut modifier les informations générales de l'affaire
          if(role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_PPE_ROLE_ID)) {
            _this.permission.editNumerosReferencesAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireAllowed = !_this.parentAffaireReadOnly;
            _this.permission.affaireCloture = [ _this.typesAffaires_conf.ppe, _this.typesAffaires_conf.modification_ppe].includes(_this.affaire.type_id);
          }
          
          // Opérateur mo_ppe peut modifier les informations générales de l'affaire
          if(role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_MO_PPE_ROLE_ID)) {
            _this.permission.editFactureAllowed = _this.permission.editFactureAllowed && _this.affaire.type_id === _this.typesAffaires_conf.cadastration;
            _this.permission.editNumerosReferencesAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireAllowed = !_this.parentAffaireReadOnly;
            _this.permission.affaireCloture = [ _this.typesAffaires_conf.ppe, _this.typesAffaires_conf.modification_ppe].includes(_this.affaire.type_id);
          }
          
          // Opérateur responsable peut référencer des numéros
          if(role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)) {
            _this.permission.editEmolumentIndiceApplication = true;
            _this.permission.editEmolumentTva = true;
            _this.permission.editNumerosReferencesAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireTypeAllowed = !_this.parentAffaireReadOnly;
          }

          // Si l'opérateur de l'affaire est l'utilisateur connecté, il doit pouvoir réserver/référencer et modifier le contenu de l'affaire
          if(_this.affaire.technicien_id === JSON.parse(localStorage.getItem("infolica_user")).id) {
            _this.permission.editNumerosAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editNumerosMOAllowed = !_this.parentAffaireReadOnly;
            _this.permission.editAffaireAllowed = !_this.parentAffaireReadOnly;
          }

          // If admin, allow edit
          if(checkPermission(process.env.VUE_APP_FONCTION_ADMIN)) {
            for (const property in _this.permission) {
              _this.permission[property] = true;
            }
            _this.parentAffaireReadOnly = false;
          }

          // Set affaire attribution
          if (_this.affaire.attribution) {
            _this.affaireAttribution.checked = true;
            _this.affaireAttribution.text = "Étape attribuée à " + _this.affaire.attribution;
          } else {
            _this.affaireAttribution.checked = false;
            _this.affaireAttribution.text = "Cliquer pour s'attribuer l'étape";
          }

          // Set header width
          if (_this.affaire.date_cloture) {
            _this.cssHeaderWidth = 'width: 100%';
          } else {
            _this.cssHeaderWidth = 'width: calc(100% - 80px)';
          }

          // init params attribution affaire
          _this.initParams();
      });
    },


    /**
     * Get chefs d'équipe
     */
    async getChefsEquipe() {
      getOperateurs()
      .then(response => {
        if (response && response.data) {
          this.chefs_equipe_list = response.data.filter(x => x.chef_equipe).map(x => ({
            id: x.id,
            nom: [x.prenom, x.nom].filter(Boolean).join(" ")
          }));
        }
      }).catch(err => handleException(err, this))
    },


    /**
     * Show map
     */
    showMap() {
      if(this.$refs && this.$refs.mapHandler && !this.mapLoaded){
        this.center = {
          x: this.affaire.localisation_e,
          y: this.affaire.localisation_n
        };
        this.$refs.mapHandler.initMap(
          this.center,
          process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM
        );
        this.$refs.mapHandler.addMarker(this.center.x, this.center.y);
        this.$refs.mapHandler.modify.setActive(false);
        this.$refs.mapHandler.snap.setActive(false);
        this.$refs.mapHandler.modify.on("modifyend", this.onFeatureChange(this));
        this.mapLoaded = true;
      }
    },

    onFeatureChange(_this) {

      return function(modify) {
        const features = modify.features.getArray();
        if (features) {
          const feature = features[0];
          const coordinates = feature.getGeometry().getCoordinates();
          _this.affaire.localisation_e = coordinates[0];
          _this.affaire.localisation_n = coordinates[1];
        }
      };
    },

    /**
     * Cloture affaire
     */
    callClotureAffaire() {
      this.$refs.clotureAffaireForm.openClotureDialog();
    },

    /**
     * Réactivation de l'affaire
     */
    callActivationAffaire() {
      this.$refs.activationAffaire.openActivationDialog();
    },

    /**
     * Abandon affaire
     */
    async callAbandonAffaireAndNumeros() {
      let formData = new FormData();
      formData.append("id_affaire", this.affaire.id);
      formData.append("abandon", true);
      formData.append("date_cloture", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          //update etat numeros reserves and numero etat histo
          let promises = [];
          this.$refs.numeros.affaire_numeros_nouveaux.forEach(x => {
            if (x.numero_etat_id === Number(process.env.VUE_APP_NUMERO_PROJET_ID)) {
              promises.push(this.updateNumeroEtat(x, Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)));
              promises.push(this.postNumeroEtatHisto(x, Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)));
            }
          })
          Promise.all(promises)
          .then(() => {
            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_FIN_PROCESSUS_ID), "Abandon de l'affaire")
            .then(() => this.$router.go());
          })
          .catch(err => handleException(err, this));
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Update numeros reserves
     */
    async updateNumeroEtat(numero, nouvel_etat_id) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("id", numero.numero_id);
        formData.append("etat_id", nouvel_etat_id);

        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response)
        ).catch(err => reject(err));
      });
    },
    
    /**
     * post numeros etat histo
     */
    async postNumeroEtatHisto(numero, nouvel_etat_id) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("numero_id", numero.numero_id);
        formData.append("numero_etat_id", nouvel_etat_id);
        formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ETAT_HISTO_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response)
        ).catch(err => reject(err));
      });
    },
    
    /**
     * Open Theme SITN
     */
    openSitnTheme(theme) {
      let route;
      if (theme === "amenagement_territoire") {
          route = process.env.VUE_APP_SITN_AMENAGEMENT_TERRITOIRE_URL;
      } else if (theme === "cadastre") {
          route = process.env.VUE_APP_SITN_CADASTRE_URL;
      } else if (theme === "sites_pollues") {
          route = process.env.VUE_APP_SITN_SITES_POLLUES_URL;
      } else {
        return null;
      }
      window.open(route + "&map_x=" + this.affaire.localisation_e + "&map_y=" + this.affaire.localisation_n, "_blank");
    },

    modifyOff(value) {
      if (value === false) {
        this.$refs.mapHandler.modify.setActive(true);
        this.$refs.mapHandler.snap.setActive(true);
        this.showMovePointComment = true;
      } else {
        this.$refs.mapHandler.modify.setActive(false);
        this.$refs.mapHandler.snap.setActive(false);
        this.$refs.mapHandler.addMarker(this.affaire.localisation_e, this.affaire.localisation_n);
        this.center.x = this.affaire.localisation_e;
        this.center.y = this.affaire.localisation_n;
        this.showMovePointComment = false;
      }
    },


    /**
     * Génère le bordereau de l'affaire (document DEMANDE)
     */
    async generateBordereauAffaire() {
      let formData = this.fillFormDataBordereauAffaire();
      getDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le fichier '" + response + "' se trouve dans le dossier 'Téléchargement'");
      }).catch(err => handleException(err, this));
    },

    /**
     * Get and fill formData for bordereau-affaire
     */
    fillFormDataBordereauAffaire() {
      let tmp = this.$refs.facturation.affaire_factures.map(x => ({
        adresse: x.adresse_facturation_.replace(/, /gi, "\n"),
        tel: x.client_co_id === null? x.client_tel_fixe: x.client_co_tel_fixe,
        tel_port: x.client_co_id === null? x.client_tel_portable: x.client_co_tel_portable,
        mail: x.client_co_id === null? x.client_mail: x.client_co_mail,
        facture: [x.sap !== null? x.sap: "-", String((Number(x.montant_mo) + Number(x.montant_rf)).toFixed(2)), x.montant_mat_diff, x.montant_tva, x.montant_total].join("\n")
      }));
      
      let factures = [];
      for (let i = 0; i < 3; i++) {
        if (i < tmp.length) {
          factures.push(tmp[i]);
        } else {
          factures.push({
            adresse: null,
            tel: null,
            tel_port: null,
            mail: null,
            facture: null
          })
        }

      }
      
      let formData = new FormData();
      formData.append("template", "Commande");
      formData.append("values", JSON.stringify({
        "AFFAIRE_ID": this.affaire.id,
        "OPERATEUR": this.affaire.technicien_initiales,
        "CLIENT_COMMANDE_ADRESSE": this.affaire.client_commande_nom_,
        "CLIENT_COMMANDE_TEL": this.affaire.client_commande_tel_fixe,
        "CLIENT_COMMANDE_TEL_PORT": this.affaire.client_commande_tel_portable,
        "CLIENT_COMMANDE_MAIL": this.affaire.client_commande_mail,
        "CLIENT_ENVOI_ADRESSE": this.affaire.client_envoi_nom_,
        "CLIENT_ENVOI_TEL": this.affaire.client_envoi_tel_fixe,
        "CLIENT_ENVOI_TEL_PORT": this.affaire.client_envoi_tel_portable,
        "CLIENT_ENVOI_MAIL": this.affaire.client_envoi_mail,
        "CLIENT_FACTURE1_ADRESSE": factures[0].adresse,
        "CLIENT_FACTURE1_TEL": factures[0].tel,
        "CLIENT_FACTURE1_TEL_PORT": factures[0].tel_port,
        "CLIENT_FACTURE1_MAIL": factures[0].mail,
        "FACTURE_1": factures[0].facture,
        "CLIENT_FACTURE2_ADRESSE": factures[1].adresse,
        "CLIENT_FACTURE2_TEL": factures[1].tel,
        "CLIENT_FACTURE2_TEL_PORT": factures[1].tel_port,
        "CLIENT_FACTURE2_MAIL": factures[1].mail,
        "FACTURE_2": factures[1].facture,
        "CLIENT_FACTURE3_ADRESSE": factures[2].adresse,
        "CLIENT_FACTURE3_TEL": factures[2].tel,
        "CLIENT_FACTURE3_TEL_PORT": factures[2].tel_port,
        "CLIENT_FACTURE3_MAIL": factures[2].mail,
        "FACTURE_3": factures[2].facture,
        "AFFAIRE_TYPE": this.affaire.type_affaire,
        "MODIFICATION_TYPE": this.affaire.modification_type,
        "AFFAIRE_DE_BASE": this.affaire.modification_affaire_id_mere,
        "NUMEROS_BASES": this.$refs.numeros.affaire_numeros_anciens.map(x => x.numero).sort((a, b) => a-b).join(", "),
        "NUMEROS_RESERVES": this.$refs.numeros.affaire_numeros_nouveaux.map(x => x.numero).sort((a, b) => a-b).join(", "),
        "CADASTRE": this.affaire.cadastre,
        "DESCRIPTION": this.affaire.nom,
        "SPECIFICITES": this.affaire.information, 
        "DATE": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        "DATE_ENVOI_SCAT": this.affaire.preavis_scat_date_demande !== null? this.affaire.preavis_scat_date_demande: null,
        "DATE_RETOUR_SCAT": this.affaire.preavis_scat_date_reponse !== null? this.affaire.preavis_scat_date_reponse: null,
        "DATE_ENVOI_SAGR": this.affaire.preavis_sagr_date_demande !== null? this.affaire.preavis_sagr_date_demande: null,
        "DATE_RETOUR_SAGR": this.affaire.preavis_sagr_date_reponse !== null? this.affaire.preavis_sagr_date_reponse: null,
        "DATE_ENVOI_SENE": this.affaire.preavis_sene_date_demande !== null? this.affaire.preavis_sene_date_demande: null,
        "DATE_RETOUR_SENE": this.affaire.preavis_sene_date_reponse !== null? this.affaire.preavis_sene_date_reponse: null,
        "DATE_ENVOI_RF": this.affaire.preavis_rf_date_demande !== null? this.affaire.preavis_rf_date_demande: null,
        "DATE_RETOUR_RF": this.affaire.preavis_rf_date_reponse !== null? this.affaire.preavis_rf_date_reponse: null,
        "DATE_ENVOI": this.affaire.date_envoi !== null? this.affaire.date_envoi: null,
        "DATE_CLOTURE": this.affaire.date_cloture !== null? this.affaire.date_cloture: null
      }));

      return formData;
    
    },

    /**
     * open Abandon menu
     */
    openAbandonMenu() {
      this.numerosReserves = this.$refs.numeros.affaire_numeros_nouveaux;

      this.showConfirmAbandonErrorAffaireDialog = [
        this.typesAffaires_conf.modification_visa,
        this.typesAffaires_conf.modification_duplicata,
        this.typesAffaires_conf.modification_mutation,
        this.typesAffaires_conf.modification_ppe
      ].includes(this.affaire.type_id);

      this.showConfirmAbandonAffaireDialog = true;
    },

    /**
     * abandon affaire and reactivate parent-affaire
     */
    async callAbandonAffaireAndReactivateParentAffaire() {
      let formData = new FormData();
      formData.append('affaire_id', this.affaire.id);
      formData.append('operateur_id', JSON.parse(localStorage.getItem("infolica_user")).id);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ABANDON_AFFAIRE_REOUVERTURE_AFFAIRE_PARENT_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(() => this.$router.go(0))
      .catch(err => handleException(err));
    },


    /**
     * Affaire Attribution Change State
     */
    async affaireAttributionChangeState() {
      let formData = new FormData();
      if (this.affaireAttribution.checked) {
        formData.append("affaire_id", this.affaire.id);
        formData.append("attribution", JSON.parse(localStorage.getItem("infolica_user")).initiales);
      } else {
        formData.append("affaire_id", this.affaire.id);
        formData.append("attribution", null);
      }
      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_ATTRIBUTION_CHANGE_STATE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(() => this.setAffaire())
      .catch(err => handleException(err));
    },


    /**
     * initialize parameters
     */
    initParams() {
      this.affaireAttribution.show = true;

      let etapesAtributionAffaire = [
        Number(process.env.VUE_APP_CONTROLE_TECHNIQUE_ID),
        Number(process.env.VUE_APP_REPORT_SERVITUDES_ID),
        Number(process.env.VUE_APP_CONTROLE_JURIDIQUE_ID),
        Number(process.env.VUE_APP_PREPARATION_ADMINISTRATIVE_ID),
        Number(process.env.VUE_APP_SIGNATURE_ID),
        Number(process.env.VUE_APP_VALIDATION_ID)
      ];

      if (etapesAtributionAffaire.includes(this.affaire.etape_id)) {
        this.affaireAttribution.show = true;
      } else {
        this.affaireAttribution.show = false;
      }
    }

  },

  mounted: function() {
    this.searchAffaireTypeLayout();
    this.setAffaire();
    this.getChefsEquipe();

    this.$root.$on('mapHandlerReady', () => this.showMap() );
    this.$root.$on('setAffaire', () => this.setAffaire() );
  }
};
</script>
