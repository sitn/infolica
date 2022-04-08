<style src="./preavisEdit.css" scoped></style>
<template src="./preavisEdit.html"></template>


<script>
import MapHandler from "@/components/MapHandler/MapHandler.vue";
import PreavisEditComments from "@/components/Preavis/PreavisEditComments.vue";
import PreavisEditDecision from "@/components/Preavis/PreavisEditDecision.vue";

import { handleException } from "@/services/exceptionsHandler";

import { Drag, Drop } from 'vue-drag-drop';
// import moment from "moment";

export default {
  name: "PreavisAffaire",
  props: {},
  components: {
    Drag,
    Drop,
    MapHandler,
    PreavisEditComments,
    PreavisEditDecision,
  },
  data() {
    return {
      affaire: {},
      affaireLoaded: false,
      documents: [{}],
      droppedFiles: [],
      mapLoaded: false,
    };
  },

  methods: {
    /*
     * SEARCH AFFAIRE PREAVIS
     */
    async getAffaire() {
      return new Promise((resolve, reject) => {
        this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_AFFAIRE_BY_ID_ENDPOINT + "?preavis_id=" + this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => {
          if (response && response.data) {
            this.affaire = response.data;
            resolve(response.data);
            this.affaireLoaded = true;
          }
        })
        .catch((err) => {
          handleException(err, this);
          reject(err);
        });
      })
    },

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
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_DOCUMENTS_BY_AFFAIRE_ID_ENDPOINT + "?affaire_id=" + this.affaire.id,
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

    // handleDrop
    handleDrop(data, event) {
      event.preventDefault();
      this.droppedFiles.push(...event.dataTransfer.files);
    },

    // save files on back-end
    async saveFiles() {
      let formData = new FormData();
      formData.append('affaire_id', this.affaire.id);
      
      for( let i = 0; i < this.droppedFiles.length; i++ ){
        formData.append('files[' + i + ']', this.droppedFiles[i]);
      }
      
      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_POST_FILE_BY_AFFAIRE_ID_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {
            'Accept': "application/json",
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(() => {
        this.getDocuments();
        this.droppedFiles = [];
      })
      .catch(err => handleException(err, this));
    },

    // remove item from fileupload list
    removeItem(item) {
      let index = this.droppedFiles.indexOf(item);
      if (index !== -1) {
        this.droppedFiles.splice(index, 1);
      }
    },

    // save preavis devinitively and submit it to SGRF
    async savePreavisDefinitively() {
      let ped = this.$refs.ped;
      if (ped.decision.show === true) {
        ped.saveDecision(true).then(() => {
          this.$router.push({name: 'Preavis'});
        }).catch(err => handleException(err));
      } else {
        this.$router.push({name: 'Preavis'});
      }
    }

  },

  mounted: function() {
    this.getAffaire().then(() => {
      this.showMap();
      this.getDocuments();
    });
  }
};
</script>
