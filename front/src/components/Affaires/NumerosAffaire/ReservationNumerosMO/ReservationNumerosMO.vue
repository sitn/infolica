<style src="./reservationNumerosMO.css" scoped></style>
<template src="./reservationNumerosMO.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import { checkPermission,  } from "@/services/helper";

// const moment = require("moment");

export default {
  name: "ReservationNumerosMO",
  props: {
    affaire: Object,
    typesAffaires: Object,
  },
  components: {},
  data: () => {
    return {
      reservationNumerosMO: [],
      showReservationNumerosMO: true,
    };
  },

  methods: {
    /*
     * SEARCH reservation numeros MO by affaire_id
     */
    async searchReservationNumerosMO() {
      this.$http
      .get(
        process.env.VUE_APP_API_URL +
          process.env.VUE_APP_RESERVATION_NUMEROS_MO_ENDPOINT + "/" +
          this.$route.params.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      )
      .then(response => {
        if (response && response.data) {
          this.reservationNumerosMO = response.data;
          this.reservationNumerosMO.forEach(x => x.nombre = x.numero_a - x.numero_de + 1);
        }
      })
      .catch(err => {
        handleException(err, this);
      });
    },


    // /**
    //  * Contrôler qu'un numéro de référence n'est pas une numéro de base pour un numéro
    //  * réservé dans l'affaire
    //  */
    // isNumeroBaseInAffaire(numero) {
    //   // Filtrer les numéros de base
    //   var numerosAssocies = this.affaire_numeros_nouveaux.filter(x => {
    //     return parseInt(x.numero_base_id) == parseInt(numero.numero_id);
    //   });
    //   // Créer un array avec les numéros pour l'affichage du message
    //   var numerosAssociesArray = [];
    //   numerosAssocies.forEach(x => numerosAssociesArray.push(x.numero));
    //   // Empêcher la suppression si des numéros sont définis sur le numéro de base, supprimer sinon
    //   if (numerosAssocies[0]) {
    //     this.$root.$emit(
    //       "ShowError",
    //       "Les immeubles " +
    //         numerosAssociesArray.join() +
    //         " sont définis sur l'immeuble " +
    //         numero.numero
    //     );
    //     return true;
    //   } else {
    //     return false;
    //   }
    // },


    // /**
    //  * Abandonner/rétablir un numéro réservé
    //  */
    // onDeleteReserveNumero(numero_id) {
    //   // get numéro pour l'update
    //   var numero_ = {};
    //   this.$http
    //     .get(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_NUMEROS_ENDPOINT +
    //         numero_id,
    //       {
    //         withCredentials: true,
    //         headers: { Accept: "application/json" }
    //       }
    //     )
    //     .then(response => {
    //       if (response.data) {
    //         numero_ = response.data;
    //         this.updateNumero(numero_);
    //       }
    //     })
    //     .catch(err => {
    //       handleException(err, this);
    //     });
    // },

    // /**
    //  * Update Numero
    //  */
    // async updateNumero(numero_) {
    //   this.$http
    //     .delete(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_NUMEROS_ENDPOINT +
    //         numero_.id,
    //       {
    //         withCredentials: true,
    //         headers: { Accept: "application/json" }
    //       }
    //     )
    //     .then(response => {
    //       if (response && response.status === 200) {
    //         this.searchAffaireNumeros();
    //         // Afficher le changement d'état
    //         var etat = "Abandonné";
    //         if (numero_.etat === "Abandonné") {
    //           etat = "Projet";
    //         }
    //         this.$root.$emit(
    //           "ShowMessage",
    //           "L'état du numéro " +
    //             numero_.numero +
    //             " est passé à '" +
    //             etat +
    //             "'"
    //         );
    //       }
    //     })
    //     .catch(err => {
    //       handleException(err, this);
    //     });
    // },

    // /**
    //  * Ouvrir la boîte de dialogue de référence de numéros
    //  */
    // callOpenReferenceDialog() {
    //   this.$refs.formReference.openReferenceDialog();
    // },

    // /**
    //  * Ouvrir la boîte de dialogue de réservation de numéros
    //  */
    // callOpenReservationDialog() {
    //   this.affaire_id = Number(this.$route.params.id);
    //   this.$refs.formReservation.openReservationDialog();
    // },

    // /**
    //  * Ouvrir le dialog de quittance de réservation de PCOP
    //  */
    // callOpenQuittancePCOPDialog() {
    //   this.$refs.formQuittancePCOP.openQuittancePCOPDialog();
    // },

    // /**
    //  * Créer Différer un numéro
    //  */
    // doCreateDiffererNumero(numero) {
    //   var formData = new FormData();
    //   formData.append("numero_id", numero.numero_id);
    //   formData.append("affaire_id", this.$route.params.id)
    //   formData.append(
    //     "date_entree",
    //     moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(
    //       process.env.VUE_APP_DATEFORMAT_WS
    //     )
    //   );

    //   this.$http
    //     .post(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
    //       formData,
    //       {
    //         withCredentials: true,
    //         headers: { Accept: "application/json" }
    //       }
    //     )
    //     .then(response => {
    //       if (response && response.data) {
    //         this.searchAffaireNumeros();
    //         this.$root.$emit(
    //           "ShowMessage",
    //           "Le numéro " + numero.numero + " a été différé"
    //         );
    //       }
    //     })
    //     .catch(err => {
    //       handleException(err, this);
    //     });
    // },

    // /**
    //  * Mettre à jour Différer un numéro
    //  */
    // doUpdateDiffererNumero(numero) {
    //   var formData = new FormData();
    //   formData.append("numero_diff_id", numero.numero_diff_id);
    //   formData.append("numero_id", numero.numero_id);
    //   formData.append("date_entree", numero.numero_diff_entree);
    //   formData.append(
    //     "date_sortie",
    //     moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(
    //       process.env.VUE_APP_DATEFORMAT_WS
    //     )
    //   );

    //   this.$http
    //     .put(
    //       process.env.VUE_APP_API_URL +
    //         process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
    //       formData,
    //       {
    //         withCredentials: true,
    //         headers: { Accept: "application/json" }
    //       }
    //     )
    //     .then(response => {
    //       if (response && response.data) {
    //         this.searchAffaireNumeros();
    //         this.$root.$emit(
    //           "ShowMessage",
    //           "La mention 'différé' du numéro " +
    //             numero.numero +
    //             " a été correctement supprimée"
    //         );
    //       }
    //     })
    //     .catch(err => {
    //       handleException(err, this);
    //     });
    // },

    // // /**
    // //  * Get immeubles associes
    // //  */
    // // async getImmeublesAssocies() {
    // //   return new Promise((resolve, reject) => {
    // //     // Récupère la liste des id des numéros référencés
    // //     var numeros_base_id_list = this.affaire_numeros_anciens.map(x => x.numero_id);
  
    // //     var formData = new FormData();
    // //     formData.append("numeros_base_id_list", JSON.stringify(numeros_base_id_list));
  
    // //     this.$http.post(
    // //       process.env.VUE_APP_API_URL +
    // //       process.env.VUE_APP_NUMEROS_RELATIONS_BY_NUMEROSBASEID_ENDPOINT,
    // //       formData,
    // //       {
    // //         withCredentials: true,
    // //         headers: {'Content-type': 'application/json'},
    // //       }
    // //     )
    // //     .then(response => {if (response && response.data) resolve(response.data)})
    // //     .catch(err => reject(err));
    // //   });
    // // },

    // /**
    //  * Afficher la balance si c'est une affaire de division
    //  */
    // async showBalance_() {
    //   this.showBalance = await this.affaire.type_id === Number(process.env.VUE_APP_TYPE_AFFAIRE_DIVISION);
    // },

    // /**
    //  * Génère une quittance des numéros réservés dans l'affaire
    //  */
    // async doQuittanceNumerosReserves() {
    //   let tmp = this.getCadastresNumerosNumerosBases(this.affaire_numeros_nouveaux);
    //   let cadastres = tmp[0];
    //   let numeros = tmp[1];
    //   let numeros_bases = tmp[2];

    //   let formData = new FormData();
    //   formData.append("template", "NumerosReserves");
    //   formData.append("values", JSON.stringify({
    //     "affaire_id": this.affaire.id,
    //     "date": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
    //     "cadastre": cadastres,
    //     "numero": numeros,
    //     "numero_base": numeros_bases
    //   }));

    //   getDocument(formData).then(response => {
    //     this.$root.$emit("ShowMessage", "Le fichier '" + response + " se trouve dans le dossier 'Téléchargement'");
    //   }).catch(err => handleException(err, this));
    // },

    // /**
    //  * Return lists of cadastre, numero and numero_base for quittance numeros_reserves
    //  */
    // getCadastresNumerosNumerosBases(numeros_reserves) {
    //   let cadastres = [];
    //   let numeros = [];
    //   let numeros_bases = [];

    //   numeros_reserves.forEach(x => {
    //     cadastres.push(x.numero_cadastre);
    //     numeros.push(x.numero_suffixe !== null? x.numero + " / " + x.numero_suffixe: x.numero);
    //     numeros_bases.push(x.numero_base);
    //   });

    //   cadastres = cadastres.join("\n");
    //   numeros = numeros.join("\n");
    //   numeros_bases = numeros_bases.join("\n");
    //   return [cadastres, numeros, numeros_bases];
    // }

  },
  mounted: function() {
    this.searchReservationNumerosMO();
    
    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_NUMERO_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



