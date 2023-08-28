<style src="./notifications.css" scoped></style>
<template src="./notifications.html"></template>


<script>

export default {
  name: 'Notifications',
  data: () => ({
    alert: {
      active: false,
      title: "",
      content: ""
    },
    confirmation: {
      active: false,
      title: "",
      content: "",
      confirmText: "OK",
      cancelText: "Annuler",
      onCancel: () => {},
      onConfirm: () => {}
    },
    msg: String,
    showSnackbar: false,
    isError: false,
    duration: 5000 //ms
  }),

  mounted: function(){
    //Show Message
    this.$root.$on('ShowMessage', (msg) =>{
      this.msg = msg;
      this.isError = false;
      this.showSnackbar = true;
      this.duration = 5000;
    });

    //Show Error
    this.$root.$on('ShowError', (msg) =>{
      this.msg = msg;
      this.isError = true;
      this.showSnackbar = true;
      this.duration = 7500;
    });

    //Show Alert Dialog
    this.$root.$on('ShowAlert', (alert) =>{
      this.alert = {
        active: true,
        title: alert.title || "",
        content: alert.content || ""
      };
    });

    //Show Confirmation Dialog
    this.$root.$on('ShowConfirmation', (confirmation) =>{
      this.confirmation = {
        active: true,
        title: confirmation.title || "",
        content: confirmation.content || "",
        confirmText: confirmation.confirmText || "Confirmer",
        cancelText: confirmation.cancelText || "Annuler",
        onCancel: () => { this.confirmation.sync = false },
        onConfirm: () => confirmation.onConfirm()
      };
    });
  }
}
</script>

