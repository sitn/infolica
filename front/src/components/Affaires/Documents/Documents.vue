<style src="./documents.css" scoped></style>
<template src="./documents.html"></template>


<script>
import { checkPermission } from '@/services/helper'
import { handleException } from '@/services/exceptionsHandler'
import axios from "axios";


export default {
  name: "Documents",
  props: {
    affaire: {type: Object},
  },
  components: {},
  data: () => ({
    currentDeleteDocId: null,
    currentDeleteDocName: null,
    deleteDocActive: false,
    deleteDocMessage: '',
    documentFiles: null,
    documentFileName: null,
    documents: [],
    dossier_affaire: null,
    editAffairePath: false,
    form: {
      affairePath: null,
    },
    type_document: null,
    types_documents_list: null,
    showEditAffairePathBtn: false,
    showUploadDocBtn: false,
    showUploadDocsDialog: false,
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
      window.open(process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_DOWNLOAD_DOCUMENT_ENDPOINT + '?affaire_id=' + affaire_id + '&relpath=' + item.relpath + '&filename=' + item.filename + '&time=' + new Date().getTime());
    },


    /**
     * Copier dans le presse-papier
     */
    copyToClipboard () {
      this.$clipboard(this.dossier_affaire);
      this.$root.$emit("ShowMessage", "Copié dans le presse-papier avec succès")
    },

    /**
     * Save modified path of affaire
     */
    async saveAffairePath() {
      let formData = new FormData();
      formData.append('id_affaire', this.affaire.id);
      formData.append('chemin', this.dossier_affaire);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.searchAffaireDocuments();
          this.$root.$emit("setAffaire");
          this.$root.$emit("ShowMessage", "Le dossier d'affaire a bien été modifié.");
        }
      }).catch(err => {
        this.searchAffaireDossier();  
        handleException(err, this);
      });
      
      this.editAffairePath = false;
    },

    /**
     * Cancel Edition of affaire path
     */
    cancelEditAffairePath() {
      this.editAffairePath = false;
      this.searchAffaireDossier();
    },



  },

  mounted: function() {
    this.searchAffaireDocuments();
    this.searchAffaireDossier();

    this.$root.$on("searchAffaireDocuments", () => {
      this.searchAffaireDossier()
      this.searchAffaireDocuments()
    })

    // show edit affaire path
    if(checkPermission(process.env.VUE_APP_FONCTION_ADMIN)) {
      this.showEditAffairePathBtn = true;
    }

  }
};
</script>



