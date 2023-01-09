<style src="./notesMAJ.css" scoped></style>
<template src="./notesMAJ.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler'
import {disabledDates_fct, checkPermission} from '@/services/helper'
const moment = require('moment');

export default {
  name: 'NotesMAJ',
  props: {},
  data: () => {
    return {
      currentVersion: {},
      disabledDates: disabledDates_fct,
      newNote: {
        show: false,
        version: null,
        titre: null,
        message: null,
        delai: null,
      },
      mustUpdateLastVersionOperateur: false,
      notes: [],
      permissions : {
        admin: false
      },
      showNotesMAJ: false,
    }
  },
  methods: {
    /**
     * Get Notes
     */
    getNotesMAJ(operateur_lastNoteMaj) {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT + "?lastNoteMaj_id=" + String(operateur_lastNoteMaj),
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
      return new Promise ((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_VERSION_ENDPOINT,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.$root.$emit("checkVersion", response.data.version, false);
            resolve(response);
          }
        }).catch(err => reject(err));
      });
    },

    /**
     * Go to router
     */
    goTo(route){
      if(this.$router && this.$router.currentRoute && this.$router.currentRoute.name != route) {
        this.$router.push({ name: route});
        this.showNotesMAJ = false;
        this.updateMainDivHeight();
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
          this.compareOperateurVersionWithCurrentVersion();
          this.mustUpdateLastVersionOperateur = true;
        }
      }).catch(err => handleException(err, this));

      this.newNote = {
        show: false,
        version: null,
        titre: null,
        message: null,
        delai: null,
      };
    },

    /**
     * get permissions
     */
    getPermissions() {
      this.permissions.admin = checkPermission(process.env.VUE_APP_FONCTION_ADMIN);
    },

    /**
     * Get operateur by id
     */
    async getOperateurById() {
      return new Promise ((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT + "/" + JSON.parse(localStorage.getItem("infolica_user")).id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            resolve(response);
          }
        }).catch(err => reject(err));
      });
    },

    /**
     * Compare last version in operateur with current version
     */
    async compareOperateurVersionWithCurrentVersion() {
      let promises = [];
      promises.push(this.getOperateurById());
      promises.push(this.getVersion());

      let operateur_lastMajNote = null;
      let operateur_service = null;
      Promise.all(promises).then(response => {
        operateur_lastMajNote = response[0].data.last_notemaj_id;
        operateur_service = response[0].data.service;

        // if user is not from SGRF, don't load version notes
        if (operateur_service !== process.env.VUE_APP_SERVICE_MO) {
          return
        }

        this.currentVersion = response[1].data;
        if (operateur_lastMajNote !== this.currentVersion.lastId) {
          this.$root.$emit("checkVersion", this.currentVersion.version, this.currentVersion.isNew);
          this.getNotesMAJ(operateur_lastMajNote);
          this.showNotesMAJ = true;
          this.mustUpdateLastVersionOperateur = true;
        } else {
          this.$root.$emit("checkVersion", this.currentVersion.version, false);
          this.mustUpdateLastVersionOperateur = false;
          this.notes = [];
        }

        // set main_div height
        this.updateMainDivHeight();

      });

      this.getOperateurById().then(response => {
        if (response && response.data) {
          operateur_lastMajNote = response.data.lastVersion;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * update div "main" height
     */
    updateMainDivHeight() {
      if (this.showNotesMAJ) {
        // recursively check untill element notesmaj is ready
        const interval = setInterval(() => {
          let div_notesmaj = document.getElementById('notesmaj');
          if (div_notesmaj) {
            document.getElementById('main').setAttribute("style","height: calc(100% - " + String(div_notesmaj.offsetHeight + 9) + "px)");
            clearInterval(interval);
          }
          return;
        }, 200);

      } else {
        document.getElementById('main').setAttribute("style","height: calc(100% - 60px)");
      }
    },

    /**
     * closeInfobulle with saving lastId notes MAJ
     */
    async closeAndSaveInfobulle() {
      if (this.mustUpdateLastVersionOperateur) {
        let formData = new FormData();
        formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);
        formData.append("last_notes_maj_id", this.currentVersion.lastId);

        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEUR_LASTNOTEMAJ_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.compareOperateurVersionWithCurrentVersion();
          }
        }).catch(err => handleException(err, this));
      }

      // fermer l'infobulle et setter la hauteur du div main
      this.closeInfobulle();
    },

    /**
     * close infobulle
     */
    closeInfobulle() {
      // fermer l'infobulle
      this.showNotesMAJ = false;
      //set main_div height
      this.updateMainDivHeight();
    }

  },

  mounted: function(){
    this.getVersion();
    this.getPermissions();
    
    if (JSON.parse(localStorage.getItem("infolica_user")) && JSON.parse(localStorage.getItem("infolica_user")).id) {
      this.compareOperateurVersionWithCurrentVersion();
    }

    this.$root.$on("openNotesMAJ", () => {
      if (!this.showNotesMAJ) {
        this.compareOperateurVersionWithCurrentVersion();
        this.showNotesMAJ=true;
      } else {
        this.closeInfobulle();
      }
    });
    this.$root.$on("notesMaj_set_default_params", () => this.showNotesMAJ = false);

    this.$root.$on("notesMaj_hasAdminRights", () => {
      this.getPermissions();
      this.compareOperateurVersionWithCurrentVersion();
    });
  },
}
</script>

