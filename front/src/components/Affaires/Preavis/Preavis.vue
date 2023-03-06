<style src="./preavis.css" scoped></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./preavis.html"></template>


<script>
import { getCurrentDate, checkPermission, logAffaireEtape } from "@/services/helper";
import PreavisEditComments from "@/components/PreavisExternes/PreavisExternesEditComments.vue";
import PreavisEditDecision from "@/components/PreavisExternes/PreavisExternesEditDecision.vue";
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
      modifyPreavis: false,
      new_preavis: {
        id: null,
        service: null,
        date_demande: getCurrentDate(),
        remarque_conversation: null
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
      // this.new_preavis.remarque = curr_preavis.remarque;
      this.new_preavis.service = this.services_liste
        .filter(data => data.nom === curr_preavis.service)
        .map(x => ({
          id: x.id,
          nom: x.nom,
          toLowerCase: () => x.nom.toLowerCase(),
          toString: () => x.nom
        }))[0];
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
      if (this.new_preavis.date_demande) {
        formData.append("date_demande",
          moment(this.new_preavis.date_demande, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));
      }
      if (this.new_preavis.id){
        formData.append("id", this.new_preavis.id);
      }
      
      if (this.new_preavis.remarque_conversation){
        formData.append("remarque_conversation", this.new_preavis.remarque_conversation);
      }
      
      formData.append("operateur_sgrf_id", JSON.parse(localStorage.getItem("infolica_user")).id);
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
      this.new_preavis.remarque_conversation = null;
      this.new_preavis.date_demande = getCurrentDate();
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
     * Open preavis dialog
     */
    openPreavisDialog() {

      this.new_preavis = {
        id: null,
        service: null,
        date_demande: getCurrentDate(),
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
    },
    
    
    async onExportPreavisPDF(preavis) {
      let formData = new FormData();
      formData.append('preavis_id', preavis.id)

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_PRINT_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"},
          responseType: "blob"
        }
        ).then(response => {
          let fileURL = window.URL.createObjectURL(new Blob([response.data]));
          let fileLink = document.createElement('a');
        
          fileLink.href = fileURL;
          let header_content_type = response.headers['content-type'];
          let filename = undefined;
          for (let item of header_content_type.split(';')){
            item = item.trim(); 
            if (item.startsWith('filename=')) {
              filename = item.replace('filename=', '').replaceAll('"', '');
              break
            }
          }
          fileLink.setAttribute('download', filename);
          document.body.appendChild(fileLink);
          fileLink.click();

          this.$root.$emit("ShowMessage", "Le préavis a bien été téléchargé");
      }).catch (err => handleException(err, this));
    }
  },

  mounted: function() {
    this.searchAffairePreavis();
    this.searchServices();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_PREAVIS_EDITION) || this.$parent.parentAffaireReadOnly;
    
    // this.$root.$on('getPreavis', () => this.searchAffairePreavis());
    this.$root.$on('getPreavis',
      (preavis_id) => {
        this.affaire_preavis.forEach(x => {
          if (x.id === preavis_id) {
            x.unread_remarks = x.unread_remarks-1;
          }
        }
      );
    }
    );
  }
};
</script>
