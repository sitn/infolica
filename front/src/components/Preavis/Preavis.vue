<style src="./preavis.css" scoped></style>
<template src="./preavis.html"></template>


<script>

import { handleException } from '@/services/exceptionsHandler';

// import moment from "moment";

export default {
  name: "Cockpit",
  components: {},
  data: () => {
    return {
      liste_preavis_attente: [],
      reloadData: null,
      searchTerm: null,
    };
  },

  methods: {
    // get opened preavis
    async getOpenedPreavis() {
      let params = '';
      if (this.searchTerm) {
        params = "?search=" + String(this.searchTerm);
      }

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICE_EXTERNE_PREAVIS_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {'accept': 'application/json'}
        }
      )
      .then(response => {
        if (response && response.data) {
          this.liste_preavis_attente = response.data;
        }
      }).catch(err => handleException(err, this));
    },

    // preavis attribution
    async preavisAttribution(item) {
      let formData = new FormData();
      formData.append('affaire_id', item.preavis_affaire_id);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICE_EXTERNE_PREAVIS_ATTRIBUTION_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {'accept': 'application/json'}
        }
      ).then(response => {
        if (response && response.data) {
          this.getOpenedPreavis();
        }
      }).catch(err => handleException(err, this));
    },

  },

  mounted: function() {
    this.getOpenedPreavis();

  },

  created: function() {
    this.reloadData = setInterval(
      () => this.getOpenedPreavis(),
      30000
    );
  },

  beforeDestroy: function() {
    clearInterval(this.reloadData);
  }
};
</script>

