<style src="./reservationNumeros.css" scoped></style>
<template src="./reservationNumeros.html"></template>


<script>
import { getCadastres } from "@/services/helper";
import { handleException } from "@/services/exceptionsHandler";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  name: "ReservationNumeros",
  props: {},
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
      reservation: {
        affaire_id: null,
        cadastre: null,
        nb_bf: 0,
        nb_ddp: 0,
        ddp_base: null,
        nb_ppe: 0,
        ppe_suffixe_start: null,
        ppe_base: 0,
        nb_pcop: 0,
        pcop_base: 0,
        nb_pfp3: 0,
        nb_paux: 0,
        nb_bat: 0,
        nb_dp: 0,
        nb_pcs: 0,
        plan_id: null
      }
    };
  },

  // Validations
  validations() {
    var reservation = {
      cadastre: { required }
    };
    
    if (this.reservation.nb_ddp > 0) reservation.ddp_base = { required };
    if (this.reservation.nb_ppe > 0) {
      reservation.ppe_base = { required };
      reservation.ppe_suffixe_start = { required };
    }
    if (this.reservation.nb_pcop > 0) reservation.pcop_base = { required };

    return { reservation };
  },

  methods: {
    /*
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = response.data.map(x => ({
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
     * Init default cadastre
     */
    async initDefaultCadastre() {
      return new Promise((resolve, reject) => {
        var affaire_cadastre;

        this.$http
          .get(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRES_ENDPOINT +
              this.$route.params.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response && response.data) {
              affaire_cadastre = {
                id: response.data.cadastre_id,
                nom: response.data.cadastre,
                toLowerCase: () => response.data.cadastre.toLowerCase(),
                toString: () => response.data.cadastre
              };
            }
            resolve(affaire_cadastre);
          })
          .catch(() => reject);
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
      if (this.reservation.cadastre.id)
        formData.append("cadastre_id", this.reservation.cadastre.id);
      formData.append("affaire_id", this.$route.params.id);
      if (this.reservation.nb_bf) formData.append("bf", this.reservation.nb_bf);
      if (this.reservation.nb_ddp)
        formData.append("ddp", this.reservation.nb_ddp);
      if (this.reservation.ddp_base)
        formData.append("ddp_base", this.reservation.ddp_base);
      if (this.reservation.nb_ppe)
        formData.append("ppe", this.reservation.nb_ppe);
      if (this.reservation.ppe_suffixe_start)
        formData.append("ppe_unite", this.reservation.ppe_suffixe_start);
      if (this.reservation.ppe_base)
        formData.append("ppe_base", this.reservation.ppe_base);
      if (this.reservation.nb_pcop)
        formData.append("pcop", this.reservation.nb_pcop);
      if (this.reservation.pcop_base)
        formData.append("pcop_base", this.reservation.pcop_base);
      if (this.reservation.nb_pfp3)
        formData.append("pfp3", this.reservation.nb_pfp3);
      if (this.reservation.nb_paux)
        formData.append("paux", this.reservation.nb_paux);
      if (this.reservation.nb_bat)
        formData.append("bat", this.reservation.nb_bat);
      if (this.reservation.nb_dp)
        formData.append("dp", this.reservation.nb_dp);
      if (this.reservation.nb_pcs)
        formData.append("pcs", this.reservation.nb_pcs);
      if (this.reservation.plan_id)
        formData.append("plan_id", this.reservation.plan_id);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RESERVATION_NUMEROS_ENDPOINT,
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
            this.$root.$emit("ShowMessage", "Le(s) numéro(s) réservé(s) ont été correctement ajouté(s) à l'affaire")
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
      alert(this.reservation.ddp_base);
      this.showReservationDialog = false;
      this.initializeForm();
    },

    /**
     * Initialise le formulaire de réservation de numéros
     */
    async initializeForm() {
      this.reservation.cadastre = await this.initDefaultCadastre();
      this.reservation.nb_bf = 0;
      this.reservation.nb_ddp = 0;
      this.reservation.ddp_base = null;
      this.reservation.nb_ppe = 0;
      this.reservation.ppe_suffixe_start = null;
      this.reservation.ppe_base = null;
      this.reservation.nb_pcop = 0;
      this.reservation.pcop_base = null;
      this.reservation.nb_pfp3 = 0;
      this.reservation.nb_paux = 0;
      this.reservation.nb_bat = 0;
      this.reservation.nb_dp = 0;
      this.reservation.nb_pcs = 0;
      this.reservation.plan_id = null;
      this.filterAffaireNumeros();
    },

    /**
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      const field = this.$v.reservation[fieldName];

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
        this.saveReservationNumeros();
      }
    }
  },

  mounted: function() {
    this.initCadastresList();
  }
};
</script>

