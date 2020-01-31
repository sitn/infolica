<style src="./login.css" scoped></style>
<template src="./login.html"></template>


<script>
export default {
  name: 'Login',
  props: {
  },
  methods:{

        /**
         * Login
         */
        async doLogin () {
            var formData = new FormData();
            formData.append("login", this.$refs.username.value);
            formData.append("password", this.$refs.userpass.value);

            this.$http.post(
              process.env.VUE_APP_API_URL + process.env.VUE_APP_LOGIN_ENDPOINT, 
              formData,
              {
                //withCredentials: true,
                headers: {'Accept': 'application/json'}
              }
            )
            .then(response =>{
              if(response && response.data){
                this.processLogin(response.data);
                this.$router.push('/affaires');
              }
            })
            //Error 
            .catch(err => {
              alert("error : " + err.message);  
            })
          },
          
          /**
           * Logout
           */
          async doLogout () {
            this.$http.get(
              process.env.VUE_APP_API_URL + process.env.VUE_APP_LOGOUT_ENDPOINT, 
              {
                //withCredentials: true,
                headers: {'Accept': 'application/json'}
              }
            )
            .then(() =>{
              
            })
            //Error 
            .catch(err => {
              alert("error : " + err.message);  
            })
          },

          /**
           * Process login
           */
          processLogin (data) {
            localStorage.setItem('infolica_user', JSON.stringify(data));
            this.$root.$emit('infolica_user_logged_in', data);
          },

          /**
           * Process logout
           */
          processLogout () {
            localStorage.setItem('infolica_user', null);
            this.$root.$emit('infolica_user_logged_out');
            this.$router.push('/login');
          }
    },

    mounted: function(){

      //Chek a user is logged in
      this.$root.$on('infolica_check_user_logged_in', () =>{
        var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

        if(!session_user){
          this.$router.push('/login');
          this.processLogout();  
        }
        else{
          this.processLogout(session_user);
        }
      });

      //Logout
      this.$root.$on('infolica_user_logout', () =>{        
        this.doLogout();    
        this.processLogout();    
      });
    }
}
</script>

