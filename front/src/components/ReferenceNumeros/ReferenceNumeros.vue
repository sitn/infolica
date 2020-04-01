<style src="./referenceNumeros.css" scoped></style>
<template src="./referenceNumeros.html"></template>


<script>
import { checkLogged, getCadastres } from "@/services/helper";

export default {
  name: "ReferenceNumeros",
  props: {},
  components: {},
  data: () => {
    return {
      showReferenceDialog: false,
      cadastre_liste: [],
      numeros_liste: [],
      numeros_etats_liste: [],
      numeros_types_liste: [],
      selectedNumeros: null,
      search: {
        cadastre: null,
        numero: null,
        etat: null,
        type: null
      }
    };
  },

  methods: {
    /**
     * Open référence numéros dialog
     */
    async openReferenceDialog() {

      await this.initializeForm().then(() => {
        this.initNumerosList();
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
            alert("error: " + err.message)
          });
    },

    /*
     * Init Numeros list
     */
    async initNumerosList() {
      var formData = new FormData();
      if (this.search.cadastre)
        formData.append("cadastre_id", this.search.cadastre.id);
      if (this.search.type)
        formData.append("type_numero_id", this.search.type.id);
      if (this.search.etat) formData.append("etat_id", this.search.etat.id);
      if (this.search.numero) formData.append("numero", this.search.numero);

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
          alert("error: " + err.message);
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
            alert("error: " + err.message)
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
            alert("error: " + err.message)
          });
    },

    /*
     * Init default cadastre
     */
    async initDefaultCadastre() {
      return new Promise((resolve, reject) => {
        var affaire_cadastre;

        this.$http
          .get(
            process.env.VUE_APP_API_URL +
              process.env.VUE_APP_AFFAIRES_ENDPOINT +
              this.$route.params.id,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            if (response && response.data) {
              affaire_cadastre = {
                id: response.data.cadastre_id,
                nom: response.data.cadastre,
                toLowerCase: () => response.data.cadastre.toLowerCase(),
                toString: () => response.data.cadastre
              };
            }
            resolve(affaire_cadastre);
          })
          .catch(() => reject);
      });
    },

    /**
     * Create numeros
     */
    onConfirmReferenceNumeros() {
      var formData = new FormData();
      // if (this.reservation.cadastre.id)
      //   formData.append("cadastre_id", this.reservation.cadastre.id);
      // formData.append("affaire_id", this.$route.params.id);
      // if (this.reservation.nb_bf) formData.append("bf", this.reservation.nb_bf);
      // if (this.reservation.nb_ddp)
      //   formData.append("ddp", this.reservation.nb_ddp);
      // if (this.reservation.nb_ppe)
      //   formData.append("ppe", this.reservation.nb_ppe);
      // if (this.reservation.ppe_suffixe_start)
      //   formData.append("ppe_unite", this.reservation.ppe_suffixe_start);
      // if (this.reservation.nb_pcop)
      //   formData.append("pcop", this.reservation.nb_pcop);
      // if (this.reservation.nb_pfp3)
      //   formData.append("pfp3", this.reservation.nb_pfp3);
      // if (this.reservation.nb_paux)
      //   formData.append("paux", this.reservation.nb_paux);
      // if (this.reservation.nb_bat)
      //   formData.append("bat", this.reservation.nb_bat);
      // if (this.reservation.nb_pcs)
      //   formData.append("pcs", this.reservation.nb_pcs);
      // if (this.reservation.plan_id)
      //   formData.append("plan_id", this.reservation.plan_id);

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_RESERVATION_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            this.$parent.searchAffaireNumeros();
          }
        })
        .catch(err => {
          alert("error: " + err);
        });
      this.showReferenceDialog = false;
      this.initializeForm();
    },

    /**
     * Annuler la réservation de uméros
     */
    onCancelReferenceNumeros() {
      this.showReferenceDialog = false;
      this.initializeForm();
    },

    /**
     * Initialise le formulaire de réservation de numéros
     */
    async initializeForm() {
      this.search.cadastre = await this.initDefaultCadastre();

      return new Promise(resolve => {
        this.search.etat = {
          id: 2,
          nom: "Vigueur",
          toLowerCase: () => "Vigueur".toLowerCase(),
          toString: () => "Vigueur"
        };
        this.search.type = {
          id: 1,
          nom: "Bien-fonds",
          toLowerCase: () => "Bien-fonds".toLowerCase(),
          toString: () => "Bien-fonds"
        };
        resolve(this.search);
      });
    },

    /**
     * Enregistrer la sélection des biens-fonds référencés
     */
    onSelect(items) {
      this.selectedNumeros = items;
    },

  },

  mounted: function() {
    checkLogged();
    this.initCadastresList();
    this.initNumerosEtatsList();
    this.initNumerosTypesList();
  }
};
</script>

