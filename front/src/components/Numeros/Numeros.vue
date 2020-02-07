<style src="./numeros.css" scoped></style>
<template src="./numeros.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'Numeros',
  props: {},
  data: () => ({
      numeros: [],
      search: {
        cadastre: null,
        type: null,
        etat: null
      }
  }),

  methods: {
    /* SEARCH NUMEROS */
    async searchNumeros(){
      
      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_RECHERCHE_NUMEROS_ENDPOINT, 
        {etat: 'Projet'},
        {
          //withCredentials: true,
          headers: {'Accept': 'application/json'}
        }
      )
      
      .then(response =>{
        if(response && response.data){
          this.numeros = response.data;
        }
      })

      .catch(err => {
        alert("error : " + err.message);  
      })
    }

  },

  mounted: function(){
    checkLogged();
    this.searchNumeros();
  }
}
</script>

