<style src="./preavisExtComment.css" scoped></style>
<template src="./preavisExtComment.html"></template>


<script>

export default {
  name: "PreavisExtComment",
  props: {
    remarque: {
      type: String,
      default() { return null }
    },
    disabled: {
      type: Boolean,
      default() { return true }
    },
    glossaire: {
      type: Array,
      default() { return [] }
    },
  },

  emits: ['update:remarque'],

  methods: {
    addGlossaireText(text) {
      if (!this.value) {
        this.value = text;
      } else {
        this.value += '\n\n' + text;
      }
    },
  },

  computed: {
    value: {
      get() {
        return this.remarque;
      },
      set(val) {
        this.$emit('update:remarque', val);
      }
    },
  },
};

</script>
