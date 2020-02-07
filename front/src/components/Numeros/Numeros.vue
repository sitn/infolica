<style src="./numeros.css" scoped></style>
<template src="./numeros.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'Numeros',
  props: {
    msg: String
  },

  mounted: function(){
    checkLogged();
  }
}
</script>

