<style src="./remarques.css" scoped></style>
<template src="./remarques.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: "AffairesDashboard",
  props: {},
  components: {},
  data: () => ({
    affaire_remarques: [],
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
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.affaire_remarques = response.data
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },

  },

  mounted: function() {
    checkLogged();
    this.searchAffaireRemarques();
  }
};
</script>



