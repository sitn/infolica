<style src="./preavisExtComment.css" scoped></style>
<template src="./preavisExtComment.html"></template>


<script>

export default {
  name: "PreavisExtComment",
  props: {
    value: {
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

  data() {
    return {
      foo: null
    }
  },

  methods: {
    addGlossaireText(text) {
      if (!this.foo) {
        this.foo = text;
      } else {
        this.foo += '\n\n' + text;
      }
    },

    loadFoo() {
      this.foo = this.value;
    }
  },

  computed: {
    inputVal: {
      get() {
        return this.foo;
      },
      set(val) {
        this.foo = val;
        this.$emit('input', val);
      }
    },
  },

  mounted: function() {
    this.loadFoo();
  }
};

</script>
