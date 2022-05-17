<style src="./preavisEditComments.css" scoped></style>
<template src="./preavisEditComments.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "PreavisEditComments",
  props: {
    preavis_id: Number
  },
  components: {},
  data() {
    return {
      conversation: [{}],
      commentaire: null,
    };
  },

  methods: {
    /**
     * Get conversation
     */
    async getConversation() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_CONVERSATION_BY_PREAVIS_ID_ENDPOINT + "?preavis_id=" + this.preavis_id,
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
      formData.append('preavis_id', this.preavis_id);
      formData.append('commentaire', this.commentaire);

      this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_CONVERSATION_BY_PREAVIS_ID_ENDPOINT,
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

    // remark read
    async remark_read(pr) {
      let formData = new FormData();
      formData.append('preavis_remarque_id', pr.preavis_remarque_id);
      formData.append('lu_operateur_id', JSON.parse(localStorage.getItem("infolica_user")).id);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_PREAVIS_CONVERSATION_BY_PREAVIS_ID_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          this.getConversation();
          this.$root.$emit('getPreavis');
        }
      }).catch(err => handleException(err, this));
    },


  },

  mounted: function() {
    this.getConversation();
  }
};
</script>
