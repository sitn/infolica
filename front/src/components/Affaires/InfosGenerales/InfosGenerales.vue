<style src="./infosGenerales.css" scoped></style>
<template src="./infosGenerales.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission,
        stringifyAutocomplete,
        getClients,
        filterList,
        getDocument} from '@/services/helper';

const moment = require("moment");

export default {
  name: "InfosGénérales",
  props: {
    typesAffaires_conf: {type: Object},
    affaire: {type: Object}
    },
  components: {},
  data() {
    return {
      affaire_backup: {},
      infoGenReadonly: true,
      affaireReadonly: true,
      operateursListe: [],
      typesAffairesListe_all: [],
      typesAffairesListe: [],
      affaires_source: [],
      affaires_destination: [],
      clientsFacture: { 
        selectList: [],
        adressList: [],
        selected_id: 0,
        selected_adress: ''
      },
      clientsListe: [],
      searchClientsListe: [],
      showDateAlert: false,
      controle_dateItem: null,
      form: {
        technicien: null,
        responsable: null,
        typeAffaire: null,
        client_commande: null,
        client_commande_complement: null,
        client_envoi: null,
        client_envoi_complement: null
      },
    };
  },

  methods: {
    /**
     * Search clients
     */
    async initClientsListe() {
      getClients()
        .then(response => {
          if (response && response.data) {
            this.clientsListe = response.data.map(x => ({
              id: x.id,
              nom: x.adresse_,
              toLowerCase: () => x.adresse_.toLowerCase(),
              toString: () => x.adresse_
            }));
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
      this.searchClientsListe = filterList(this.clientsListe, value, 3)
    },

    /**
     * Ouvre la page de consultation/édition de client
     */
    openClientEditor(field_name) {
      let routedata = null;
      if (field_name.toLowerCase().includes('facture')) {
        routedata = this.$router.resolve({name: 'ClientsEdit', params: {id: this.clientsFacture.selected_id}});        
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
      this.infoGenReadonly = true;
      this.$emit('modify-off', true);
    },

    /**
     * Enregistrer les modifications
     */
    async onConfirmEdit() {
      var formData = new FormData();
      formData.append("id_affaire", this.affaire.id);
      formData.append("technicien_id", this.form.technicien.id);
      formData.append("type_id", this.form.typeAffaire.id);
      formData.append("information", this.affaire.information);
      formData.append("vref", this.affaire.vref || null);
      
      if (this.affaire.nom !== null) {
        formData.append("nom", this.affaire.nom || null);
      }

      if (this.form.client_commande && this.form.client_commande.id) {
        formData.append("client_commande_id", this.form.client_commande.id || null);
      }

      if (this.form.client_envoi && this.form.client_envoi.id) {
        formData.append("client_envoi_id", this.form.client_envoi.id || null);
      }

      if (this.affaire.date_validation) {
        formData.append("date_validation", this.affaire.date_validation?
          moment(this.affaire.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      } else {
        formData.append("date_validation", null);
      }
      if (this.affaire.date_envoi) {
        formData.append("date_envoi", this.affaire.date_envoi?
          moment(this.affaire.date_envoi, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      } else {
        formData.append("date_envoi", null);
      }

      if (this.affaire.date_cloture) {
        formData.append("date_cloture", this.affaire.date_cloture?
          moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS) : null);
      } else {
        formData.append("date_cloture", null);
      }

      formData.append("client_commande_complement", this.form.client_commande_complement || null);
      formData.append("client_envoi_complement", this.form.client_envoi_complement || null);
      formData.append("localisation_E", this.affaire.localisation_e);
      formData.append("localisation_N", this.affaire.localisation_n);

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
          this.$parent.setAffaire();
          this.copyAffaire();
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Initialiser la liste des opérateurs
     */
    async initOperateursListe() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.operateursListe = response.data
          .map(x => ({
            id: x.id,
            nom: [x.prenom, x.nom].filter(Boolean).join(" ")
          }))
          .map(x => ({
            id: x.id,
            nom: x.nom,
            toLowerCase: () => x.nom.toLowerCase(),
            toString: () => x.nom.toString()
          }));
        }
      }).catch(err => handleException(err, this))
    },

    /**
     * Open Edit mode
     */
    openEditMode() {
      this.form.technicien = this.operateursListe
      .filter(x => x.id === this.affaire.technicien_id)[0];

      this.form.typeAffaire = this.typesAffairesListe_all
      .filter(x => x.id === this.affaire.type_id)[0];

      this.form.client_commande = this.clientsListe.filter(x => x.id === this.affaire.client_commande_id).pop();
      this.form.client_commande_complement = this.affaire.client_commande_complement;
      this.form.client_envoi = this.clientsListe.filter(x => x.id === this.affaire.client_envoi_id);
      this.form.client_envoi_complement = this.affaire.client_envoi_complement;

      this.infoGenReadonly = false;
      this.$emit('modify-off', false);
    },

    /**
     * openCreateClient
     */
    openCreateClient() {
      let routedata = this.$router.resolve({ name: "ClientsNew" });
      window.open(routedata.href, "_blank");
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
        this.$route.params.id,
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
        this.$route.params.id,
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

    /**
     * Contrôle que la date de validation soit supérieure à la date d'ouverture
     */
    async onSelectDate() {
      await new Promise(r => setTimeout(r, 200));
      let date_ouverture = moment(this.affaire.date_ouverture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
      let date_validation = moment(this.affaire.date_validation, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
      let date_envoi = moment(this.affaire.date_envoi, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
      let date_cloture = moment(this.affaire.date_cloture, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
      if (date_validation < date_ouverture) {
        this.controle_dateItem = "date_validation";
        this.showDateAlert = true;
      }
      if (date_envoi < date_validation) {
        this.controle_dateItem = "date_envoi";
        this.showDateAlert = true;
      }
      if (date_cloture < date_envoi) {
        this.controle_dateItem = "date_cloture";
        this.showDateAlert = true;
      }
    },

    /**
     * Effacer la date inférieure
     */
    onAcceptDateAlert() {
      this.affaire[this.controle_dateItem] = null;
      this.showDateAlert = false;
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
     * Search Clients facture
     */
    async searchClientsFacture() {
      this.clientsFacture = { 
        selectList: [],
        adressList: [],
        selected_id: 0,
        selected_adress: ''
      };

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_FACTURES_ENDPOINT + this.affaire.id,
        {
          withCredentials: true,
          headers: {Accept: "appication/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;

          tmp.forEach(x => {
            // construct select list
            this.clientsFacture.selectList.push({
              id: x.client_id,
              nom: [
                x.client_entreprise,
                [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" ")
              ].filter(Boolean).join(", ")
            });


            // construct adresses list
            let adress = "";
            if (x.client_premiere_ligne !== null) {
              // Cas hoirie, PPE ou personne représentée (par)
              adress = [
                x.client_premiere_ligne,
                x.client_entreprise !== null?
                  ["Par " + x.client_entreprise, x.client_complement !== null? x.complement:
                    [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" ")].filter(Boolean).join(", "):
                  "Par " + [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                x.client_co,
                x.client_adresse,
                x.client_case_postale,
                [x.client_npa, x.client_localite].filter(Boolean).join(" ")
              ].filter(Boolean).join("\n");
            } else if (x.client_co_id !== null) {
              // Cas envoi adresse différente de celle du débiteur
              adress = [
                [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                ["c/o", x.client_co_titre, x.client_co_nom, x.client_co_prenom].filter(Boolean).join(" "),
                x.client_co_co,
                x.client_co_adresse,
                x.client_co_case_postale,
                [x.client_co_npa, x.client_co_localite].filter(Boolean).join(" ")
              ].filter(Boolean).join("\n");
            } else {
              // Cas adresse facturation = adresse débiteur
              adress = [
                x.client_entreprise,
                x.client_complement? x.client_complement: [x.client_titre, x.client_nom, x.client_prenom].filter(Boolean).join(" "),
                x.client_co,
                x.client_adresse,
                x.client_case_postale,
                [x.client_npa, x.client_localite].filter(Boolean).join(" ")
              ].filter(Boolean).join("\n");
            }
            
            this.clientsFacture.adressList.push({
              id: x.client_id,
              adress: adress
            });

          });

          // stringify lists
          this.clientsFacture.adressList = stringifyAutocomplete(this.clientsFacture.adressList, 'adress');
          this.clientsFacture.selectList = stringifyAutocomplete(this.clientsFacture.selectList, 'nom');

          //set default adress
          this.clientsFacture.selected_adress = this.clientsFacture.adressList[this.clientsFacture.selected_id].nom;
          this.clientsFacture.selected_id = this.clientsFacture.adressList[this.clientsFacture.selected_id].id;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Update client facture adress when selection changed
     */
    updateClientFactureAdresse() {
      this.clientsFacture.selected_adress = this.clientsFacture.adressList.filter(x => x.id === this.clientsFacture.selected_id)[0].nom;
    }

  },

  mounted: function() {
    this.copyAffaire();
    this.initOperateursListe();
    this.initTypesAffairesListe();
    this.searchAffaireSource();
    this.searchAffaireDestination();
    this.initClientsListe();
    this.searchClientsFacture();
    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>
