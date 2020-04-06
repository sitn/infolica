<style src="./notifications.css" scoped></style>
<template src="./notifications.html"></template>


<script>

export default {
  name: 'Notifications',
  data: () => ({
    msg: String,
    showSnackbar: false
  }),

  mounted: function(){
    //Show Message
    this.$root.$on('ShowMessage', (msg) =>{
      this.msg = msg;
      this.showSnackbar = true;
    });

    //Show Error
    this.$root.$on('ShowError', (msg) =>{
      this.msg = msg;
      this.showSnackbar = true;
    });
  }
}
</script>

