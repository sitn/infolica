<style src="./numerosAffaire.css" scoped></style>
<template src="./numerosAffaire.html"></template>


<script>
import { checkLogged } from "@/services/helper";
import ReservationNumeros from "@/components/ReservationNumeros/ReservationNumeros.vue";

export default {
  name: "NumerosAffaire",
  props: {},
  components: {
    ReservationNumeros
  },
  data: () => {
    return {
      affaire_id: null,
      affaire_numeros: [],
      showReservationDialog: false
    };
  },

  methods: {
    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT +
            this.$route.params.id
        )
        .then(response => {
          if (response.data) {
            this.affaire_numeros = response.data;
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenNumero(id) {
      window.setTimeout;
      let routeData = this.$router.resolve("/numeros/" + id);
      window.open(routeData.href, "_blank");
    },

    /**
     * Ouvrir la boîte de dialogue de réservation de numéros
     */
    callOpenReservationDialog() {
      this.affaire_id = Number(this.$route.params.id);
      this.$refs.form.openReservationDialog()
    },
  },

  mounted: function() {
    checkLogged();
    this.searchAffaireNumeros();
  }
};
</script>



