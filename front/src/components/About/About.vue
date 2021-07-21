<style src="./about.css" scoped></style>
<template src="./about.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
const moment = require('moment');

export default {
  name: 'About',
  props: {
    msg: String
  },
  data: () => {
    return {
      expandNotes: false,
      notes: [],
    }
  },
  methods: {
    /**
     * Get Notes
     */
    getNotesMAJ() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          tmp.forEach( x => {
            x.date_client = moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            x.delai_client = moment(x.delai, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
          });
          this.notes = tmp;
        }
      }).catch(err => handleException(err, this));
    },
  },
  mounted: function(){
    this.getNotesMAJ();
  }
}
</script>

