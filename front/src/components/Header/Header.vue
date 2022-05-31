<style src="./header.css" scoped></style>
<template src="./header.html"></template>


<script>
import { checkPermission } from '@/services/helper';


export default {
  name: 'Header',
  props: {
    instance: {type: Object}
  },
  data: function () {
      return {
          loggedUserName: String,
          isAdmin: false,
          isUserSGRF: false,
          session_user: {},
          versionBtn: {
            version: null,
            showBadge: false
          }
      }
  },

  methods:{

    /**
     * Set user name
     */
    setUserName(data){
      if(data && data.nom && data.prenom)
        this.loggedUserName = data.prenom + ' ' + data.nom;

      else
        this.loggedUserName = null;
    },

    /**
     * call logout
     */
    callLogout(){
      if(this.$router && this.$router.currentRoute && this.$router.currentRoute.name != 'Login'){
        let vm = this;
        this.$router.push({name: "Login"}, function(){
          vm.$root.$emit("infolica_user_logout");
        });        
      }
      
    },

    checkIsAdmin() {
      this.isAdmin = checkPermission(process.env.VUE_APP_FONCTION_ADMIN);
    },

    /**
     * Check if user is from SGRF
     */
    checkIsSGRF() {
      let session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

      if(session_user && session_user.service) {
        console.log(session_user.service, process.env.VUE_APP_SERVICE_MO, session_user.service === process.env.VUE_APP_SERVICE_MO)
        this.isUserSGRF = session_user.service === process.env.VUE_APP_SERVICE_MO;
      } else {
        this.isUserSGRF = false;
      }
    },

    /**
     * set version and badge if new
     */
    checkVersion(version, isNew=false) {
      this.versionBtn.version = version;
      this.versionBtn.showBadge = isNew;
    },

    /**
     * Open notes MAJ
     */
    openNotesMAJ() {
      this.$root.$emit("openNotesMAJ");
    },
  },

  mounted: function(){
    this.$root.$on('infolica_user_logged_in', (logged_user) =>{
      this.setUserName(logged_user);
      this.checkIsAdmin();
      this.isUserSGRF = logged_user.service === process.env.VUE_APP_SERVICE_MO;
    });

    this.$root.$on('infolica_user_logged_out', () =>{
      this.setUserName(null);
      this.isUserSGRF = false;
    });

    this.session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    this.setUserName(this.session_user);

    this.checkIsAdmin();
    this.checkIsSGRF();
    
    this.$root.$on("checkVersion", (version, isNew) => this.checkVersion(version, isNew));
  }
}
</script>

