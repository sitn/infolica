<style src="./preavis.css" scoped></style>
<template src="./preavis.html"></template>


<script>
import { getCurrentDate, checkPermission, saveDocument, logAffaireEtape } from "@/services/helper";
import PreavisEditComments from "@/components/Preavis/PreavisEditComments.vue";
import PreavisEditDecision from "@/components/Preavis/PreavisEditDecision.vue";
import { handleException } from "@/services/exceptionsHandler";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import moment from "moment";

export default {
  name: "preavis",
  mixins: [validationMixin],
  props: {
    affaire: {}
  },
  components: {
    PreavisEditComments,
    PreavisEditDecision
  },
  data: () => {
    return {
      affaire_preavis: [],
      affaireReadonly: true,
      lastRecord: null,
      preavis_type_liste: [],
      modifyPreavis: false,
      new_preavis: {
        id: null,
        service: null,
        preavis: null,
        date_demande: getCurrentDate(),
        date_reponse: null,
        remarque: null
      },
      selectedPreavis: null,
      services_liste: [],
      services_liste_bk: [],
      showNewPreavisBtn: false,
      showPreavisDialog: false,
    };
  },

  // Validations
  validations: {
    new_preavis: {
      service: { required },
      date_demande: { required }
    }
  },

  methods: {
    /*
     * SEARCH AFFAIRE PREAVIS
     */
    async searchAffairePreavis() {
      let tmp = this.selectedPreavis;
      return new Promise ((resolve, reject) => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRE_PREAVIS_ENDPOINT +
              this.$route.params.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response.data) {
              this.affaire_preavis = response.data;
              if (this.affaire_preavis.date_demande) {
                this.affaire_preavis.date_demande = moment(this.affaire_preavis.date_demande, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
              }
              if (this.affaire_preavis.date_reponse) {
                this.affaire_preavis.date_reponse = moment(this.affaire_preavis.date_reponse, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
              }

              this.selectedPreavis = tmp;

              resolve(this.affaier_preavis);
            }
          })
          .catch(err => {
            handleException(err, this);
            reject(err);
          });
      })
    },

    /*
     * SEARCH PREAVIS TYPES
     */
    async searchPreavisType() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_PREAVIS_TYPE_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.preavis_type_liste = response.data.map(x => ({
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
     * SEARCH SERVICES
     */
    async searchServices() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICES_ENDPOINT + '?cadastre_id=' + this.affaire.cadastre_id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.services_liste_bk = response.data;
            this.services_liste = response.data.filter(x => x.ordre !== null).map(x => ({
              id: x.id,
              nom: x.abreviation,
              toLowerCase: () => x.abreviation.toLowerCase(),
              toString: () => x.abreviation
            }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Modifier un préavis existant
     */
    async onModifyPreavis(curr_preavis) {
      await this.searchAffairePreavis();

      this.new_preavis.id = curr_preavis.id;
      this.new_preavis.date_demande = moment(curr_preavis.date_demande, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      if (curr_preavis.date_reponse) {
        this.new_preavis.date_reponse = moment(curr_preavis.date_reponse, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      } else {
        // si pas de date de réponse, proposition défaut aujourd'hui
        this.new_preavis.date_reponse = moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
        }
      // this.new_preavis.date_reponse = curr_preavis.date_reponse;
      this.new_preavis.remarque = curr_preavis.remarque;
      this.new_preavis.service = this.services_liste
        .filter(data => data.nom === curr_preavis.service)
        .map(x => ({
          id: x.id,
          nom: x.nom,
          toLowerCase: () => x.nom.toLowerCase(),
          toString: () => x.nom
        }))[0];
      if (curr_preavis) {
        this.new_preavis.preavis = this.preavis_type_liste
          .filter(data => data.nom === curr_preavis.preavis)
          .map(x => ({
            id: x.id,
            nom: x.nom,
            toLowerCase: () => x.nom.toLowerCase(),
            toString: () => x.nom
          }))[0];
      }
      this.new_preavis.etape = curr_preavis.etape;
      this.modifyPreavis = true;
      this.showPreavisDialog = true;
    },

    /**
     * Confirmer l'édition de préavis
     */
    onConfirmEditPreavis: function() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.saveNewPreavis();
      }
    },

    /**
     * Enregistrer une nouvelle étape
     */
    async saveNewPreavis() {
      let formData = this.fillData();

      let req;
      let remarqueEtapeStatut = "";
      if (this.modifyPreavis) {
        // Modification de préavis
        req = this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        );
        remarqueEtapeStatut = "Retour"
      } else {
        // Création d'un nouveau préavis
        req = this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        );
        remarqueEtapeStatut = "Demande"
      }
      req
        .then(response => {
          if (response && response.data) {
            let remarqueEtape = this.lastRecord + " - " + remarqueEtapeStatut;
            
            // download courrier preavis
            if (!this.modifyPreavis) {
              this.downloadModel();
              remarqueEtape += " + fichier de demande enregistré dans le dossier de l'affaire";
            }

            // handle success
            this.$root.$emit("ShowMessage", "Le préavis au " + this.lastRecord + " a été enregistré avec succès");
            
            // log etape
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_PREAVIS_ID), remarqueEtape);
            
            this.searchAffairePreavis();
            this.clearForm();
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Fill formData pour la requête post ou put
     */
    fillData() {
      var formData = new FormData();
      formData.append("affaire_id", this.$route.params.id);
      if (this.new_preavis.service.id) {
        formData.append("service_id", this.new_preavis.service.id);
        this.lastRecord = this.new_preavis.service.nom;
      }
      if (this.new_preavis.preavis) {
        formData.append("preavis_type_id", this.new_preavis.preavis.id);
      }
      if (this.new_preavis.date_demande) {
        formData.append("date_demande",
          moment(this.new_preavis.date_demande, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }
      if (this.new_preavis.date_reponse) {
        formData.append("date_reponse",
          moment(this.new_preavis.date_reponse, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }
      if (this.new_preavis.remarque) {
        formData.append("remarque", this.new_preavis.remarque);
      }
      if (this.new_preavis.id){
        formData.append("id", this.new_preavis.id);
      }
      
      formData.append("etape", 'externe');

      return formData;
    },

    /**
     * Annuler l'édition d'état
     */
    onCancelEditPreavis: function() {
      this.clearForm();
    },

    /**
     * Clear form
     */
    clearForm() {
      this.$v.$reset();
      this.showPreavisDialog = false;
      this.new_preavis.id = null;
      this.new_preavis.service = null;
      this.new_preavis.preavis = null;
      this.new_preavis.date_demande = getCurrentDate();
      this.new_preavis.date_reponse = null;
      this.new_preavis.remarque = null;
      this.modifyPreavis = false;
    },

    /*
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      const field = this.$v.new_preavis[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    },

    /**
     * Validate form
     */
    validateForm() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.onConfirmEditPreavis();
      }
    },

    /**
     * getModel pour préavis
     */
    async downloadModel() {
      let form = {};
      
      const service_ = this.services_liste_bk.filter(x => x.id === this.new_preavis.service.id)[0];
      form.adresse_service = [
        service_.service,
        [service_.titre, service_.prenom, service_.nom].filter(Boolean).join(" ") !== ""? "À l'att. de " + [service_.titre, service_.prenom, service_.nom].filter(Boolean).join(" "): null, 
        service_.adresse,
        service_.case_postale,
        [service_.npa, service_.localite].filter(Boolean).join(" ")
      ].filter(Boolean).join("\n");

      form.adresse_demandeur = [
        this.affaire.client_commande_entreprise,
        [this.affaire.client_commande_titre, this.affaire.client_commande_prenom, this.affaire.client_commande_nom].filter(Boolean).join(" "),
        this.affaire.client_commande_adresse,
        this.affaire.client_commande_case_postale,
        [this.affaire.client_commande_npa, this.affaire.client_commande_localite].filter(Boolean).join(" ")
      ].filter(Boolean).join("\n");
      
      let observation = {
        titre: "",
        contenu: ""
      };
      if (this.new_preavis.service.id === Number(process.env.VUE_APP_SERVICE_SCAT)) {
        observation.titre = "Observation:",
        observation.contenu = "Pour autant que vous le jugiez utile, veuillez transmettre le dossier au service des forêts ou au service de la viticulture."
      }

      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("template", "Preavis");
      formData.append("service_id", this.new_preavis.service.id);
      formData.append("values", JSON.stringify({
        ADRESSE_SERVICE: form.adresse_service,
        DATE_ENVOI: String(getCurrentDate()),
        NREF: this.affaire.id,
        DATE_DEMANDE: String(this.affaire.date_ouverture),
        ADRESSE_DEMANDEUR: form.adresse_demandeur,
        CADASTRE: this.affaire.cadastre,
        CONCERNE: this.affaire.nom,
        OBSERVATION_TITRE: observation.titre,
        OBSERVATION: observation.contenu,
        ANNEXES: ""
      }));

      saveDocument(formData)
      .then(response => {
          this.$root.$emit("ShowMessage", "Le fichier '" + response.data.filename + " a été enregistré dans le dossier '" + response.data.folderpath + "' de l'affaire");
          this.$root.$emit("searchAffaireDocuments");
      })
      .catch(err => handleException(err, this));
    },

    /**
     * Open preavis dialog
     */
    openPreavisDialog() {
      this.searchServices();
      this.searchPreavisType();

      this.new_preavis = {
        id: null,
        service: null,
        preavis: null,
        date_demande: getCurrentDate(),
        date_reponse: null,
        remarque: null
      }

      this.showPreavisDialog = true;
    },

    /**
     * Delete preavis
     */
    async deletePreavis(preavis_id) {
      this.$http.delete(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_ENDPOINT + "?preavis_id=" + preavis_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.showPreavisDialog = false;
        this.searchAffairePreavis();
        this.$root.$emit("ShowMessage", "Le prévais a bien été supprimé");
      }).catch(err => handleException(err, this));
    },


    // on select table item
    onSelectTableItem(item) {
      this.selectedPreavis = item;
    },


    // reopen preavis for service externe
    async reopenPreavis(){
      let formData = new FormData();
      formData.append('id', this.new_preavis.id);
      formData.append('etape', 'externe');
      formData.append('preavis_type_id', null);
      formData.append('remarque', null);
      formData.append('date_reponse', null);
      formData.append('logstep', true);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.showPreavisDialog = false;
        this.searchAffairePreavis();
        this.$root.$emit("ShowMessage", "La demande de modification du préavis a bien été enregistrée");
      }).catch(err => handleException(err, this));
    }
  },

  mounted: function() {
    this.searchAffairePreavis();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_PREAVIS_EDITION) || this.$parent.parentAffaireReadOnly;
    
    // this.$root.$on('getPreavis', () => this.searchAffairePreavis());
    this.$root.$on('getPreavis',
      (preavis_id) => {
        this.affaire_preavis.forEach(x => {
          if (x.id === preavis_id) {
            x.unread_remarks = x.unread_remarks-1;
          }
        }
      ) 
    }
    );
  }
};
</script>
