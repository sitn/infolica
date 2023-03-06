<style src="./ddp.css" scoped></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./ddp.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "DDP",
  props: {
    affaire: {type: Object},
    numero: {type: Object},
    numeroBaseListe: {type: Array},
    types_numeros: {type: Object},
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
      let promises = [];
      promises.push(this.updateNumero());
      promises.push(this.postNumerosRelation());
      promises.push(this.postAffaireNumero(this.numero.numero_id, process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID));
      promises.push(this.postAffaireNumero(this.form.numeroBase.id, process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID));

      Promise.all(promises).then(() => {
        this.$root.$emit("removeCurrentDDPpotential", this.numero);
        
        this.$root.$emit("showMessage", "Le DDP " + this.numero.numero + " a bien été enregistré sur le bien-fonds: " + this.form.numeroBase.nom);
        this.$root.$emit("searchAffaireNumeros");

        this.onCancelDDP();
      }).catch(err => handleException(err, this));
    },

    /**
     * Post numero_relation
     */
    async postNumerosRelation() {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("numero_id_base", this.form.numeroBase.id);
        formData.append("numero_id_associe", this.numero.numero_id);
        formData.append("relation_type_id", Number(process.env.VUE_APP_RELATION_TYPE_DDP_ID));
        formData.append("affaire_id", this.affaire.id);

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },
    
    /**
     * Post affaire_numero
     */
    async postAffaireNumero(numero_id, affaireNumeroType) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("affaire_id", this.affaire.id);
        formData.append("numero_id", numero_id);
        formData.append("type_id", Number(affaireNumeroType));
        formData.append("actif", true);

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

    /**
     * update numero type
     */
    async updateNumero() {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("id", this.numero.numero_id);
        formData.append("type_id", this.types_numeros.ddp);

        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
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
        this.form.numeroBase = tmp [0];
        this.searchBFBase = null;
      }
    },

  },

};
</script>

