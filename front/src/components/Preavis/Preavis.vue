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
      searchTerm: null,
      liste_preavis_old: [],
      searchTerm_old: null,
      reloadData: null,
    };
  },

  methods: {
    // get opened preavis
    async getOpenedPreavis() {
      let params = '?status=open';
      if (this.searchTerm) {
        params += "&search=" + String(this.searchTerm);
      }

      this.getPreavis(params).then(response => {
        if (response && response.data) {
          this.liste_preavis_attente = response.data;
        }
      }).catch(err => handleException(err, this));
    },

    // get closed preavis
    async getClosedPreavis() {
      let params = '?status=closed';
      if (this.searchTerm_old) {
        params += "&search=" + String(this.searchTerm_old);
      }

      this.getPreavis(params).then(response => {
        if (response && response.data) {
          this.liste_preavis_old = response.data;
        }
      }).catch(err => handleException(err, this));
    },


    async getPreavis(params='') {
      return new Promise ((resolve, reject) => {
        this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICE_EXTERNE_PREAVIS_ENDPOINT + params,
        {
          withCredentials: true,
          headers: {'accept': 'application/json'}
        }
      ).then(response => resolve(response))
      .catch(err => reject(err));
      });
    },


    // preavis attribution
    async preavisAttribution(item) {
      let formData = new FormData();
      formData.append('preavis_id', item.preavis_id);

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
    this.getClosedPreavis();

  },

  created: function() {
    this.reloadData = setInterval(
      () => {
        this.getOpenedPreavis(),
        this.getClosedPreavis()
      },
      30000 // recharge le tableau toutes les 30 secondes
    );
  },

  beforeDestroy: function() {
    clearInterval(this.reloadData);
  }
};
</script>

