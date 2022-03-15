<style src="./reservationNumerosMO.css" scoped></style>
<template src="./reservationNumerosMO.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import { getCadastres, stringifyAutocomplete, logAffaireEtape } from "@/services/helper";
import { validationMixin } from "vuelidate";
import { required, minValue, requiredIf } from "vuelidate/lib/validators";

const moment = require("moment");

export default {
  name: "ReservationNumerosMO",
  props: {
    affaire: Object,
    types_numeros: Object,
    permission: Object
  },
  components: {},
  mixins: [validationMixin],
  data: () => {
    return {
      alertReservation: {
        show: false,
        saveReservation: false,
        text: ''
      },
      cadastreListe: [],
      form: {},
      filterTableParams: {
        dateRange: {
          startDate: null, 
          endDate: moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        },
        selectedCadastre_id: -1,
        showProgressBar: true,
      },
      plansMOListe: [],
      plansMOListe_cadastre: [],
      reservationNumerosMO: [],
      showReservationNumerosMO: true,
      showReservationNumerosMODialog: false,
      reservationNumerosMODialog_errorMsg: "",
      warningMessage: "",
    };
  },

  // Validations
  validations() {
    let form = {
      cadastre: {required},
      pfp3: {
        required,
        minValue: minValue(0)
      },
      paux: {
        required,
        minValue: minValue(0)
      },
      bat: {
        required,
        minValue: minValue(0)
      },
      pdet: {
        required,
        minValue: minValue(0)
      },
      dp: {
        required,
        minValue: minValue(0)
      }
    }

    form.plan_id = {
      required: requiredIf(function() {return this.form.pdet > 0}), 
    }


    return { form };
  },

  methods: {
    /**
     * Get cadastres
     */
    async getCadastresListe() {
      getCadastres().then(response => {
        if (response && response.data) {
            this.cadastreListe = stringifyAutocomplete(response.data);
            this.form.cadastre = this.cadastreListe.filter(x => x.id === this.affaire.cadastre_id)[0];

            // Récupère les plans de la MO
            this.getPlansMO();
          }
        }).catch(err => handleException(err, this))
    },


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
          if (this.form.cadastre && this.form.cadastre.id && this.form.cadastre.id > 0) {
            this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
          }
        }
      })
    },


    /*
     * SEARCH reservation numeros MO by affaire_id
     */
    async searchReservationNumerosMO(params={}) {
      //set search criteria
      let searchParams = [];
      for (let key in params) {
        searchParams.push(key + "=" + params[key]);
      }
      if (searchParams.length > 0) {
        searchParams = "?" + searchParams.join("&");
      } else {
        this.warningMessage = "Seules les 20 dernières réservations sont affichées. Pour en voir plus, utiliser les critères de recherche ci-dessus";
      }

      this.$http
      .get(
        process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RESERVATION_NUMEROS_MO_ENDPOINT + "/" +
          this.affaire.id + searchParams,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      )
      .then(response => {
        if (response && response.data) {
          let tmp = response.data;
          tmp.forEach(x => {
            x.nombre = x.numero_a - x.numero_de + 1;
            x.date = moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            x.date_sort = new Date(moment(x.date, process.env.VUE_APP_DATEFORMAT_CLIENT)).getTime();
          });

          this.reservationNumerosMO = tmp;
        }
      })
      .catch(err => {
        handleException(err, this);
      });

      this.filterTableParams.showProgressBar = false;
    },

    /**
     * Recharger les numéros de plans lorsque le cadastre est modifié
     */
    changeCadastre() {
      this.form.plan_id = null;
      if (this.plansMOListe_cadastre !== null) {
        this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
      }
    },

    /**
     * Reset reservation
     */
    resetReservation() {
      this.showReservationNumerosMODialog = false;
      
      let affaireCadastre = {id: null, nom: null, toLowerCase: () => "", toString: () => ""};
      if (this.affaire.cadastre_id > 0) {
        affaireCadastre = this.cadastreListe.filter(x => x.id === this.affaire.cadastre_id)[0];
      }
      
      this.form = {
        cadastre: affaireCadastre,
        pfp3: 0,
        paux: 0,
        bat: 0,
        pdet: 0,
        dp: 0,
        plan_id: null,
        remarque: ''
      };
      this.reservationNumerosMODialog_errorMsg = "";
      this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
    },

    /**
     * on save reservation, if large amount of numbers
     */
    saveReservation() {
      let plan = ""
      if (this.form.plan_id){
        plan = this.plansMOListe_cadastre.filter(x => x.id === this.form.plan_id)[0];
      }

      this.alertReservation.text = "<p>Cadastre: " + this.form.cadastre.nom + "</p>";
      if (Number(this.form.pfp3) > 0) {
        this.alertReservation.text += "<p>PFP3: " + this.form.pfp3 + "</p>";
      }
      if (Number(this.form.paux) > 0) {
        this.alertReservation.text += "<p>Points auxiliaires: " + this.form.paux + "</p>";
      }
      if (Number(this.form.bat) > 0) {
        this.alertReservation.text += "<p>Bâtiments: " + this.form.bat + "</p>";
      }
      if (Number(this.form.pdet) > 0) {
        this.alertReservation.text += "<p>Points de détail sur plan " + plan + ": " + this.form.pdet + "</p>";
      }
      if (Number(this.form.dp) > 0) {
        this.alertReservation.text += "<p>Domaines publics: " + this.form.dp + "</p>";
      }
      this.alertReservation.show = true;
    },

    /**
     * On confirm save reservation
     */
    async confirmSaveReservation() {
      let promises = [];
      let plan = ""
      if (this.form.plan_id){
        plan = this.plansMOListe_cadastre.filter(x => x.id === this.form.plan_id)[0];
      }
      
      if (this.form.pfp3 !== null && this.form.pfp3 !== '' && Number(this.form.pfp3)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.pfp3, this.form.pfp3));
      }
      if (this.form.paux !== null && this.form.paux !== '' && Number(this.form.paux)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.paux, this.form.paux));
      }
      if (this.form.bat !== null && this.form.bat !== '' && Number(this.form.bat)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.bat, this.form.bat));
      }
      if (this.form.pdet !== null && this.form.pdet !== '' && Number(this.form.pdet)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.pdet, this.form.pdet, plan, this.form.plan_id));
      }
      if (this.form.dp !== null && this.form.dp !== '' && Number(this.form.dp)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.dp, this.form.dp));
      }

      Promise.all(promises).then(response => {
        if (response) {
          this.filterTable();
          this.showReservationNumerosMODialog = false;
          this.$root.$emit("ShowMessage", "Les numéros ont bien été enregistrés");
          
          let plan = ""
          if (this.form.plan_id){
            plan = this.plansMOListe_cadastre.filter(x => x.id === this.form.plan_id)[0];
          }
          //Log edition facture
          let comment = ["Cadastre: " + this.form.cadastre.nom,
                         Number(this.form.pfp3) > 0? this.form.pfp3 + " PFP3": null,
                         Number(this.form.paux) > 0? this.form.paux + " point(s) auxiliaire(s)": null,
                         Number(this.form.bat) > 0? this.form.bat + " bâtiment(s)": null,
                         Number(this.form.pdet) > 0? this.form.pdet + " point(s) de détail sur plan " + plan: null,
                         Number(this.form.dp) > 0? this.form.dp + " domaine(s) public(s)": null].filter(Boolean).join(", ");
          logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_RESERVATION_NUMEROS_MO_ID), comment);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * save Reservation Promise
     */
    async saveReservationPromise(type_points, nb_points, plan=0, plan_id=null) {
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("cadastre_id", this.form.cadastre.id);
      formData.append("type_id", type_points);
      formData.append("numero_de", 1);
      formData.append("numero_a", nb_points);
      formData.append("plan", plan);
      if (plan_id !== null) { formData.append("plan_id", plan_id) }
      formData.append("date", moment(new Date).format(process.env.VUE_APP_DATEFORMAT_WS));
      if (this.form.remarque !== null && this.form.remarque !== '') {formData.append("remarque", this.form.remarque)}
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RESERVATION_NUMEROS_MO_ENDPOINT,
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
     * Validation du formulaire avant de l'enregistrer
     */
    validationReservation() {
      
      this.$v.$touch();

      if (!this.$v.$invalid) {

        if ((this.form.pfp3 === 0 || this.form.pfp3 === "0") && (this.form.paux === 0 || this.form.paux === "0") && (this.form.bat === 0 || this.form.bat === "0") && (this.form.pdet === 0 || this.form.pdet === "0") && (this.form.dp === 0 || this.form.dp === "0")) {
          this.reservationNumerosMODialog_errorMsg = "Aucun numéro à réserver...";
          return;
        } else {
          this.reservationNumerosMODialog_errorMsg = "";
        }

        this.showReservationDialog = false;
        this.saveReservation();
      }
    },

    /**
     * Filter table
     */
    filterTable() {
      this.warningMessage = "";
      this.filterTableParams.showProgressBar = true;
      setTimeout(() => {
        this.reservationNumerosMO = [{}];
        let params = {};
        // filter by cadastre
        if (this.filterTableParams.selectedCadastre_id > 0) {
          params.cadastre_id = this.filterTableParams.selectedCadastre_id;
        }
  
        if (this.filterTableParams.dateRange) {
          if (this.filterTableParams.dateRange.startDate) {
            params.startDate = moment(this.filterTableParams.dateRange.startDate, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
          } else {
            if (this.filterTableParams.selectedCadastre_id < 0) {
              this.warningMessage = "Seules les 20 dernières réservations sont affichées. Pour en voir plus, sélectionner un cadastre ou une date de départ.";
            }
          }
          if (this.filterTableParams.dateRange.endDate) {
            params.endDate = moment(this.filterTableParams.dateRange.endDate, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS);
          }
        }
        
        this.searchReservationNumerosMO(params);
      }, 2000); //experimental value
    },


    disabledStartDates (date) {
      if (this.filterTableParams.dateRange.endDate && moment(this.filterTableParams.dateRange.endDate, process.env.VUE_APP_DATEFORMAT_CLIENT)) {
        return date > moment(this.filterTableParams.dateRange.endDate, process.env.VUE_APP_DATEFORMAT_CLIENT) || date > new Date();
      }
      if (date > new Date()) {
        return true;
      }
      return false;
    },

    disabledEndDates (date) {
      if (this.filterTableParams.dateRange.startDate && moment(this.filterTableParams.dateRange.startDate, process.env.VUE_APP_DATEFORMAT_CLIENT)) {
        return date < moment(this.filterTableParams.dateRange.startDate, process.env.VUE_APP_DATEFORMAT_CLIENT) || date > new Date();
      }
      if (date > new Date()) {
        return true;
      }
      return false;
    },

    /**
     * Open reservation dialog
     */
    openReservationDialog() {
      this.resetReservation();
      this.showReservationNumerosMODialog = true;
    }

  },
  mounted: function() {
    this.getCadastresListe()
    this.searchReservationNumerosMO();
    this.resetReservation(); 
  }
};
</script>



