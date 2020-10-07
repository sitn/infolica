<style src="./reservationNumerosMO.css" scoped></style>
<template src="./reservationNumerosMO.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import { checkPermission, getCadastres, stringifyAutocomplete } from "@/services/helper";

const moment = require("moment");

export default {
  name: "ReservationNumerosMO",
  props: {
    affaire: Object,
    typesAffaires: Object,
    types_numeros: Object
  },
  components: {},
  data: () => {
    return {
      cadastreListe: [],
      form: {},
      plansMOListe: [],
      plansMOListe_cadastre: [],
      reservationNumerosMO: [],
      showReservationNumerosMO: true,
      showReservationNumerosMODialog: false,
    };
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
          this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
        }
      })
    },


    /*
     * SEARCH reservation numeros MO by affaire_id
     */
    async searchReservationNumerosMO() {
      this.$http
      .get(
        process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RESERVATION_NUMEROS_MO_ENDPOINT + "/" +
          this.$route.params.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      )
      .then(response => {
        if (response && response.data) {
          this.reservationNumerosMO = response.data;
          this.reservationNumerosMO.forEach(x => x.nombre = x.numero_a - x.numero_de + 1);
        }
      })
      .catch(err => {
        handleException(err, this);
      });
    },

    /**
     * Recharger les numéros de plans lorsque le cadastre est modifié
     */
    changeCadastre() {
      this.form.plan = '';
      if (this.plansMOListe_cadastre !== null) {
        this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
      }
    },

    /**
     * Reset reservation
     */
    resetReservation() {
      this.showReservationNumerosMODialog = false;
      this.form = {
        cadastre: this.cadastreListe.filter(x => x.id === this.affaire.cadastre_id)[0],
        pfp3: 0,
        paux: 0,
        bat: 0,
        pdet: 0,
        dp: 0,
        plan: '',
        remarque: ''
      };
      this.plansMOListe_cadastre = stringifyAutocomplete(this.plansMOListe.filter(x => x.cadastre_id === this.form.cadastre.id), "planno", "idobj");
    },

    /**
     * On save reservation
     */
    saveReservation() {
      let promises = [];
      
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
        promises.push(this.saveReservationPromise(this.types_numeros.pdet, this.form.pdet, this.form.plan.id));
      }
      if (this.form.dp !== null && this.form.dp !== '' && Number(this.form.dp)>0) {
        promises.push(this.saveReservationPromise(this.types_numeros.dp, this.form.dp));
      }

      Promise.all(promises).then(response => {
        if (response) {
          this.searchReservationNumerosMO();
          this.showReservationNumerosMODialog = false;
          this.resetReservation();
          this.$root.$emit("ShowMessage", "Les numéros ont bien été enregistrés");
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * save Reservation Promise
     */
    async saveReservationPromise(type_points, nb_points, plan_id=null) {
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("cadastre_id", this.form.cadastre.id);
      formData.append("type_id", type_points);
      formData.append("numero_de", 1);
      formData.append("numero_a", nb_points);
      if (plan_id !== null) {formData.append("plan_id", plan_id)}
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


  },
  mounted: function() {
    this.getCadastresListe()
    this.searchReservationNumerosMO();
    this.resetReservation();
    
    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_NUMERO_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



