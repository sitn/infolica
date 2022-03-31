<style src="./preavisEdit.css" scoped></style>
<template src="./preavisEdit.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";

import { handleException } from "@/services/exceptionsHandler";

// import moment from "moment";

export default {
  name: "PreavisAffaire",
  props: {},
  components: {
    MapHandler,
  },
  data() {
    return {
      affaire: {},
      affaireLoaded: false,
      documents: [{}],
      conversation: [{}],
      mapLoaded: false,
      commentaire: null,
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
    /*
     * SEARCH AFFAIRE PREAVIS
     */
    async getAffaire() {
      return new Promise((resolve, reject) => {
        this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_AFFAIRE_BY_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => {
          if (response && response.data) {
            this.affaire = response.data;
            resolve(response.data)
          }
        })
        .catch((err) => {
          handleException(err, this);
          reject(err)
        });
      })
    },



    // async searchAffaire() {
    //   this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_AFFAIRE_BY_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
    //     {
    //       withCredentials: true,
    //       headers: { Accept: "application/json" }
    //     }
    //   ).then(response => {
    //     if (response && response.data) {
    //       this.affaire = response.data;
    //     }
    //   })
    //   .catch((err) => handleException(err, this));
    // },

    /**
     * Show map
     */
    showMap() {
      if(this.$refs && this.$refs.mapHandler && !this.mapLoaded){
        this.center = {
          x: this.affaire.coord_e,
          y: this.affaire.coord_n
        };
        this.$refs.mapHandler.initMap(
          this.center,
          process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM
        );
        this.$refs.mapHandler.addMarker(this.center.x, this.center.y);
        this.$refs.mapHandler.modify.setActive(false);
        this.$refs.mapHandler.snap.setActive(false);
        this.mapLoaded = true;
      }
    },



    /**
     * Documents
     */
    async getDocuments() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DOCUMENTS_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.documents = response.data;
        }
      }).catch(err => handleException(err));
    },

    /**
     * Get conversation
     */
    async getConversation() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_CONVERSATION_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.conversation = response.data;
        }
      }).catch(err => handleException(err));
    },

    async saveMessage() {
      let formData = new FormData();
      formData.append('affaire_id', this.$route.params.id);
      formData.append('commentaire', this.commentaire);

      this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_CONVERSATION_BY_AFFAIRE_ID_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.$root.$emit('ShowMessage', 'Le commentaire a bien été enregistré');
          this.commentaire = null;
          this.getConversation();
        }
      }).catch(err => handleException(err));
    },
    

    // /**
    //  * Open Theme SITN
    //  */
    // openSitnTheme(theme) {
    //   let route;
    //   if (theme === "amenagement_territoire") {
      //       route = process.env.VUE_APP_SITN_AMENAGEMENT_TERRITOIRE_URL;
    //   } else if (theme === "cadastre") {
      //       route = process.env.VUE_APP_SITN_CADASTRE_URL;
    //   } else if (theme === "sites_pollues") {
      //       route = process.env.VUE_APP_SITN_SITES_POLLUES_URL;
    //   } else {
      //     return null;
    //   }
    //   window.open(route + "&map_x=" + this.affaire.localisation_e + "&map_y=" + this.affaire.localisation_n, "_blank");
    // },

    /**
     * Download file from table
     */
    async downloadFile(item) {
      let requestParams = [
        'affaire_id=' + this.affaire.id,
        'relpath=' + item.rel_path,
        'filename=' + item.filename,
        '&time=' + new Date().getTime()
      ].join("&");

      window.open(process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_DOWNLOAD_DOCUMENT_ENDPOINT + '?' + requestParams)
    },


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
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_LIST_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id,
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
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DECISION_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.$route.params.id + "&preavisDecision_id=" + preavisDecision_id,
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
      formData.append('affaire_id', this.$route.params.id);
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
      }).catch(err => handleException(err));
    },
  },

  mounted: function() {
    this.getAffaire().then(() => {
      this.showMap();
    });

    this.getDocuments();
    this.getConversation();
    this.getDecisionList();
  }
};
</script>
