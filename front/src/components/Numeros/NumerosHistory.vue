<style src="./numerosHistory.css" scoped></style>
<template src="./numerosHistory.html"></template>


<script>
import { getCadastres } from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'

export default {
  name: "NumerosHistory",
  props: {},
  data: () => ({
    cadastre_liste: [],
    numero: [],
    numero_affaires: [],
    numero_provenance: [],
    numero_destination: [],
    search: {
      cadastre: null,
      numero: null
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
          process.env.VUE_APP_NUMEROS_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.numero = response.data;
            this.search.cadastre = this.numero.cadastre;
            this.search.numero = this.numero.numero;
            this.numero.diff = "Non";
            if (this.numero.diff_entree && !this.numero.diff_sortie) {
              this.numero.diff = "Oui";
            }
            if (!this.numero.suffixe){
              this.numero.suffixe = "-"
            }
          }
        }).catch(err => {
          handleException(err, this);
        });
    },


    /*
     * Init Cadastres list
     */
    initCadastresList() {
      getCadastres()
      .then(response => {
        if (response && response.data) {
          this.cadastre_liste = response.data.map(function(obj) {
            return obj.nom;
          });
        }
      }).catch(err => {
        handleException(err, this);
      });
    },


    /*
     * Get affaires par numéro
     */
    async getNumeroAffaires() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMERO_AFFAIRES_ENDPOINT +
          this.$route.params.id,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
        ).then(response => {
          if (response && response.data) {
            this.numero_affaires = response.data;
          }
        }).catch(err => {
          handleException(err, this);
        })
    },


    /*
     * Get Numero_provenance
     */
    async getNumeroProvenance() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMERO_RELATIONS_BASE_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response.data) {
            this.numero_provenance = response.data.map(function(obj) {
              return obj.numero_base_numero;
            });
          } else {
            this.numero_provenance = "-"
          }
        }).catch(err => {
          handleException(err, this);
        });
    },


    /*
     * Get Numero_destination
     */
    async getNumeroDestination() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMERO_RELATIONS_ASSOCIE_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response.data) {
            this.numero_destination = response.data.map(function(obj) {
              return obj.numero_associe_numero;
            });
          } else {
            this.numero_destination = "-"
          }
        }).catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Open numéro in new tab
     */
    doOpenAffaire(id) {
      let routeData = this.$router.resolve('/affaires/' + id);
      window.open(routeData.href, '_blank');
    }
  },

  mounted: function() {
    this.getNumeroById();
    this.initCadastresList();
    this.getNumeroAffaires();
    this.getNumeroProvenance();
    this.getNumeroDestination();
  }
};
</script>

