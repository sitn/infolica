<style src="./main.css" scoped></style>
<template src="./main.html"></template>


<script>
import Login from '@/components/Login/Login.vue'
import {checkLogged} from '@/services/helper'

export default {
  name: 'Main',
  components: {
    Login
  },
  props: {
    msg: String
  },
  mounted: function(){
    checkLogged();
  }
}
</script>

