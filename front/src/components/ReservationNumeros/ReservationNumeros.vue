<style src="./reservationNumeros.css" scoped></style>
<template src="./reservationNumeros.html"></template>


<script>
import { getCadastres, stringifyAutocomplete } from "@/services/helper";
import { handleException } from "@/services/exceptionsHandler";
import { validationMixin } from "vuelidate";
import { required, minValue } from "vuelidate/lib/validators";

export default {
  name: "ReservationNumeros",
  props: {
    affaire: {type: Object}
  },
  components: {},
  mixins: [validationMixin],
  data: () => {
    return {
      showReservationDialog: false,
      cadastre_liste: [],
      affaire_numeros_base: {
        DDP: null,
        PPE: null,
        PCOP: null
      },
      form: {
        cadastre: null,
        nombre: null,
        type_id: null,
      },
      alertReservation: {
        show: false,
        saveReservation: false,
        text: ''
      }
    };
  },

  // Validations
  validations() {
    var form = {
      cadastre: { required },
      nombre: { 
        required,
        minValue: minValue(1)
      }
    };

    // if (this.reservation.nb_ddp > 0) {
    //   reservation.ddp_base = { required };
    // }
    // if (this.reservation.nb_ppe > 0) {
    //   reservation.ppe_base = { required };
    //   reservation.ppe_suffixe_start = { required };
    // }
    // if (this.reservation.nb_pcop > 0) {
    //   reservation.pcop_base = { required };
    // }

    return { form };
  },

  methods: {
    /*
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = stringifyAutocomplete(response.data);
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Retourne tous les numéros concernés par l'affaire
     * Possibilité de filtrer en fonction du type de numéros
     */
    filterAffaireNumeros() {
      this.affaire_numeros = this.$parent.affaire_numeros_all;

      // Pour les DDP
      this.affaire_numeros_base.DDP = this.affaire_numeros.filter(x => {
        return (
          (x.numero_type === "Bien-fonds") |
          (x.numero_type === "Droit distinct et permanent (DDP)")
        );
      });
      // Pour les PPE et les DDP
      this.affaire_numeros_base.PPE = this.affaire_numeros.filter(x => {
        return (
          (x.numero_type === "Bien-fonds") |
          (x.numero_type === "Droit distinct et permanent (DDP)")
        );
      });
      // Pour les PCOP
      this.affaire_numeros_base.PCOP = this.affaire_numeros.filter(x => {
        return (
          (x.numero_type === "Bien-fonds") |
          (x.numero_type === "Droit distinct et permanent (DDP)") |
          (x.numero_type === "Unité de PPE")
        );
      });
    },

    /**
     * Open reservation numéros dialog
     */
    openReservationDialog() {
      this.initializeForm();
      this.showReservationDialog = true;
    },

    /**
     * Create numeros
     */
    saveReservationNumeros() {
      var formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("nombre", this.form.nombre);
      formData.append("cadastre_id", this.form.cadastre.id);
      formData.append("etat_id", Number(process.env.VUE_APP_NUMERO_PROJET_ID));
      
      //Type de numéro selon le type d'affaire
      if (this.affaire.type_id === Number(process.env.VUE_APP_TYPE_AFFAIRE_DIVISION)) {
        this.form.type_id = Number(process.env.VUE_APP_NUMERO_TYPE_BF);
      }
      formData.append("type_id", this.form.type_id);
      
      this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_RESERVATION_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response.data) {
            this.$parent.searchAffaireNumeros();
            this.$parent.searchAffaireNewNumerosMo();
            this.$root.$emit("ShowMessage", "Le(s) numéro(s) réservé(s) ont été correctement rattaché(s) à l'affaire")
          }
        })
        .catch(err => {
          handleException(err, this);
        });
      // this.showReservationDialog = false;
      this.initializeForm();
    },

    /**
     * Annuler la réservation de uméros
     */
    onCancelReservationNumeros() {
      this.showReservationDialog = false;
      this.initializeForm();
    },

    /**
     * Initialise le formulaire de réservation de numéros
     */
    initializeForm() {
      this.form.cadastre = this.cadastre_liste.filter(x => x.id === this.affaire.cadastre_id).pop();
      this.form.nombre = 0;
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
     * Confirmer l'édition de la facture et l'enregistrer
     */
    onConfirmReservationNumeros() {
      
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.showReservationDialog = false;
      
        this.form.nombre = Number(this.form.nombre);
        if (this.form.nombre >= 10) {
          this.alertReservation.text = "En cliquant sur 'confirmer', " + this.form.nombre + " numéros de bien-fonds vont être réservés."
          this.alertReservation.show = true;
        } else {
          this.saveReservationNumeros();
        }
      }
    }
  },

  mounted: function() {
    this.initCadastresList();
  }
};
</script>

