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
    typesAffaires_conf: {type: Object},
    types_numeros: {type: Object}
  },
  components: {},
  mixins: [validationMixin],
  data: () => {
    return {
      affaire_numeros_base: {
        DDP: null,
        PPE: null,
        PCOP: null
      },
      alertReservation: {
        show: false,
        saveReservation: false,
        text: ''
      },
      cadastre_liste: [],
      newNumeroBase: {
        showDialog: false,
        cadastre: {nom: null},
        numero: null,
        type_id: 1,
        suffixe: null
      },
      form: {
        cadastre: null,
        nombre: null,
        type_id: null,
        numeroBase: null,
        ppe_suffixe_start: null
      },
      numerosBaseListe: [],
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
      this.getNumerosBase();
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
        if (this.form.numeroBase && this.form.numeroBase.id) {
          formData.append("numero_base_id", this.form.numeroBase.id);
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
            this.$parent.searchAffaireNumeros();
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
     * Retourne les numéros en vigueur et en projet dans le cadastre sélectionné
     */
    async getNumerosBase() {
      let types = process.env.VUE_APP_NUMERO_TYPE_BF + "," + process.env.VUE_APP_NUMERO_TYPE_DDP;
      return new Promise ((resolve) => {
        if (this.affaire.type_id === this.typesAffaires_conf.pcop) {
          types += ',' + process.env.VUE_APP_NUMERO_TYPE_PPE;
        }

        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT +
          "?cadastre_id=" + this.form.cadastre.id +
          "&type_id=" + types +
          "&etat_id=" + process.env.VUE_APP_NUMERO_PROJET_ID + "," +  process.env.VUE_APP_NUMERO_VIGUEUR_ID,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.numerosBaseListe = stringifyAutocomplete(response.data, "numero_sitn");
            resolve(response);
          }
        }).catch(err => handleException(err, this));
      })
    },


    /**
     * createNumeroBase()
     */
    createNumeroBase() {
      this.newNumeroBase = {
        cadastre: this.form.cadastre,
        numero: null,
        type_id: 1,
        suffixe: null
      };

      this.showReservationDialog = false;
      this.newNumeroBase.showDialog = true;
    },

    /**
     * create Numero base
     */
    async onConfirmCreateNumeroBase() {
      var formData = new FormData();
      formData.append("cadastre_id", this.newNumeroBase.cadastre.id);
      formData.append("numero", this.newNumeroBase.numero);
      formData.append("type_id", this.newNumeroBase.type_id);
      formData.append("etat_id", Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID));
      if (this.newNumeroBase.suffixe) {
        formData.append("suffixe", this.newNumeroBase.suffixe);
      }

      // Enregistrer le numéro
      this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => {
          if (response.data) {
            this.$root.$emit('ShowMessage', "Le numéro " +  this.newNumeroBase.numero + " a été créé sur le cadastre de " + this.newNumeroBase.cadastre.nom + " avec succès");
            this.getNumerosBase().then(() => this.form.numeroBase = this.numerosBaseListe.filter(x => x.nom === this.newNumeroBase.numero)[0]);
          }
        }).catch(err => handleException(err, this));

      this.showReservationDialog = true;
      this.newNumeroBase.showDialog = false;
    },

    /**
     * cancel create Numero base
     */
    onCancelCreateNumeroBase() {
      this.newNumeroBase = {
        cadastre: {nom: null},
        numero: null,
        type_id: 1,
        suffixe: null
      };

      this.showReservationDialog = true;
      this.newNumeroBase.showDialog = false;
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
  }
};
</script>

