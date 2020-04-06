<style src="./remarques.css" scoped></style>
<template src="./remarques.html"></template>


<script>
import { getCurrentDate } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'

export default {
  name: "affaireRemarques",
  props: {},
  components: {},
  data: () => ({
    affaire_remarques: [],
    showNewRemarqueBtn: false,
    new_remarque: {
      showDiv: false,
      remarque: null,
      date: null,
      operateur: null
    }
  }),

  methods: {
    /*
     * SEARCH AFFAIRE REMARQUES
     */
    async searchAffaireRemarques() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_REMARQUES_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
        )
        .then(response => {
          if (response.data) {
            this.affaire_remarques = response.data;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Ouvrir div nouvelle remarque
     */
    addRemarque: function() {
      this.new_remarque.showDiv = !this.new_remarque.showDiv;
    },

    /**
     * Enregistrer une nouvelle remarque
     */
    saveNewRemarque: function() {
      if (this.new_remarque.remarque != null) {
        var formData = new FormData();
        if (this.new_remarque.remarque)
          formData.append("remarque", this.new_remarque.remarque);
        formData.append("date", getCurrentDate());
        formData.append(
          "operateur_id",
          JSON.parse(localStorage.getItem("infolica_user")).id
        );
        formData.append("affaire_id", this.$route.params.id);

        this.$http
          .post(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_REMARQUES_ENDPOINT,
            formData,
          {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
          }
          )
          .then(response => {
            if (response.data) {
              this.searchAffaireRemarques();
            }
          })
          .catch(err => {
            handleException(err, this);
          });
      }
      this.new_remarque.showDiv = false;
      this.new_remarque.remarque = null;
    },

    /**
     * Annuler l'édition d'une nouvelle remarque
     */
    cancelNewRemarque: function() {
      this.new_remarque.showDiv = false;
      this.new_remarque.remarque = null;
    }
  },

  mounted: function() {
    this.searchAffaireRemarques();
  }
};
</script>



