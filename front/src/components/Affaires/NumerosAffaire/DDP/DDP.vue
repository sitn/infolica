<style src="./ddp.css" scoped></style>
<style lang="css">
.md-menu-content {
  z-index: 9000 !important;
}
</style>
<template src="./ddp.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "DDP",
  props: {
    affaire: { type: Object },
    numero: { type: Object },
    numeroBaseListe: { type: Array },
    types_numeros: { type: Object },
  },

  data: () => {
    return {
      form: {
        numeroBase: null,
      },
      searchBFBase: null,
      showDDPDialog: false,
    };
  },

  methods: {

    /**
     * On cancel creation DDP
     */
    onCancelDDP() {
      this.form.numeroBase = null;
      this.showDDPDialog = false;
    },

    /**
     * On cancel creation DDP
     */
    onConfirmDDP() {

      let formData = new FormData();
      formData.append("base", this.form.numeroBase.id);
      formData.append("ddp", this.numero.numero_id);
      formData.append("affaire_id", this.affaire.id);

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DDP_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(() => {
        this.$root.$emit("removeCurrentDDPpotential", this.numero);
        this.$root.$emit("searchAffaireNumeros");

        this.$root.$emit("showMessage", "Le DDP " + this.numero.numero + " a bien été enregistré sur le bien-fonds: " + this.form.numeroBase.nom);

        this.onCancelDDP();
      })
        .catch(err => handleException(err, this));

    },


    /**
     * Filter BF
     */
    filterBF() {
      let regExp = new RegExp("[0-9]{1,}");
      let tmp = this.numeroBaseListe.filter(x => {

        if (regExp.test(x.nom)) {
          return regExp.exec(x.nom)[0] === String(this.searchBFBase);
        }
        return false
      });

      if (!tmp.length > 0) {
        alert("Aucun numéro ne correspond à la recherche.");
      } else if (tmp.length > 1) {
        alert("Curieux! Il y a plusieurs biens-fonds correspondant à la recherche...");
      } else {
        this.form.numeroBase = tmp[0];
        this.searchBFBase = null;
      }
    },

  },

};
</script>

