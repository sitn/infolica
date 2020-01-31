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
            formData.append("login", "cko");
            formData.append("password", "cko");

            this.$http.post(
              process.env.VUE_APP_API_URL + process.env.VUE_APP_LOGIN_ENDPOINT, 
              formData,
              {
                //withCredentials: true,
                headers: {'Accept': 'application/json'}
              }
            )
            .then(response =>{
              if(response)
                this.$router.push('/affaires');
            })
            //Error 
            .catch(err => {
              alert("error : " + err.message);  
            })
          }          
    },

    created: function(){
      
    }
}
</script>

