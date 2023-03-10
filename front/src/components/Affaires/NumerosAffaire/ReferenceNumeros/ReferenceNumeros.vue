<style src="./referenceNumeros.css"></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./referenceNumeros.html"></template>


<script>
import { getCadastres } from "@/services/helper";
import { handleException } from '@/services/exceptionsHandler'

export default {
  name: "ReferenceNumeros",
  props: {
    affaire_numeros_anciens: {type: Array, default: () => []},
    cadastre_id: {type: Number, default: null},
    saveNumerosReferences: {type: Function, default: () => {alert("Echec de l'enregistrement")}},
    dialogTitle: {type: String, default: () => 'Référencer des numéros'},
    selectionType: {type: String, default: () => 'multiple'},
  },
  components: {},
  data() {
    return {
      showReferenceDialog: false,
      numeros_liste: [],
      cadastre_liste: [],
      numeros_etats_liste: [],
      numeros_types_liste: [],
      selectedNumeros: [],
      search: {
        cadastre: null,
        numero: null,
        suffixe: null,
        etat: null,
        type: null
      },
      success: {
        check: false,
        txt: null
      }
    };
  },

  methods: {
    /**
     * Open référence numéros dialog
     */
    async openReferenceDialog(searchTerms=null) {
      await this.initializeForm().then(() => {
        this.initNumerosList(searchTerms);
        this.showReferenceDialog = true;
      });
    },

    /*
     * Init Cadastres list
     */
    async initCadastresList() {
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
     * Init Numeros list
     */
    async initNumerosList(searchTerms=null) {
      if (searchTerms) {
        if (searchTerms && searchTerms.type_id){
          this.search.type = this.numeros_types_liste.filter(x => x.id === searchTerms.type_id)[0];
        }
      }

      // Récupère les id des numéros référencés dans l'affaire
      let numerosReferencesId = this.affaire_numeros_anciens.map(x => x.numero_id);

      var formData = new FormData();
      if (this.search.cadastre) {
        formData.append("cadastre_id", this.search.cadastre.id);
      }
      if (this.search.type) {
        formData.append("type_numero_id", this.search.type.id);
      }
      if (this.search.etat) {
        formData.append("etat_id", this.search.etat.id);
      }
      if (this.search.numero) {
        formData.append("%numero", this.search.numero);
      }
      if (this.search.suffixe) {
        formData.append("suffixe", this.search.suffixe);
      }
      if (numerosReferencesId) {
        formData.append("_id", JSON.stringify(numerosReferencesId));
      }

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RECHERCHE_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.numeros_liste = response.data;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init Numeros etat liste
     */
    async initNumerosEtatsList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.numeros_etats_liste = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom.toString()
            }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /*
     * Init Numeros type liste
     */
    async initNumerosTypesList() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.numeros_types_liste = response.data.map(x => ({
              id: x.id,
              nom: x.nom,
              toLowerCase: () => x.nom.toLowerCase(),
              toString: () => x.nom.toString()
            }));
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },


    /**
     * Référencer des numéros
     */
    async onConfirmReferenceNumeros(items) {
      this.saveNumerosReferences(items)
      .then(() => {})
      .catch(err => handleException(err, this));
      
      this.showReferenceDialog = false;
      this.initializeForm();
    },

    /**
     * Annuler la réservation de numéros
     */
    onCancelReferenceNumeros() {
      this.showReferenceDialog = false;
      this.initializeForm();
    },

    /**
     * Initialise le formulaire de réservation de numéros
     */
    async initializeForm() {
      // Récupérer le cadastre
      const cadastre = this.cadastre_liste.filter(x => x.id === this.cadastre_id)[0];

      return new Promise(resolve => {
        this.search = {
          cadastre: cadastre,
          etat: null,
          type: null,
          numero: null,
          suffixe: null
        };
        resolve(this.search);
      });
    },

    /**
     * Récupérer la sélection des biens-fonds à référencer
     */
    onSelect(items) {
      this.selectedNumeros = items;
    },

  },

  mounted: function() {
    this.initCadastresList();
    this.initNumerosEtatsList();
    this.initNumerosTypesList();
  }
};
</script>

