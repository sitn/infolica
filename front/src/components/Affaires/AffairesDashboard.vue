<style src="./affairesDashboard.css" scoped></style>
<template src="./affairesDashboard.html"></template>


<script>
import InfosGenerales from "@/components/Affaires/InfosGenerales/InfosGenerales.vue";
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import NumerosAffaire from "@/components/Affaires/NumerosAffaire/NumerosAffaire.vue";
import Documents from "@/components/Affaires/Documents/Documents.vue";
import Suivi from "@/components/Affaires/Suivi/Suivi.vue";
import Preavis from "@/components/Affaires/Preavis/Preavis.vue";
import DuplicationAffaire from "@/components/Affaires/DuplicationAffaire/DuplicationAffaire.vue";
import Facturation from "@/components/Affaires/Facturation/Facturation.vue";
import Remarques from "@/components/Affaires/Remarques/Remarques.vue";
import ControleMutation from "@/components/Affaires/ControleMutation/ControleMutation.vue";
import ControleGeometre from "@/components/Affaires/ControleGeometre/ControleGeometre.vue";
import ControlePPE from "@/components/Affaires/ControlePPE/ControlePPE.vue";
import SuiviMandat from "@/components/Affaires/SuiviMandat/SuiviMandat.vue";
import ClotureAffaire from "@/components/Affaires/ClotureAffaire/ClotureAffaire.vue";
import ActivationAffaire from "@/components/Affaires/ActivationAffaire/ActivationAffaire.vue";

import { handleException } from "@/services/exceptionsHandler";
import { getTypesAffaires, getOperateurs, checkPermission, getDocument, stringifyAutocomplete, logAffaireEtape } from '@/services/helper'

import moment from "moment";

