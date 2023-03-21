<style src="./preavisExtComment.css"></style>
<template src="./preavisExtComment.html"></template>


<script>

export default {
  name: "PreavisExtComment",
  props: {
    glossaire: {
      type: Array,
      default() { return [] }
    },
    commentaire: {
      type: String,
      default() { return null }
    },
    disabled: {
      type: Boolean,
      default() { return false }
    },
  },
  // data: () => {
  //   return {
  //   };
  // },

  // methods: {
  // },
};

</script>
