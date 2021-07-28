<style src="./css/style.css"></style>
<template src="./app.html"></template>

<script>

// Import components
import Header from './components/Header/Header.vue'
import Main from './components/Main/Main.vue'
import Notifications from '@/components/Notifications/Notifications.vue'
import NotesMAJ from '@/components/NotesMAJ/NotesMAJ.vue';

export default {
  name: 'app',
  components: {
    Header, NotesMAJ, Main, Notifications
  },
  data: () => {
    return {
      instance: {
        isProd: false,
        name: process.env.VUE_APP_STATUS.toUpperCase(),
      }
    };
  },
  mounted: function(){
    this.instance.isProd = this.instance.name === 'PRODUCTION';
  }
}
</script>




