<style src="./numerosHistory.css" scoped></style>
<template src="./numerosHistory.html"></template>


<script>
import { checkLogged } from "@/services/helper";

export default {
  name: "NumerosHistory",
  props: {},
  data: () => ({
    cadastre_liste: [],
    numero: [],
    search: {
      cadastre: null,
      numero: null,
    }
  }),

  methods: {
    /*
     * Get Numero_by_id
     */
    async getNumeroById() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMERO_BY_ID_ENDPOINT +
            this.$route.params.id
        )

        .then(response => {
          if (response && response.data) {
            this.numero = response.data;
            this.search.cadastre = this.numero.cadastre;
            this.search.numero = this.numero.numero;
            this.numero.diff = "Non"
            if (this.numero.diff_entree && !this.numero.diff_sortie) {
                this.numero.diff = "Oui"

            }
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    /*
     * Get Cadastres
     */
    async getCadastres() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT
        )

        .then(response => {
          if (response && response.data) {
            this.cadastre_liste = response.data.map(function(obj) {
              return obj.nom;
            });
          }
        })

        .catch(err => {
          alert("error: " + err.message);
        });
    },

    // /*
    //  * Get Types Numeros
    //  */
    // async getTypesNumeros() {
    //   this.$http
    //     .get(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT
    //     )

    //     .then(response => {
    //       if (response && response.data) {
    //         this.types_numeros = response.data.map(function(obj) {
    //           return obj.nom;
    //         });
    //       }
    //     })

    //     .catch(err => {
    //       alert("error: " + err.message);
    //     });
    // },

    // /*
    //  * Get Etats Numeros
    //  */
    // async getEtatsNumeros() {
    //   this.$http
    //     .get(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT
    //     )

    //     .then(response => {
    //       if (response && response.data) {
    //         this.etats_numeros = response.data.map(function(obj) {
    //           return obj.nom;
    //         });
    //       }
    //     })

    //     .catch(err => {
    //       alert("error: " + err.message);
    //     });
    // },

    /*
     * Clear the form
     */
    // clearForm() {
    //   this.search.cadastre = null;
    //   this.search.numero = null;
    // }

  },

  mounted: function() {
    checkLogged();
    this.getNumeroById();
    this.getCadastres();

  }
};
</script>

