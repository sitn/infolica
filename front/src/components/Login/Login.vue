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
        .then(response =>{
          if(response && response.data && response.data.id){
            this.processLogin(response.data);

            if (["SAT", "SU_NE"].includes(response.data.service)) {
              this.$router.push({ name: "Preavis"});
            } else {
              const redirectPath = localStorage.getItem('infolica_redirectPath');
              if (redirectPath) {
                this.$router.replace(redirectPath);
                localStorage.removeItem('infolica_redirectPath');
              } else {
                this.$router.push({ name: "Cockpit"});
              }
            }
          } else {
            this.showProgess = false;
            this.$refs.userpass.value = "";
            this.$root.$emit("ShowError", "Le nom d'utilisateur ou le mot de passe est incorrect");
          }
        })
        //Error 
        .catch(err => {
          this.showProgess = false;
          handleException(err, this);
        })
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
        })
      },


      /**
       * Process login
       */
      processLogin (data) {
        localStorage.setItem('infolica_user', JSON.stringify(data));
        setCurrentUserFunctions().then(() => {
          this.$root.$emit("notesMaj_hasAdminRights");
        });
        this.$root.$emit('infolica_user_logged_in', data);
      },

      /**
       * Process logout
       */
      processLogout () {
        localStorage.setItem('infolica_user', null);
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
      this.getVersion();

      //Logout
      this.$root.$on("infolica_user_logout", () => {        
        this.doLogout();    
        this.processLogout();    
      });
    }
}
</script>

