<style src="./preavis.css" scoped></style>
<template src="./preavis.html"></template>


<script>

import { handleException } from '@/services/exceptionsHandler';
// import { checkPermission, getOperateurs, stringifyAutocomplete, stringifyAutocomplete2, getCurrentUserRoleId } from '@/services/helper';

// import moment from "moment";

export default {
  name: "Cockpit",
  components: {},
  data: () => {
    return {
      liste_preavis_attente: [],
    };
  },

  methods: {
    // get opened preavis
    async getOpenedPreavis() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_SERVICE_EXTERNE_PREAVIS_ENDPOINT,
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
    }

    //
  },

  mounted: function() {
    this.getOpenedPreavis();

  }
};
</script>

