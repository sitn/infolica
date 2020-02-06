<style src="./clients.css" scoped></style>
<template src="./clients.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'Clients',
  props: {},
  data: () => ({
      clients: []
  }),
  methods: {
        /**
         * Search clients
        */
        async searchClients () {
            /*var formData = new FormData();
            formData.append("login", this.$refs.username.value);
            formData.append("password", this.$refs.userpass.value);*/

            this.$http.post(
              process.env.VUE_APP_API_URL + process.env.VUE_APP_SEARCH_CLIENTS_ENDPOINT, 
              {nom: 'Marc'},
              {
                //withCredentials: true,
                headers: {'Accept': 'application/json'}
              }
            )
            .then(response =>{
              if(response && response.data){
                this.clients = response.data;
              }
            })
            //Error 
            .catch(err => {
              alert("error : " + err.message);  
            })
          }
  },

  mounted: function(){
    checkLogged();
    this.searchClients();
  }
}
</script>