export default {
  name: "AffairesDashboard",
  props: {},
  components: {
    InfosGenerales,
    MapHandler,
    NumerosAffaire,
    Documents,
    Suivi,
    Preavis,
    Facturation,
    Remarques,
    ControleMutation,
    ControleGeometre,
    ControlePPE,
    SuiviMandat,
    DuplicationAffaire,
    ClotureAffaire,
    ActivationAffaire
  },
  data() {
    return {
      abandonAffaireEnabled: true,
      affaire: {},
      affaireEtapes: [],
      etapeAffaire: {
        prochaine: null,
        remarque: null,
        showDialog: false,
      },
      affaireLoaded: false,
      cloreAffaireEnabled: false,
      duplicationAffaireForm: null,
      editAffaireAllowed: true,
      mapLoaded: false,
      chefs_equipe_list: [],
      parentparentAffaireReadOnly: false,
      showConfirmAbandonAffaireDialog: false,
      suiviAffaireTheorique: [],
      typesAffaires: [],
      typesAffaires_conf: {
        mutation: Number(process.env.VUE_APP_TYPE_AFFAIRE_DIVISION),
        cadastration: Number(process.env.VUE_APP_TYPE_AFFAIRE_CADASTRATION),
        ppe: Number(process.env.VUE_APP_TYPE_AFFAIRE_PPE),
        pcop: Number(process.env.VUE_APP_TYPE_AFFAIRE_PCOP),
        maj_periodique: Number(process.env.VUE_APP_TYPE_AFFAIRE_MAJ_PERIODIQUE),
        modification: Number(process.env.VUE_APP_TYPE_AFFAIRE_MODIFICATION),
        revision_abornement: Number(process.env.VUE_APP_TYPE_AFFAIRE_REVISION_ABORNEMENT),
        remaniement_parcellaire: Number(process.env.VUE_APP_TYPE_AFFAIRE_REMANIEMENT_PARCELLAIRE),
        servitude: Number(process.env.VUE_APP_TYPE_AFFAIRE_SERVITUDE),
        retablissement_pfp3: Number(process.env.VUE_APP_TYPE_AFFAIRE_RETABLISSEMENT_PFP3),
        autre: Number(process.env.VUE_APP_TYPE_AFFAIRE_AUTRE),
        modification_type: {
          abandon_partiel: Number(process.env.VUE_APP_TYPE_MODIFICATION_ABANDON_PARTIEL_ID)
        }
      },
      etapes_affaire_conf: {
        travaux_chef_equipe: Number(process.env.VUE_APP_ETAPE_TRAVAUX_CHEF_EQUIPE_ID)
      },
      // numeros_base_associes = []
    };
  },

  methods: {
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
              var obj = response.data;

              obj["client_commande_nom_"] = [
                obj.client_commande_entreprise,
                obj.client_commande_complement? obj.client_commande_complement: [obj.client_commande_titre, obj.client_commande_nom, obj.client_commande_prenom].filter(Boolean).join(" "),
                obj.client_commande_co,
                obj.client_commande_adresse,
                obj.client_commande_case_postale,
                [obj.client_commande_npa, obj.client_commande_localite].filter(Boolean).join(" ")]
                .filter(Boolean).join("\n");

              obj["client_envoi_nom_"] = [
                obj.client_envoi_entreprise,
                obj.client_envoi_complement !== null? obj.client_envoi_complement: [obj.client_envoi_titre, obj.client_envoi_nom, obj.client_envoi_prenom].filter(Boolean).join(" "),
                obj.client_envoi_co,
                obj.client_envoi_adresse,
                obj.client_envoi_case_postale,
                [obj.client_envoi_npa, obj.client_envoi_localite].filter(Boolean).join(" ")]
                .filter(Boolean).join("\n");

              obj["technicien"] = [obj.technicien_prenom, obj.technicien_nom]
                .filter(Boolean).join(" ");

              Object.keys(obj).forEach(function(key) {
                // Formater la date en DD.MM.YYYY
                if (key.includes("date") && obj[key] !== null && obj[key] !== "") {
                  obj[key] = moment(obj[key], process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
                }
              });
              resolve(obj);
            }
          })
          .catch(() => reject);
      });
    },

    /**
     * Search affaire etapes
     */
    async searchAffaireEtapes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPES_INDEX_ENDPOINT,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        this.affaireEtapes = stringifyAutocomplete(response.data.filter(x => x.ordre !== null));
        // get suivi d'affaire théorique
        this.typesAffaires = getTypesAffaires().then(response => {
          if (response && response.data) {
            this.suiviAffaireTheorique = response.data.filter(x => x.id === this.affaire.type_id)[0].logique_processus;
          }
        })
      }).catch(err => handleException(err, this));
    },

    /**
     * Set affaire
     */
    async setAffaire() {
        let _this = this;
        this.searchAffaire().then(function(obj){
          _this.affaire = obj;
          _this.affaireLoaded = true;
          _this.editAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION);
          _this.abandonAffaireEnabled = (_this.affaire.date_cloture === null || _this.affaire.date_cloture === undefined);
          _this.cloreAffaireEnabled = (_this.affaire.date_cloture === null || _this.affaire.date_cloture === undefined) && (_this.affaire.date_envoi !== null && _this.affaire.date_envoi !== undefined);
          _this.parentAffaireReadOnly = (_this.affaire.date_cloture !== null && _this.affaire.date_cloture !== undefined) && (_this.affaire.date_envoi !== null && _this.affaire.date_envoi !== undefined);
  
          //If admin, allow edit
          if(checkPermission(process.env.VUE_APP_FONCTION_ADMIN)){
            _this.parentAffaireReadOnly = false;
          }
          _this.searchAffaireEtapes();
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
    async callAbandonAffaire() {
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
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_ABANDON_ID));

            this.$router.go();
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
    
    // /**
    //  * Duplicate affaire
    //  */
    // duplicateAffaire(){
    //   this.$refs.duplicationAffaireForm.openDuplicationAffaireDialog();
    // },

    /**
     * Open Theme SITN
     */
    openSitnTheme(theme) {
      var route;
      if (theme === "environnement") {
        route = process.env.VUE_APP_SITN_ENVIRONNEMENT_URL;
      } else if (theme === "amenagement_territoire") {
          route = process.env.VUE_APP_SITN_AMENAGEMENT_TERRITOIRE_URL;
      } else {
        return null;
      }
      window.open(route + "&map_x=" + this.affaire.localisation_e + "&map_y=" + this.affaire.localisation_n, "_blank");
    },

    modifyOff(value) {
      if (value === false) {
        this.$refs.mapHandler.modify.setActive(true);
        this.$refs.mapHandler.snap.setActive(true);
      } else {
        this.$refs.mapHandler.modify.setActive(false);
        this.$refs.mapHandler.snap.setActive(false);
        this.$refs.mapHandler.addMarker(this.affaire.localisation_e, this.affaire.localisation_n);
        this.center.x = this.affaire.localisation_e;
        this.center.y = this.affaire.localisation_n;
      }
    },

    /**
     * open New state dialog
     */
    openNewStateDialog(){
      // set next step prediction
      this.etapeAffaire.prochaine = null;
      this.etapeAffaire.chef_equipe_id = this.affaire.technicien_id || null;
      this.etapeAffaire.remarque = null;
      
      if (this.suiviAffaireTheorique.includes(this.affaire.etape_id)) {
        this.etapeAffaire.prochaine = this.affaireEtapes.filter(x => x.id === this.suiviAffaireTheorique[this.suiviAffaireTheorique.indexOf(this.affaire.etape_id)+1])[0];
      }

      this.etapeAffaire.showDialog = true;
    },

    /**
     * Enregistrer la nouvelle étape
     */
    async updateAffaireEtape() {
      // fix value of this.etapeAffaire.chef_equipe_id to null if another step is selected
      this.etapeAffaire.chef_equipe_id = this.etapeAffaire.prochaine.id && this.etapeAffaire.prochaine.id === this.etapes_affaire_conf.travaux_chef_equipe? this.etapeAffaire.chef_equipe_id: null;

      logAffaireEtape(this.affaire.id, this.etapeAffaire.prochaine.id, this.etapeAffaire.remarque, this.etapeAffaire.chef_equipe_id)
      .then(() => {
        this.$root.$emit("ShowMessage", "L'étape a bien été mise à jour");
        this.etapeAffaire.showDialog = false;
        this.setAffaire();
      })
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
        adresse: x.client_.replace(/, /gi, "\n"),
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
        "OPERATEUR": [this.affaire.technicien_prenom, this.affaire.technicien_nom].filter(Boolean).join (" "),
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

  },

  mounted: function() {
    this.setAffaire();
    this.getChefsEquipe();
    this.$root.$on('mapHandlerReady', () =>{
      this.showMap();
    });
  }
};
</script>
