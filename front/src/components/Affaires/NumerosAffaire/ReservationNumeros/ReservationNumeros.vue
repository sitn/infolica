<style src="./reservationNumeros.css" scoped></style>
<template src="./reservationNumeros.html"></template>


<script>
import { getCadastres, stringifyAutocomplete, getTypesNumeros } from "@/services/helper";
import { handleException } from "@/services/exceptionsHandler";
import { validationMixin } from "vuelidate";
import { required, minValue } from "vuelidate/lib/validators";

export default {
  name: "ReservationNumeros",
  props: {
    affaire: {type: Object},
    numerosBaseListe: {type: Array},
    typesAffaires_conf: {type: Object},
    types_numeros: {type: Object}
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
      cadastre_liste: [],
      form: {
        cadastre: null,
        nombre: null,
        type_id: null,
        numeroBase: null,
        ppe_suffixe_start: null
      },
      numeroTypesList: [],
      showReservationDialog: false
    };
  },

  // Validations
  validations() {
    // Réservation de numéros
    let form = {
      cadastre: { required },
      nombre: { 
        required,
        minValue: minValue(1)
      }
    };
    if ([this.typesAffaires_conf.ppe, this.typesAffaires_conf.pcop, this.typesAffaires_conf.modification_ppe].includes(this.affaire.type_id)) {
      form.numeroBase = { required };
    }

    if ([this.typesAffaires_conf.ppe, this.typesAffaires_conf.modification_ppe].includes(this.affaire.type_id)) {
      form.ppe_suffixe_start = { required };
    }

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

    /**
     * Open reservation numéros dialog
     */
    openReservationDialog() {
      this.initializeForm();

      // set default selection for base number
      if (this.numerosBaseListe.length>0) {
        this.form.numeroBase = this.numerosBaseListe[0];
      }

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
      if ((this.affaire.type_id === this.typesAffaires_conf.ppe || this.affaire.type_id === this.typesAffaires_conf.pcop)) {
        if (this.form.numeroBase && this.form.numeroBase.numero_id) {
          formData.append("numero_base_id", this.form.numeroBase.numero_id);
        } else {
          this.$root.$emit("ShowError", "Le numéro de base a été mal saisi. Il faut le sélectioner dans la liste (pas seulement l'écrire).");
          return;
        }
      }
      if (this.affaire.type_id === this.typesAffaires_conf.ppe && this.form.ppe_suffixe_start !== null) {
        formData.append("ppe_suffixe_start", this.form.ppe_suffixe_start);
      }
      
      //Type de numéro selon le type d'affaire
      if (this.affaire.type_id === this.typesAffaires_conf.mutation) {
        this.form.type_id = Number(process.env.VUE_APP_NUMERO_TYPE_BF);
      } else {
        this.form.type_id = Number(this.affaire.reservation_numeros_types_id[0]);
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
            this.$root.$emit("searchAffaireNumeros");
            this.$root.$emit("ShowMessage", "Le(s) numéro(s) réservé(s) ont été correctement rattaché(s) à l'affaire")
          }
        })
        .catch(err => {
          handleException(err, this);
        });
      this.showReservationDialog = false;
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
      this.form.numeroBase = null;
      this.form.ppe_suffixe_start = null;
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
     * Confirmer l'édition de la réservation et l'enregistrer
     */
    onConfirmReservationNumeros() {
      
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.form.nombre = Number(this.form.nombre);
        if (this.form.nombre >= 10) {
          this.alertReservation.text = "En cliquant sur 'confirmer', " + this.form.nombre + " numéros de bien-fonds vont être réservés."
          this.alertReservation.show = true;
        } else {
          this.saveReservationNumeros();
        }
      }
    },

    /**
     * init type numeros list
     */
    async initTypeNumerosList() {
      getTypesNumeros()
      .then(response => {
        if (response && response.data) {
          this.numeroTypesList = stringifyAutocomplete(response.data);
        }
      }).catch(err => handleException(err, this));
    }

  },

  mounted: function() {
    this.initCadastresList();
    this.initTypeNumerosList();
    console.log(this.numerosBaseListe);
  }
};
</script>

