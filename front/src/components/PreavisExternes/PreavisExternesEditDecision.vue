<style src="./preavisExternesEditDecision.css"></style>
<template src="./preavisExternesEditDecision.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "PreavisEditDecision",
  props: {
    preavis_id: Number,
    showAddDecision: Boolean
  },
  components: {},
  data() {
    return {
      decisions_liste: [],
      decision: {
        id: null,
        preavis_type_id: null,
        remarque: null,
        disabled: true,
        show: false,
      },
      glossaire: [],
      hasRightAddDecision: false,
      lastDecisionVersion: -1,
      selected_glossaire: {},
      showGlossaire: false,
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
      this.getGlossaire();

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
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_LIST_BY_PREAVIS_ID_ENDPOINT + "?preavis_id=" + this.preavis_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.decisions_liste = response.data;
          
          //get max version of decision
          this.decisions_liste.forEach(x => {
            this.lastDecisionVersion = x.version > this.lastDecisionVersion? x.version: this.lastDecisionVersion;
          });

          this.decisions_liste.forEach(x => {
            if (x.preavis_type_id === 1) {
              x.icon_status = 'check_circle_outline';
              x.icon_status_style = x.version === this.lastDecisionVersion? 'color: green;': 'color: lightgrey; font-style: italic;';
            } else if (x.preavis_type_id === 2) {
              x.icon_status = 'highlight_off';
              x.icon_status_style = x.version === this.lastDecisionVersion? 'color: red;': 'color: lightgrey; font-style: italic;';
            } else if (x.preavis_type_id === 3) {
              x.icon_status = 'remove_circle_outline';
              x.icon_status_style = x.version === this.lastDecisionVersion? 'color: grey;': 'color: lightgrey; font-style: italic;';
            } else if (x.preavis_type_id === 5) {
              x.icon_status = 'error_outline';
              x.icon_status_style = x.version === this.lastDecisionVersion? 'color: orange;': 'color: lightgrey; font-style: italic;';
            }
          });
        }
      }
      ).catch(err => handleException(err));
    },


    
    // get Decision draft
    async getDecisionDraft() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_PREAVIS_ID_ENDPOINT + "?preavis_id=" + this.preavis_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.decision = response.data;
          this.decision.show = true;
        }
        this.$root.$emit('setPreavisDecisionDraft');
      }
      ).catch(err => handleException(err));
    },
    
    
    // saveDecision
    async saveDecision(definitif=false) {
      let formData = new FormData();
      formData.append('preavis_id', this.preavis_id);
      formData.append('preavis_type_id', this.decision.preavis_type_id);
      formData.append('remarque', this.decision.remarque);
      formData.append('definitif', definitif);

      return new Promise((resolve, reject) => {
        let req = this.$http
        if (this.decision.id) {
          formData.append('preavis_decision_id', this.decision.id)
          req = req.put(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_PREAVIS_ID_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
        } else {
          req = req.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_PREAVIS_ID_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
        }
  
        req.then((response) => resolve(response)
        ).catch(err => reject(err));
      });
    },

    // save data provisoires
    async saveDecisionProvisoire() {
      this.saveDecision(false).then(() => {
        this.getDecisionDraft();
        this.$root.$emit('ShowMessage', 'La décision provisoire a bien été enregistrée');
      }).catch(err => handleException(err, this));
    },

    // get permissions
    getPermissions() {
      let session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
      if (session_user && session_user.service_id) {
        this.hasRightAddDecision = true;
      }
    },

    // copy text from old preavis
    copyText(preavis) {
      this.decision.remarque = preavis.remarque;
    },

    // get service glossaire
    async getGlossaire() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICE_EXTERNE_GLOSSAIRE_ENDPOINT + "?preavis_id=" + this.preavis_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.glossaire = response.data;
        }
      }).catch(err => handleException(err));
    },
    
    addGlossaireText(data) {
      if (!this.decision.remarque) {
        this.decision.remarque = data;
      } else {
        this.decision.remarque += '\n\n' + data;
      }
    }

  },

  mounted: function() {
    this.getDecisionList();
    this.getDecisionDraft();
    this.getPermissions();
  }
};
</script>
