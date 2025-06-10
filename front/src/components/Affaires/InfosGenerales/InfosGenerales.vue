<style src="./infosGenerales.css" scoped></style>
<template src="./infosGenerales.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {
  stringifyAutocomplete,
  getDocument,
  getCurrentUserRoleId
} from '@/services/helper';

import ClientSearch from "@/components/Utils/ClientSearch/ClientSearch.vue";

const moment = require("moment");

export default {
  name: "InfosGénérales",
  props: {
    typesAffaires_conf: {type: Object},
    affaire: {type: Object},
    clientTypes_conf: {type: Object},
    permission: {type: Object},
    etapes_affaire_conf: {type: Object},
    affaireDashboardLayout: {type: Object},
  },
  components: {
    ClientSearch
  },
  data() {
    return {
      affaire_backup: {},
      infoGenReadonly: true,
      affaireReadonly: true,
      typeAffaireReadonly: true,
      affaireUrgente: {
        disabled: true,
        urgent: false,
        urgent_echeance: null,
      },
      typesAffairesListe_all: [],
      typesAffairesListe: [],
      affaires_source: [],
      affaires_destination: [],
      clientsFacture: [],
      clientsFacture_selected_id: 1,
      client_moral_personnes: {
        commande: [],
        envoi: [],
      },
      form: {
        typeAffaire: null,
        client_commande_id: null,
        client_commande_type_id: null,
        client_commande_complement: null,
        client_envoi_id: null,
        client_envoi_type_id: null,
        client_envoi_complement: null
      },
      saveAllowed: true,
      show: {
        clientFacture: false,
      }
    };
  },

  methods: {
    /**
     * Ouvre la page de consultation/édition de client
     */
    openClientEditor(field_name) {
      let routedata = null;
      if (field_name.toLowerCase().includes('facture')) {
        routedata = this.$router.resolve({name: 'ClientsEdit', params: {id: this.clientsFacture.filter(x => x.id === this.clientsFacture_selected_id)[0].client_id}});
      }else {
        routedata = this.$router.resolve({name: 'ClientsEdit', params: {id: this.affaire[field_name]}});
      }
      window.open(routedata.href, "_blank");
    },
    /*
     * CREATE COPY OF AFFAIRE
     */
    copyAffaire() {
      Object.assign(this.affaire_backup, this.affaire);
    },

    /**
     * Annuler l'édition du formulaire
     */
    onCancelEdit() {
      Object.assign(this.affaire, this.affaire_backup);
      this.setAffaireUrgente();
      this.infoGenReadonly = true;
      this.$emit('modify-off', true);
    },

    /**
     * Enregistrer les modifications
     */
    async onConfirmEdit() {
      let formData = new FormData();
      formData.append("id_affaire", this.affaire.id);
      formData.append("type_id", this.form.typeAffaire.id);
      formData.append("information", this.affaire.information);
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);

      if (this.affaire.nom !== null) {
        formData.append("nom", this.affaire.nom || null);
      }

      if (this.form.client_commande_id) {
        formData.append("client_commande_id", this.form.client_commande_id || null);
      }

      if (this.form.client_envoi_id) {
        formData.append("client_envoi_id", this.form.client_envoi_id || null);
      }

      if (this.affaireUrgente.urgent) {
        formData.append("urgent", this.affaireUrgente.urgent);

        if (this.affaireUrgente.urgent_echeance !== null) {
          formData.append("urgent_echeance", moment(this.affaireUrgente.urgent_echeance, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
        }
      }

      formData.append("client_commande_complement", this.form.client_commande_complement || null);
      formData.append("client_envoi_complement", this.form.client_envoi_complement || null);
      formData.append("localisation_E", this.affaire.localisation_e);
      formData.append("localisation_N", this.affaire.localisation_n);

      // dates
      formData.append("date_ouverture", this.affaire.date_ouverture? moment(this.affaire.date_ouverture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("date_envoi", this.affaire.date_envoi? moment(this.affaire.date_envoi, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("date_validation", this.affaire.date_validation? moment(this.affaire.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);
      formData.append("date_cloture", this.affaire.date_cloture? moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS): null);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => { //response =>{
          this.infoGenReadonly = true;
          this.$emit('modify-off', true);
          this.$parent.setAffaire().then(() => {
            this.copyAffaire();
            this.enableAffaireUrgente();
          });
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },


    /**
     * Open Edit mode
     */
    openEditMode() {
      this.form.typeAffaire = this.typesAffairesListe_all.filter(x => x.id === this.affaire.type_id)[0];

      this.form.client_commande_id = this.affaire.client_commande_id;
      this.form.client_commande_complement = this.affaire.client_commande_complement;

      this.form.client_envoi_id = this.affaire.client_envoi_id;
      this.form.client_envoi_complement = this.affaire.client_envoi_complement;
      this.infoGenReadonly = false;
      this.$emit('modify-off', false);

      setTimeout(() => {
        this.selectedClient(this.form.client_commande_id, 'client_commande');
        this.selectedClient(this.form.client_envoi_id, 'client_envoi');
      }, 200);
    },

    /**
     * get cadastres
     */
    async initTypesAffairesListe() {

        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.typesAffairesListe_all = stringifyAutocomplete(response.data);
            if (this.affaire.modif_affaire_type_id_vers !== null) {
              this.typesAffairesListe = this.typesAffairesListe_all.filter(x => {
                return this.affaire.modif_affaire_type_id_vers.includes(x.id);
            });
            } else {
              this.typesAffairesListe = [];
            }
          }
        }).catch(err => handleException(err, this))

    },

    /**
     * Récupère l'affaire mère
     */
    async searchAffaireSource() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_MODIFICATION_AFFAIRE_BY_AFFAIRE_MERE_ENDPOINT +
        this.affaire.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          var tmp = [];
          response.data.forEach(x => {
            tmp.push(x.affaire_id_mere)
          });
          this.affaires_source = tmp;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Récupère l'affaire fille
     */
    async searchAffaireDestination() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_MODIFICATION_AFFAIRE_BY_AFFAIRE_FILLE_ENDPOINT +
        this.affaire.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          var tmp = [];
          response.data.forEach(x => {
            tmp.push(x.affaire_id_fille)
          });
          this.affaires_destination = tmp;
        }
      }).catch(err => handleException(err, this));
    },


    genererBordereau() {
      let formData = new FormData()
      formData.append("template", "Bordereau");
      formData.append("values", JSON.stringify({
        "ADRESSE": this.affaire.client_envoi_nom_
      }));

      getDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le document '"+ response +"' se trouve dans le dossier Téléchargement")
      }).catch(err => handleException(err, this));
    },


    /**
     * Open affaire "repris par" or "provient de"
     */
    openAffaire(affaire_id) {
      this.$router.replace({ name: "AffairesDashboard", params: {id: affaire_id}});
      this.$router.go(0);
    },


    /**
     * on set echeance
     */
    onSetUrgentEcheance() {
      if (this.affaireUrgente.urgent_echeance !== null) {
        this.affaireUrgente.urgent_echeance = moment(this.affaireUrgente.urgent_echeance).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        this.affaireUrgente.urgent_echeance = null;
      }
    },

    /**
     * Set Affaire urgente
     */
    setAffaireUrgente() {
      this.affaireUrgente = {
        urgent: this.affaire.urgent,
        urgent_echeance: this.affaire.urgent_echeance,
        disabled: true,
      }
    },

    /**
     * Enable edit Affaire Urgente
     */
    enableAffaireUrgente() {
      //Check role_id
      let role_id = getCurrentUserRoleId();

      // Secrétariat peut modifier des factures à tout moment, éditer les informations des affaires et référencer des numéros à l'affaire
      this.affaireUrgente.disabled = this.affaireUrgente.urgent === true || ![
        Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID),
        Number(process.env.VUE_APP_ADMIN_ROLE_ID),
        Number(process.env.VUE_APP_PPE_ROLE_ID),
        Number(process.env.VUE_APP_MO_PPE_ROLE_ID),
      ].includes(role_id);
    },

    /**
     * Set permissions
     */
    setPermissions() {
      this.affaireReadonly = !this.permission.editAffaireAllowed;
      this.typeAffaireReadonly = !(
        this.permission.editAffaireTypeAllowed
        && this.affaire.modif_affaire_type_id_vers !== null
        && [this.etapes_affaire_conf.coordination, this.etapes_affaire_conf.travaux_chef_equipe, this.etapes_affaire_conf.controle_technique].includes(this.affaire.etape_id)
      );
    },

    selectedClient(client_id, client_type) {
      this.form[client_type + '_id'] = client_id;
      this.form[client_type + '_type_id'] = this.$refs['ref_' + client_type].client.type_client;
      this.updateContact();
    },

    /**
     * Update contact when
     */
     async updateContact() {
      if (this.form.client_commande_id !== null) {
        this.initClientMoralPersonnes(this.form.client_commande_id, 'commande');
      }
      if (this.form.client_envoi_id !== null) {
        this.initClientMoralPersonnes(this.form.client_envoi_id, 'envoi');
      }
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

    async getClientsFacture() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_CLIENTS_FACTURE_BY_AFFAIRE_ID_ENDPOINT +
        this.affaire.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.clientsFacture = response.data;
        }
      }).catch(err => handleException(this, err))
      .finally(() => this.show.clientFacture = this.affaire.type_id !== this.typesAffaires_conf.pcop);

    },

    async delaySaveBtn() {
      this.saveAllowed = false;
    },

    estObjetDate(val) {
      return val instanceof Date && !isNaN(val.getTime());
    },
  },

  watch: {
    'affaire.date_ouverture' (newVal, oldVal) {
      if (newVal !== oldVal && this.estObjetDate(newVal)) {
        this.affaire.date_ouverture = moment(this.affaire.date_ouverture).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        this.saveAllowed = true;
      }
    },
    'affaire.date_envoi' (newVal, oldVal) {
      if (newVal !== oldVal && this.estObjetDate(newVal)) {
        this.affaire.date_envoi = moment(this.affaire.date_envoi).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        this.saveAllowed = true;
      }
    },
    'affaire.date_validation' (newVal, oldVal) {
      if (newVal !== oldVal && this.estObjetDate(newVal)) {
        this.affaire.date_validation = moment(this.affaire.date_validation).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        this.saveAllowed = true;
      }
    },
    'affaire.date_cloture' (newVal, oldVal) {
      if (newVal !== oldVal && this.estObjetDate(newVal)) {
        this.affaire.date_cloture = moment(this.affaire.date_cloture).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        this.saveAllowed = true;
      }
    },
  },

  mounted: function() {
    this.copyAffaire();
    this.initTypesAffairesListe();
    this.searchAffaireSource();
    this.searchAffaireDestination();
    this.setAffaireUrgente();
    this.setPermissions();
    this.getClientsFacture();
    this.$root.$on('reloadClientFactureInfosGen', () => this.getClientsFacture());
    this.enableAffaireUrgente();
  }
};
</script>
