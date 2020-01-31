<style src="./header.css" scoped></style>
<template src="./header.html"></template>


<script>
export default {
  name: 'Header',
  props: {},

  data: function () {
      return {
          loggedUserName: String
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
      //this.userNameVisible = (typeof this.loggedUserName === "string" && this.loggedUserName.length > 0);
    },

    /**
     * call logout
     */
    callLogout(){
      this.$root.$emit('infolica_user_logout');
    }
  },

  mounted: function(){
      //this.userNameVisible = false;

      this.$root.$on('infolica_user_logged_in', (logged_user) =>{
        this.setUserName(logged_user);
      });

      this.$root.$on('infolica_user_logged_out', () =>{
        this.setUserName(null);
      });

      var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
      this.setUserName(session_user);
  }
}
</script>

