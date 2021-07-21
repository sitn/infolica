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
      newNote: {
        show: false,
        titre: null,
        message: null,
        delai: moment(new Date() + 24*3600*1000).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
      }
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
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Get version
     */
    getVersion() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_VERSION_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          console.log(response.data)
          this.$root.$emit("checkVersion", response.data.version, response.data.isNew);
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
    this.getVersion();

    this.$root.$on("openNotesMAJ", () => this.showNotesMAJ = true);
}
}
</script>

