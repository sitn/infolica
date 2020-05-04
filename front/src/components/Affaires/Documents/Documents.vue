<style src="./documents.css" scoped></style>
<template src="./documents.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'
import axios from "axios";

export default {
  name: "Documents",
  props: {},
  components: {},
  data: () => ({
    showUploadDocsDialog: false,
    documentFile: null,
    documentFileName: null,
    documents: []
  }),

  methods: {
    /*
     * SEARCH AFFAIRE REMARQUES
     */
    async searchAffaireDocuments() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_DOCUMENTS_ENDPOINT +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.documents = response.data;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Télécharger le document en local
     */
    downloadItem(item) {
      alert(item.chemin.replace(/\\/g, "/"))
      axios.get(item.chemin.replace(/\\/g, "/"), { responseType: "blob" })
        .then(response => {
          const blob = new Blob([response.data], { type: "application/pdf" });
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          window.open(link.href)
        })
        .catch(console.error);
    },

    /**
     * Upload affaire document to server
     */
    uploadAffaireDocument() {
      let _this = this;
      let formData = new FormData();
      formData.append('affaire_doc_file', this.documentFile);
      formData.append('affaire_id', this.$route.params.id);

      axios.post(process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_UPLOAD_DOCUMENTS_ENDPOINT,
          formData, 
          {
              withCredentials: true,
              headers: {'Content-Type': 'multipart/form-data'}
          }
        ).then(function () {
         _this.$root.$emit("ShowMessage", "Le document " + _this.documentFileName + " a été chargé avec succès");
         _this.searchAffaireDocuments();
        })
        .catch(function (err) {
          handleException(err, _this);
        });
    },

    /**
     * Handle file change
    */
    handleFileSelect(files) {
      if(files && files.length > 0){
        this.documentFile = files[0];
      } 
    }
  },

  mounted: function() {
    this.searchAffaireDocuments();
  }
};
</script>



