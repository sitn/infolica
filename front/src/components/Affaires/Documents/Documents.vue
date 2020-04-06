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
      axios.get(item.chemin, { responseType: "blob" })
        .then(response => {
          const blob = new Blob([response.data], { type: "application/pdf" });
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          link.download = item.nom;
          link.click();
          URL.revokeObjectURL(link.href);
        })
        .catch(console.error);
    }
  },

  mounted: function() {
    this.searchAffaireDocuments();
  }
};
</script>



