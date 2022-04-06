<style src="./preavisEditDecision.css" scoped></style>
<template src="./preavisEditDecision.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "PreavisEditDecision",
  props: {
    affaire: Object
  },
  components: {},
  data() {
    return {
      decisions_liste: [],
      decision: {
        preavis_type_id: null,
        remarque: null,
        desabled: true,
        show: false,
      },
    };
  },

  methods: {
    /**
     * open new decision
     */
    openNewDecision() {
      this.resetDecision();
      this.decision.disabled = null;
      this.decision.show = true;

    },


    // reset decision
    resetDecision() {
      this.decision.preavis_type_id = null;
      this.decision.remarque = null;
      this.decision.operateur = null;
      this.decision.date = null;
    },


    // get Decision List for menu
    async getDecisionList() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_LIST_BY_AFFAIRE_ID_ENDPOINT + "?preavis_id=" + this.affaire.preavis_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.decisions_liste = response.data;
        }
      }
      ).catch(err => handleException(err));
    },


    // get Decision
    async getDecision(preavisDecision_id) {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_AFFAIRE_ID_ENDPOINT + "?preavis_id=" + this.affaire.preavis_id + "&preavisDecision_id=" + preavisDecision_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.decision = response.data;
          this.decision.disabled = true;
          this.decision.show = true;
        }
      }
      ).catch(err => handleException(err));
    },
    
    
    // saveDecision
    async saveDecision() {
      this.decision.disabled = true;

      let formData = new FormData();
      formData.append('preavis_id', this.affaire.preavis_id);
      formData.append('preavis_type_id', this.decision.preavis_type_id);
      formData.append('remarque', this.decision.remarque);

      this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_AFFAIRE_ID_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.getDecisionList();
        this.resetDecision();
        this.decision.show = false;
        this.$root.$emit('ShowMessage', 'La décision a bien été enregistrée');
      }).catch(err => handleException(err, this));
    }
  },

  mounted: function() {
    this.getDecisionList();
  }
};
</script>
