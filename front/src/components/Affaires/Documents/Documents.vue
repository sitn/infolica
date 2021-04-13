<style src="./documents.css" scoped></style>
<template src="./documents.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'
import axios from "axios";

export default {
  name: "Documents",
  props: {
    affaire: {type: Object}
  },
  components: {},
  data: () => ({
    showUploadDocBtn: false,
    deleteDocActive: false,
    deleteDocMessage: '',
    currentDeleteDocId: null,
    currentDeleteDocName: null,
    types_documents_list: null,
    showUploadDocsDialog: false,
    type_document: null,
    // disableOpenFolder: false,
    documentFiles: null,
    documentFileName: null,
    documents: [],
    dossier_affaire: null,
  }),

  methods: {
    /**
     * Search affaire dossier
     */
    async searchAffaireDossier() {
      this.$http.get(
        process.env.VUE_APP_API_URL + 
        process.env.VUE_APP_AFFAIRE_DOSSIER_ENDPOINT +
        this.$route.params.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.dossier_affaire = response.data;
        }
      }).catch(err => handleException(err, this))
    },

    /*
     * SEARCH AFFAIRE DOCUMENTS
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
            let tmp = response.data;
            tmp.forEach(x => x.modification_sort = new Date(x.modification).getTime());
            this.documents = tmp;
          }
        })
        .catch(err => {
          handleException(err, this);
        });

        this.showUploadDocsDialog = false;
    },

    /**
     * Télécharger le document en local
     */
    downloadItem(item) {
      axios.get(item.chemin.replace(/\\/g, "/"), { responseType: "blob" })
        .then(response => {
          const blob = new Blob([response.data], { type: "application/pdf" });
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          window.open(link.href)
        })
        .catch(console.error);
    },

    /*
    * Init types clients list
    */
    initTypesDocumentsList() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TYPES_DOCUMENTS_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      )
      .then(response =>{
        if (response && response.data) {
          this.types_documents_list = response.data;

          if(this.types_documents_list.length > 0){
            this.type_document = this.types_documents_list[0].id;
          }
        }
      })
      //Error 
      .catch(err => {
        handleException(err, this);
      });
    },


    /**
     * Handle file change
    */
    handleFileSelect(files) {
      if(files && files.length > 0){
        this.documentFiles = files;
      } 
    },
    
    /**
     * Download file
    */
    downloadFile(item) {
      const affaire_id = this.$route.params.id;
      window.open(process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_DOWNLOAD_DOCUMENT_ENDPOINT + '?affaire_id=' + affaire_id + '&relpath=' + item.relpath + '&filename=' + item.filename);
    },


    /**
     * Copier dans le presse-papier
     */
    copyToClipboard () {
      let copyText = document.querySelector("#dossier-affaire");
      copyText.setAttribute('type', 'text');
      copyText.select();
      var success = document.execCommand("copy");
      if (success) {
        this.$root.$emit("ShowMessage", "Copié dans le presse-papier avec succès")
      } else {
        this.$root.$emit("ErrorMessage", "Erreur, n'a pas pu copier le contenu")
      }
    },

    // /**
    //  * Open folder
    //  */
    // async openFolder(){
    //   this.disableOpenFolder = true;
    //   setTimeout(() => {  this.disableOpenFolder=false; }, 2000);
    //   this.$http.get(
    //     process.env.VUE_APP_API_URL + process.env.VUE_APP_OPEN_FOLDER_ENDPOINT + '?affaire_id=' + this.affaire.id,
    //     {
    //       withCredentials: true,
    //       headers: {"Accept": "application/json"}
    //     }
    //   )
    // }

  },

  mounted: function() {
    this.searchAffaireDocuments();
    this.searchAffaireDossier();
  }
};
</script>



