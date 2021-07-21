<style src="./notesMAJ.css" scoped></style>
<template src="./notesMAJ.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'
import {disabledDates_fct} from '@/services/helper'
const moment = require('moment');

export default {
  name: 'NotesMAJ',
  props: {},
  data: () => {
    return {
      disabledDates: disabledDates_fct,
      newNote: {
        show: false,
        version: null,
        titre: null,
        message: null,
        delai: null,
      },
      notes: [],
      permissions : {
        admin: false
      },
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
          this.$root.$emit("checkVersion", response.data.version, response.data.isNew);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Go to router
     */
    goTo(route){
      if(this.$router && this.$router.currentRoute && this.$router.currentRoute.name != route) {
        this.$router.push({ name: route});
        this.showNotesMAJ = false;
      }
    },

    /**
     * open new Note
     */
    openNewNote() {
      let tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);

      this.newNote.delai = tomorrow;
      this.newNote.show = true;
    },

    /**
     * on cancel new Note
     */
    onCancelNewNote() {
      this.newNote = {
        show: false,
        version: null,
        titre: null,
        message: null,
        delai: null,
      };
    },

    /**
     * on save new Note
     */
    onSaveNewNote() {
      // Ne pas enregistrer si un champ est null
      for (const key in this.newNote) {
        if (this.newNote[key] === null || this.newNote[key] === "") {
          return
        }
      }

      let formData = new FormData();
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);
      formData.append("version", this.newNote.version);
      formData.append("titre", this.newNote.titre);
      formData.append("message", this.newNote.message);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
      formData.append("delai", moment(this.newNote.delai, process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));


      this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.$root.$emit("ShowMessage", "La note de mise à jour a bien été enregistrée");
          this.getNotesMAJ();
          this.getVersion();
        }
      }).catch(err => handleException(err, this));

      this.newNote = {
        show: false,
        version: null,
        titre: null,
        message: null,
        delai: null,
      };
    }
  },
  mounted: function(){
    this.getNotesMAJ();
    this.getVersion();

    this.$root.$on("openNotesMAJ", () => this.showNotesMAJ = true);
    this.$root.$on("notesMaj_hasAdminRights", (hasAdminRights) => this.permissions.admin = hasAdminRights);
  }
}
</script>

