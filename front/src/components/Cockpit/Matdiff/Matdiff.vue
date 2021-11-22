<style src="./matdiff.css" scoped></style>
<template src="./matdiff.html"></template>


<script>
import Matdiff_secr from "@/components/Cockpit/Matdiff/Matdiff_secr/Matdiff_secr.vue";
import Matdiff_mo from "@/components/Cockpit/Matdiff/Matdiff_mo/Matdiff_mo.vue";
import Matdiff_ctrl from "@/components/Cockpit/Matdiff/Matdiff_ctrl/Matdiff_ctrl.vue";


export default {
  name: "Matdiff",
  components: {
    Matdiff_secr,
    Matdiff_mo,
    Matdiff_ctrl
  },
  props: {
    operateurs: {type: Array},
    showMatdiff_secr: {type: Boolean},
    showMatdiff_mo: {type: Boolean},
    showMatdiff_ctrl: {type: Boolean},
  },
  data: () => {
    return {
      affaires: [{}],
      affaires_bk: [{}],
      plural: "",
      selectedOperateur_id: -1,
    }
  },
};
</script>

