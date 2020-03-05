<style src="./reservationNumeros.css" scoped></style>
<template src="./reservationNumeros.html"></template>


<script>
import { checkLogged, getCadastres } from "@/services/helper";

export default {
  name: "ReservationNumeros",
  props: {
    showReservationDialog: Boolean,
    affaire_id: Number
  },
  components: {},
  data: () => {
    return {
      cadastre_liste: [],
      types_numeros: [],
      etats_numeros: [],
      reservation: {
        cadastre: "",
        nb_bf: 0,
        nb_ddp: 0,
        nb_ppe: 0,
        ppe_suffixe_start: null,
        nb_pcop: 0,
        nb_pfp3: 0,
        nb_paux: 0,
        nb_bat: 0,
        nb_pcs: 0,
        plan_id: null
      }
    };
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
          alert("error: " + err.message);
        });
    },

    /**
     * Create numeros
     */
    onConfirmReservationNumeros() {
      var formData = new FormData();
      if (this.reservation.cadastre.id)
        formData.append("cadastre_id", this.reservation.cadastre.id);
      if (this.affaire_id) formData.append("affaire_id", this.affaire_id);
      if (this.reservation.nb_bf) formData.append("bf", this.reservation.nb_bf);
      if (this.reservation.nb_ddp)
        formData.append("ddp", this.reservation.nb_ddp);
      if (this.reservation.nb_ppe)
        formData.append("ppe", this.reservation.nb_ppe);
      if (this.reservation.ppe_suffixe_start)
        formData.append("ppe_unite", this.reservation.ppe_suffixe_start);
      if (this.reservation.nb_pcop)
        formData.append("pcop", this.reservation.nb_pcop);
      if (this.reservation.nb_pfp3)
        formData.append("pfp3", this.reservation.nb_pfp3);
      if (this.reservation.nb_paux)
        formData.append("paux", this.reservation.nb_paux);
      if (this.reservation.nb_bat)
        formData.append("bat", this.reservation.nb_bat);
      if (this.reservation.nb_pcs)
        formData.append("pcs", this.reservation.nb_pcs);
      if (this.reservation.plan_id)
        formData.append("plan_id", this.reservation.plan_id);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RESERVATION_NUMEROS_ENDPOINT,
          formData
        )
        .then(response => {
          if (response.data) {
            this.$emit("confirmReserveNumeros");
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
      this.onCancelReservationNumeros();
    },

    /**
     * Cancel creation of numeros
     */
    onCancelReservationNumeros() {
      this.reservation.cadastre = "";
      this.reservation.nb_bf = 0;
      this.reservation.nb_ppe = 0;
      this.reservation.ppe_suffixe_start = null;
      this.reservation.nb_pcop = 0;
      this.reservation.nb_pfp3 = 0;
      this.reservation.nb_paux = 0;
      this.reservation.nb_bat = 0;
      this.reservation.nb_pcs = 0;
      this.reservation.plan_id = null;
      this.$emit("closeReservationDialog");
    }
  },

  mounted: function() {
    checkLogged();
    this.initCadastresList();
  }
};
</script>

