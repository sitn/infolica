<style src="./numerosAffaire.css" scoped></style>
<template src="./numerosAffaire.html"></template>


<script>
import { checkLogged } from "@/services/helper";
import ReferenceNumeros from "@/components/ReferenceNumeros/ReferenceNumeros.vue";
import ReservationNumeros from "@/components/ReservationNumeros/ReservationNumeros.vue";

export default {
  name: "NumerosAffaire",
  props: {},
  components: {
    ReferenceNumeros,
    ReservationNumeros
  },
  data: () => {
    return {
      affaire_id: null,
      affaire_numeros_anciens: [],
      affaire_numeros_nouveaux: [],
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
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.affaire_numeros_nouveaux = response.data.filter(
              x => x.affaire_numero_type === "Nouveau"
            );
            this.affaire_numeros_anciens = response.data.filter(
              x => x.affaire_numero_type === "Ancien"
            );
            this.affaire_numeros_nouveaux.forEach(function(element) {
              if (element.numero_etat === "Abandonné") element.active = false;
              else if (element.numero_etat === "Projet") element.active = true;
            });
          }
        })
        .catch(err => {
          alert("error : " + err.message);
        });
    },

    /**
     * Supprimer numéro référencé
     */
    onDeleteReferenceNumero(numero_id) {
      // var formData = new FormData()
      // formData.append("affaire_id", this.$route.params.id)
      // formData.append("numero_id", numero_id)



      this.$http
        .delete(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_REFERENCE_NUMEROS_ENDPOINT + "?affaire_id=" + this.$route.params.id + "&numero_id=" + numero_id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.searchAffaireNumeros();
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
    },



    /**
     * Abandonner/rétablir un numéro réservé
     */
    onDeleteReserveNumero(numero_id) {
      // get numéro pour l'update
      var numero_ = {};
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_ENDPOINT +
            numero_id,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            }
        )
        .then(response => {
          if (response.data) {
            numero_ = response.data;
            this.updateNumero(numero_);
          }
        })
        .catch(err => {
          alert("error: " + err.message);
        });
    },

    /**
     * Update Numero
     */
    async updateNumero(numero_) {
      this.$http
        .delete(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_ENDPOINT +
          numero_.id,
        {
          withCredentials: true,
          headers: {'Accept': 'application/json'}
        }
        )
        .then(response => {
          if (response && response.status === 200) {
            this.searchAffaireNumeros();
          }
        })
        .catch(err => {
          alert("error: " + err.message);
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
     * Ouvrir la boîte de dialogue de référence de numéros
     */
    callOpenReferenceDialog() {
      this.$refs.formReference.openReferenceDialog();
    },

    /**
     * Ouvrir la boîte de dialogue de réservation de numéros
     */
    callOpenReservationDialog() {
      this.affaire_id = Number(this.$route.params.id);
      this.$refs.formReservation.openReservationDialog();
    }
  },

  mounted: function() {
    checkLogged();
    this.searchAffaireNumeros();
  }
};
</script>



