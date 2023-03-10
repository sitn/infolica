<style src="./newStepSetter.css" scoped></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./newStepSetter.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "NewStepSetter",
  props: {
    affaire_id: {
      type: Number,
    }
  },
  data: () => {
    return {
      actual_step: null,
      etapes: [],
      new_step_id: null
    };
  },

  methods: {
    async getActualAffaireEtape() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPE_INDEX_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.affaire_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        this.actual_step = response.data.etape;
        this.new_step_id = response.data.predicted_next_step_id;
      }).catch(err => handleException(err, this));
    },
    
    
    async getAffaireEtapes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPES_INDEX_ENDPOINT,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        this.etapes = response.data;
      }).catch(err => handleException(err, this));
    },

    newStepSelected(value) {
      this.$emit('new-step-selected', value);
    }

  },
  mounted: function() {
    this.getAffaireEtapes();
    this.getActualAffaireEtape();
  }
};

</script>
