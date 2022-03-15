<style src="./main.css" scoped></style>
<template src="./main.html"></template>


<script>
import Login from '@/components/Login/Login.vue'


export default {
  name: 'Main',
  components: {
    Login
  },
  data: () => ({
    isAuthenticated: false
  })
}
</script>

