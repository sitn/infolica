<style src="./about.css" scoped></style>
<template src="./about.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'About',
  props: {
    msg: String
  },

  mounted: function(){
    checkLogged();
  }
}
</script>

