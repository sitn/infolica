<style src="./referenceNumeros.css" scoped></style>
<template src="./referenceNumeros.html"></template>


<script>
import { getCadastres } from "@/services/helper";
import { handleException } from '@/services/exceptionsHandler'
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  name: "ReferenceNumeros",
  props: {
    affaire_numeros_anciens: {type: Array, default: () => []},
    cadastre_id: {type: Number, default: null},
    saveNumerosReferences: {type: Function, default: () => {alert("Echec de l'enregistrement")}},
  },
  mixins: [validationMixin],
  components: {},
  data() {
    return {
      showReferenceDialog: false,
      numeros_liste: [],
      cadastre_liste: [],
      numeros_etats_liste: [],
      numeros_types_liste: [],
      selectedNumeros: [],
      isModeCreate: false,
      isModeCreatePPE: false,
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

  // Validations
  validations() {
    if (!this.isModeCreatePPE) {
      // formulaire pour les biens-fonds autre que unité de PPE
      return {
        search: {
          cadastre: { required },
          numero: { required },
          etat: { required },
          type: { required }
        }
      };
    } else {
      // formulaire pour les unités de PPE
      return {
        search: {
          cadastre: { required },
          numero: { required },
          suffixe: { required },
          etat: { required },
          type: { required }
        }
      };
    }
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

      this.isModeCreate = false;
      this.isModeCreatePPE = false;

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
        formData.append("numero", this.search.numero);
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
          etat: {
            id: 2,
            nom: "Vigueur",
            toLowerCase: () => "Vigueur".toLowerCase(),
            toString: () => "Vigueur"
          },
          type: {
            id: 1,
            nom: "Bien-fonds",
            toLowerCase: () => "Bien-fonds".toLowerCase(),
            toString: () => "Bien-fonds"
          },
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

    /**
     * Créer le nouveau numéro dans la base
     */
    onConfirmCreateNumero() {
      var formData = new FormData();
      if (this.search.cadastre) {
        formData.append("cadastre_id", this.search.cadastre.id);
      }
      if (this.search.numero) {
        formData.append("numero", this.search.numero);
      }
      if (this.search.suffixe) {
        formData.append("suffixe", this.search.suffixe);
      }
      if (this.search.type) {
        formData.append("type_id", this.search.type.id);
      }
      if (this.search.etat) {
        formData.append("etat_id", this.search.etat.id);
      }

      // Enregistrer le numéro
      this.$http
        .post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.success = {
              check: true,
              txt:
                "Le numéro " +
                this.search.numero +
                " a été créé sur le cadastre de " +
                this.search.cadastre.nom +
                " avec succès"
            };
            this.initNumerosList();
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Get validation class par fieldname
     */
    getValidationClass(fieldName) {
      // ne pas effectuer les contrôles pour la recherche de numéros
      // seulement pour enregistrer un nouveau numéro
      if (this.isModeCreate) {
        const field = this.$v.search[fieldName];

        if (field) {
          return {
            "md-invalid": field.$invalid && field.$dirty
          };
        }
      } else {
        return { "md-invalid": false };
      }
    },

    /**
     * Validate form
     */
    validateForm() {
      this.isModeCreate = true;

      // ne pas signaler le champ "unité vide" si le type de numéro n'est pas unité de PPE
      const numero_type_ppe_id = Number(process.env.VUE_APP_NUMERO_TYPE_PPE);
      if (this.search.type) {
        if (this.search.type.id === numero_type_ppe_id) {
          this.isModeCreatePPE = true;
        }
      }

      this.$v.$touch();

      if (!this.$v.$invalid) {
        if (this.search.type.id !== numero_type_ppe_id) {
          this.search.suffixe = null;
        }
        this.onConfirmCreateNumero();
      }
    }
  },

  mounted: function() {
    this.initCadastresList();
    this.initNumerosEtatsList();
    this.initNumerosTypesList();
  }
};
</script>

