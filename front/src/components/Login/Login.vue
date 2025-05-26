<style src="./login.css" scoped></style>
<template src="./login.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {setCurrentUserFunctions} from '@/services/helper';

export default {
  name: 'Login',
  props: {},
  data: () => {
    return {
      showProgess: false
    }
  },
  methods:{

    /**
     * Login
     */
    async doLogin () {
        this.showProgess = true;
        var formData = new FormData();
        formData.append("login", this.$refs.username.value);
        formData.append("password", this.$refs.userpass.value);

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_LOGIN_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if(response && response.data && response.data.id){
            this.processLogin(response.data).then(() => {
              if (process.env.VUE_APP_SERVICE_MO === response.data.service) {
                this.$router.push(this.$route.query.redirect || { name: "Cockpit"});
              } else {
                this.$router.push(this.$route.query.redirect || { name: "Preavis"});
              }
            });
          } else {
            this.showProgess = false;
            this.$refs.userpass.value = "";
          }
        })
        //Error
        .catch(() => {
          this.showProgess = false;
          this.$root.$emit('ShowError', "Échec de la connexion")
        });
      },

      /**
       * Logout
       */
      async doLogout () {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_LOGOUT_ENDPOINT,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(() =>{
          localStorage.removeItem('infolica_user');
        })
        //Error
        .catch(err => {
          handleException(err, this);
        });
      },


      /**
       * Process login
       */
      async processLogin (data) {
        return new Promise((resolve) => {
          localStorage.setItem('infolica_user', JSON.stringify(data));
          setCurrentUserFunctions().then(() => {
            this.$root.$emit("notesMaj_hasAdminRights");
          });
          this.$root.$emit('infolica_user_logged_in', data);
          localStorage.removeItem('infolica_cockpit_searchParams');
          resolve();
        });
      },

      /**
       * Process logout
       */
      processLogout () {
        localStorage.removeItem('infolica_user');
        this.$root.$emit('notesMaj_set_default_params');
        this.$root.$emit('infolica_user_logged_out');

        if(this.$router && this.$router.currentRoute && this.$router.currentRoute.name != 'Login')
          this.$router.push({ name: "Login"});
      },

      /**
       * get version of Infolica
       */
      async getVersion() {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_VERSION_ENDPOINT,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.$root.$emit("checkVersion", response.data.version, false);
          }
        }).catch(err => handleException(err));
      },

    },

    mounted: function(){
      //Logout
      this.$root.$on("infolica_user_logout", () => {
        this.doLogout();
        this.processLogout();
      });
    },

    beforeMount: function() {
      localStorage.removeItem('infolica_user');
      this.getVersion();
    }
}
</script>

