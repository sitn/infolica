<style src="./numeros.css" scoped></style>
<template src="./numeros.html"></template>


<script>
import {
  getCadastres,
  getTypesNumeros,
  getEtatsNumeros,
  stringifyAutocomplete
} from "@/services/helper";
import {handleException} from '@/services/exceptionsHandler'

export default {
  name: "Numeros",
  props: {},
  data: () => ({
    numeros: [],
    affaireNumerosMO: [],
    affaireNumerosMO_limitStatus: false,
    numerosMO: [],
    cadastre_liste: [],
    types_numeros: [],
    types_numeros_mo: [],
    types_numeros_mo_bf: [],
    etats_numeros: [],
    search: {
      numero: null,
      suffixe: null,
      cadastre: "",
      type: "",
      etat: "",
      matDiff: false,
    },
    searchNumeroMO: {
      cadastre: null,
      type: null,
      plan: null
    },
    searchAffaireNumeroMO: {
      numero: null,
      type: null,
      cadastre: null,
      plan: null
    },
    emptyResultNumeros: false,
    emptyResultNumerosMO: false,
    emptyResultAffaireNumerosMO: false,
  }),

  methods: {
    /*
     * SEARCH NUMEROS
     */
    async searchNumeros() {
      var formData = new FormData();
      if (this.search.numero) {
        formData.append("numero", this.search.numero);
      }
      if (this.search.suffixe) {
        formData.append("suffixe", this.search.suffixe);
      }
      if (this.search.cadastre) {
        formData.append("cadastre_id", this.search.cadastre.id);
      }
      if (this.search.type) {
        formData.append("type_numero_id", this.search.type.id);
      }
      if (this.search.etat) {
        formData.append("etat_id", this.search.etat.id);
      }
      if (this.search.matDiff) {
        formData.append("matDiff", this.search.matDiff);
      }

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RECHERCHE_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data && response.data.length > 0) {
            this.numeros = response.data;
            this.emptyResultNumeros = false;
          } else {
            this.emptyResultNumeros = true;
          }
        })
        .catch(err => {
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
            this.cadastre_liste = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })

        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init Types Numeros list
     */
    async initTypesNumerosList() {
      getTypesNumeros()
        .then(response => {
          if (response && response.data) {
            this.types_numeros = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })

        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init Etats Numeros list
     */
    async initEtatsNumerosList() {
      getEtatsNumeros()
        .then(response => {
          if (response && response.data) {
            this.etats_numeros = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom
            }));
          }
        })

        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Clear the form
     */
    clearForm() {
      this.search.numero = null;
      this.search.suffixe = null;
      this.search.cadastre = "";
      this.search.type = "";
      this.search.etat = "";
      this.search.matDiff = false;
      this.numeros = [];
      this.emptyResultNumeros = false;
    },

    // ------------------ NUMEROS MO ------------------

    /**
     * get next numero mo by cadastre, type and plan
     */
    async getNextNumeroMO() {
      let searchParams = [];
      if (this.searchNumeroMO.cadastre && this.searchNumeroMO.cadastre.id) {
        searchParams.push('cadastre_id=' + this.searchNumeroMO.cadastre.id);
      }
      if (this.searchNumeroMO.type && this.searchNumeroMO.type.id) {
        searchParams.push('type_id=' + this.searchNumeroMO.type.id);
      }
      if (this.searchNumeroMO.plan) {
        searchParams.push('plan=' + this.searchNumeroMO.plan);
      }

      if (searchParams.length === 0) {
        alert("Il faut renseigner au moins un des trois champs: cadastre, type ou plan");
        return;
      }

      searchParams = "?" + searchParams.join("&");

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_NEXT_NUMERO_MO_AVAILABLE_ENDPOINT + searchParams,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data){
          if (response.data.length > 0) {
            this.numerosMO = response.data;
            this.emptyResultNumerosMO = false;
          } else {
            this.numerosMO = [];
            this.emptyResultNumerosMO = true;
          }
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * Get liked affaire from number of MO
     */
    async getAffaireNumeroMO() {
      let searchParams = [];
      if (this.searchAffaireNumeroMO.numero) {
        searchParams.push('numero=' + this.searchAffaireNumeroMO.numero);
      } else {
        alert(`Le champ "numéro" doit être renseigné`);
        return;
      }
      if (this.searchAffaireNumeroMO.type && this.searchAffaireNumeroMO.type.id) {
        searchParams.push('type_id=' + this.searchAffaireNumeroMO.type.id);
      }
      if (this.searchAffaireNumeroMO.cadastre && this.searchAffaireNumeroMO.cadastre.id) {
        searchParams.push('cadastre_id=' + this.searchAffaireNumeroMO.cadastre.id);
      }
      if (this.searchAffaireNumeroMO.plan) {
        searchParams.push('plan=' + this.searchAffaireNumeroMO.plan);
      }

      if (searchParams.length === 0) {
        alert("Il faut renseigner au moins un des quatre champs: numero, type, cadastre, ou plan");
        return;
      }

      searchParams = "?" + searchParams.join("&");

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMERO_MO_ENDPOINT + searchParams,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          if (response.data.data.length > 0) {
            this.affaireNumerosMO = response.data.data;
            this.affaireNumerosMO_limitStatus = response.data.limitStatus==="true"? true: false;
            this.emptyResultAffaireNumerosMO = false;
          } else {
            this.affaireNumerosMO = [];
            this.emptyResultAffaireNumerosMO = true;
          }
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * get numero mo types
     */
    getNumeroMoTypes() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_NUMEROS_MO_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          this.types_numeros_mo = stringifyAutocomplete(tmp).sort((a,b) => (a.nom > b.nom) ? 1 : ((b.nom > a.nom) ? -1 : 0));
          tmp.push({id: 1, nom: "Bien-fonds", ordre: 1, toLowerCase: () => "bien-fonds", toString: () => "Bien-fonds"});
          this.types_numeros_mo_bf = stringifyAutocomplete(tmp).sort((a,b) => (a.nom > b.nom) ? 1 : ((b.nom > a.nom) ? -1 : 0));
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Effacer les champs de recherche des numéros de la MO ainsi que le résultat
     */
    clearNumerosMOForm() {
      this.searchNumeroMO = {
        cadastre: null,
        type: null,
        plan: null,
      };

      this.numerosMO = [];
      this.emptyResultNumerosMO = false;
    },

    clearAffaireNumerosMOForm() {
      this.searchAffaireNumeroMO = {
        numero: null,
        type: null,
        cadastre: null,
        plan: null,
      };

      this.affaireNumerosMO = [];
      this.emptyResultAffaireNumerosMO = false;
    }

  },

  mounted: function() {
    this.initCadastresList();
    this.initTypesNumerosList();
    this.initEtatsNumerosList();
    this.getNumeroMoTypes();
  }
};
</script>

