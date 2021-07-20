<style src="./notesMAJ.css" scoped></style>
<template src="./notesMAJ.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'
const moment = require('moment');

export default {
  name: 'NotesMAJ',
  props: {},
  data: () => {
    return {
      notes: [],
      showNotesMAJ: true,
    }
  },
  methods: {
    /**
     * Get Notes
     */
    getNotesMAJ() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT + "?active=true",
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
            x.title = "Version " + String(x.version) + " du " + String(x.date_client);
          });

          this.notes = tmp;

          // Update version btn in header
          let lastUpdate = tmp[0];
          let version = lastUpdate.version;
          let isNew = (moment(lastUpdate.delai, process.env.VUE_APP_DATEFORMAT_WS) - new Date()) / 1000 / 3600 / 24 + 1 > 0;
          this.$root.$emit("checkVersion", version, isNew);

        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Go to router
     */
    goTo(route){
      if(this.$router && this.$router.currentRoute && this.$router.currentRoute.name != route)
        this.$router.push({ name: route});
        this.showNotesMAJ = false;
    },

  },
  mounted: function(){
    this.getNotesMAJ();

    this.$root.$on("openNotesMAJ", () => this.showNotesMAJ = true);
}
}
</script>

