<style src="./numerosAffaire.css" scoped></style>
<template src="./numerosAffaire.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import { getCurrentDate, saveDocument, getCurrentUserRoleId, stringifyAutocomplete, stringifyAutocomplete2 } from "@/services/helper";
import ReferenceNumeros from "@/components/Affaires/NumerosAffaire/ReferenceNumeros/ReferenceNumeros.vue";
import ReservationNumeros from "@/components/Affaires/NumerosAffaire/ReservationNumeros/ReservationNumeros.vue";
import QuittancePCOP from "@/components/Affaires/NumerosAffaire/QuittancePCOP/QuittancePCOP.vue";
import ReservationNumerosMO from "@/components/Affaires/NumerosAffaire/ReservationNumerosMO/ReservationNumerosMO.vue";
// import Balance from "@/components/Affaires/Balance/Balance.vue";
import BalanceFromFile from "@/components/Affaires/BalanceFromFile/BalanceFromFile.vue";


const moment = require("moment");

export default {
  name: "NumerosAffaire",
  props: {
    affaire: Object,
    typesAffaires_conf: Object,
    permission: Object
  },
  components: {
    ReferenceNumeros,
    ReservationNumeros,
    QuittancePCOP,
    ReservationNumerosMO,
    // Balance,
    BalanceFromFile
  },
  data: () => {
    return {
      affaire_id: null,
      affaire_numeros_all: [],
      affaire_numeros_anciens: [],
      affaire_numeros_mo: [],
      affaire_numeros_nouveaux: [],
      affaire_numeros_nouveaux_mo: [],
      confirmDialog: {
        show: false,
        title: '',
        content: '',
        onConfirm: () => {}
      },
      editMatDiffAllowed: false,
      numerosBaseListe: [],
      numerosMoLoading: true,
      show: {
        balance: false,
        deleteReferencedNumberColumn: false,
        numeros_references_card: false,
        numeros_reserves_card: false,
        numeros_reserves_immeuble_base: false,
        reservation_numeros_mo: false
      },
      showNumerosMO: true,
      showAlertMatDiffDialog: false,
      showQuittancePCOPDialog: false,
      types_numeros: {
        bf: Number(process.env.VUE_APP_NUMERO_TYPE_BF),
        ddp: Number(process.env.VUE_APP_NUMERO_TYPE_DDP),
        ppe: Number(process.env.VUE_APP_NUMERO_TYPE_PPE),
        pcop: Number(process.env.VUE_APP_NUMERO_TYPE_PCOP),
        pfp3: Number(process.env.VUE_APP_NUMERO_TYPE_PFP3),
        paux: Number(process.env.VUE_APP_NUMERO_TYPE_PAUX),
        bat: Number(process.env.VUE_APP_NUMERO_TYPE_BAT),
        pdet: Number(process.env.VUE_APP_NUMERO_TYPE_PDET),
        dp: Number(process.env.VUE_APP_NUMERO_TYPE_DP)
      },
      etatNumeros_conf: {
        projet: Number(process.env.VUE_APP_NUMERO_PROJET_ID),
        abandonne: Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
      }
      // numeros_base_relations: []
    };
  },

  methods: {
    /*
     * SEARCH AFFAIRE NUMEROS
     */
    async searchAffaireNumeros() {
      return new Promise((resolve, reject) => {

        this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT + "/" +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          const routeAffaireData = this.$router.resolve({ name: "Affaires" });

          if (response && response.data) {
            this.affaire_numeros_all = stringifyAutocomplete2(response.data, ["numero_sitn"]);
            this.affaire_numeros_all.forEach(x => {
              if (x.numero_id === Number(process.env.VUE_APP_NUMERO_DP_ID)) {
                x.numero_sitn = "DP";
                x.numero_cadastre = "-";
                x.numero_etat = "-";
              } else if (x.numero_id === Number(process.env.VUE_APP_NUMERO_RP_ID)) {
                x.numero_sitn = "RP";
                x.numero_cadastre = "-";
                x.numero_etat = "-";
              }
            })

            this.affaire_numeros_nouveaux = this.affaire_numeros_all.filter(
              x => x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID)
            );
            this.affaire_numeros_anciens = this.affaire_numeros_all.filter(
              x => x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID)
            );
            this.affaire_numeros_nouveaux.forEach(function(element) {
              if (element.numero_etat_id === Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)) {
                element.active = false;
              } else if (element.numero_etat_id === Number(process.env.VUE_APP_NUMERO_PROJET_ID)) {
                element.active = true;
              }
            });

            //Affaires links
            this.affaire_numeros_anciens.map( function(item) {
              item.affaire_destination_href = routeAffaireData.href + '/edit/' + item.affaire_destination_id;
              return item;
            });

            this.affaire_numeros_nouveaux.map( function(item) {
              item.affaire_destination_href = routeAffaireData.href + '/edit/' + item.affaire_destination_id;
              return item;
            });

            //Set nouveaux_numéros in component etape
            this.$root.$emit("setEtapeNouveauxNumeros", this.affaire_numeros_nouveaux);

            resolve(this.affaire_numeros_all, this.affaire_numeros_anciens, this.affaire_numeros_nouveaux);
          }
        })
        .catch(err => {
          handleException(err, this);
          reject;
        });
      })
    },


    /**
     * Contrôler qu'un numéro de référence n'est pas une numéro de base pour un numéro
     * réservé dans l'affaire
     */
    isNumeroBaseInAffaire(numero) {
      // Filtrer les numéros de base
      var numerosAssocies = this.affaire_numeros_nouveaux.filter(x => {
        return parseInt(x.numero_base_id) == parseInt(numero.numero_id);
      });
      // Créer un array avec les numéros pour l'affichage du message
      var numerosAssociesArray = [];
      numerosAssocies.forEach(x => numerosAssociesArray.push(x.numero));
      // Empêcher la suppression si des numéros sont définis sur le numéro de base, supprimer sinon
      if (numerosAssocies[0]) {
        this.$root.$emit(
          "ShowError",
          "Les immeubles " +
            numerosAssociesArray.join() +
            " sont définis sur l'immeuble " +
            numero.numero
        );
        return true;
      } else {
        return false;
      }
    },


    /**
     * Abandonner/rétablir un numéro réservé
     */
    onDeleteReserveNumero(numero_id) {
      // get numéro pour l'update
      var numero_ = {};
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_ENDPOINT +
            numero_id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            numero_ = response.data;
            this.updateNumero(numero_);
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Update Numero
     */
    async updateNumero(numero_) {
      this.$http
        .delete(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_ENDPOINT +
            numero_.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.status === 200) {
            this.searchAffaireNumeros();
            // Afficher le changement d'état
            var etat = "Abandonné";
            if (numero_.etat === "Abandonné") {
              etat = "Projet";
            }
            this.$root.$emit(
              "ShowMessage",
              "L'état du numéro " +
                numero_.numero +
                " est passé à '" +
                etat +
                "'"
            );
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Ouvrir la boîte de dialogue de référence de numéros
     */
    callOpenReferenceDialog() {
      this.$refs.formReference.openReferenceDialog();
    },

    /**
     * Ouvrir la boîte de dialogue de réservation de numéros
     */
    callOpenReservationDialog() {
      this.affaire_id = Number(this.$route.params.id);
      this.$refs.formReservation.openReservationDialog();
    },

    /**
     * Ouvrir le dialog de quittance de réservation de PCOP
     */
    callOpenQuittancePCOPDialog() {
      this.$refs.formQuittancePCOP.openQuittancePCOPDialog();
    },

    /**
     * Confirm create numero différé
     */
    confirmCreateDiffererNumero(numero, etat) {
      if (etat === "entree") {
        this.confirmDialog = {
          title: "Matérialisation différée",
          content: "Le numéro " + numero.numero + " aura la mention 'mat diff'.",
          show: true,
          onConfirm: () => this.doCreateDiffererNumero(numero)
        };
      } else if (etat === "sortie") {
        if (this.affaire.date_envoi !== null) {
          this.confirmDialog = {
            title: "Matérialisation différée",
            content: "Le numéro " + numero.numero + " a été matérialisé et la mention 'mat diff' va être supprimée.",
            show: true,
            onConfirm: () => this.doUpdateDiffererNumero(numero)
          };
        } else {
          this.showAlertMatDiffDialog = true;
        }
      }
    },

    /**
     * Créer Différer un numéro
     */
    async doCreateDiffererNumero(numero) {
      var formData = new FormData();
      formData.append("numero_id", numero.numero_id);
      formData.append("affaire_id", this.$route.params.id)
      formData.append("date_entree", moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.searchAffaireNumeros();
            this.$root.$emit("ShowMessage", "Le numéro " + numero.numero + " a été différé");
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Mettre à jour Différer un numéro
     */
    async doUpdateDiffererNumero(numero) {
      var formData = new FormData();
      formData.append("numero_diff_id", numero.numero_diff_id);
      formData.append("numero_id", numero.numero_id);
      formData.append("date_entree", numero.numero_diff_entree);
      formData.append("date_sortie", moment(getCurrentDate(), process.env.VUE_APP_DATEFORMAT_CLIENT).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http
        .put(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.searchAffaireNumeros();
            this.$root.$emit("ShowMessage", "La mention 'différé' du numéro " + numero.numero + " a été correctement supprimée");
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    // /**
    //  * Get immeubles associes
    //  */
    // async getImmeublesAssocies() {
    //   return new Promise((resolve, reject) => {
    //     // Récupère la liste des id des numéros référencés
    //     var numeros_base_id_list = this.affaire_numeros_anciens.map(x => x.numero_id);
  
    //     var formData = new FormData();
    //     formData.append("numeros_base_id_list", JSON.stringify(numeros_base_id_list));
  
    //     this.$http.post(
    //       process.env.VUE_APP_API_URL +
    //       process.env.VUE_APP_NUMEROS_RELATIONS_BY_NUMEROSBASEID_ENDPOINT,
    //       formData,
    //       {
    //         withCredentials: true,
    //         headers: {'Content-type': 'application/json'},
    //       }
    //     )
    //     .then(response => {if (response && response.data) resolve(response.data)})
    //     .catch(err => reject(err));
    //   });
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

    /**
     * Génère une quittance des numéros réservés dans l'affaire
     */
    async doQuittanceNumerosReserves() {
      let tmp = this.getCadastresNumerosNumerosBases(this.affaire_numeros_nouveaux);
      let cadastres = tmp[0];
      let numeros = tmp[1];
      let numeros_bases = tmp[2];

      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("template", "NumerosReserves");
      formData.append("relpath", process.env.VUE_APP_RELPATH_DESIGNATIONS_ENDPOINT);
      formData.append("filename", this.affaire.id + "_Res_biens-fonds");
      formData.append("values", JSON.stringify({
        "affaire_id": this.affaire.id,
        "date": moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        "cadastre": cadastres,
        "numero": numeros,
        "numero_base": numeros_bases
      }));

      saveDocument(formData).then(response => {
        this.$root.$emit("ShowMessage", "Le fichier '" + response.data.filename + "' se trouve dans le dossier '"+ response.data.folderpath +"' de l'affaire");
        this.$root.$emit("searchAffaireDocuments");
      }).catch(err => handleException(err, this));
    },

    /**
     * Return lists of cadastre, numero and numero_base for quittance numeros_reserves
     */
    getCadastresNumerosNumerosBases(numeros_reserves) {
      let cadastres = [];
      let numeros = [];
      let numeros_bases = [];

      numeros_reserves.forEach(x => {
        cadastres.push(x.numero_cadastre);
        numeros.push(x.numero_suffixe !== null? x.numero + " / " + x.numero_suffixe: x.numero);
        numeros_bases.push(x.numero_base);
      });

      cadastres = cadastres.join("\n");
      numeros = numeros.join("\n");
      numeros_bases = numeros_bases.join("\n");
      return [cadastres, numeros, numeros_bases];
    },

    /**
     * set permission to edit mat diff
     */
    setMatDiffEdition() {
      //Check if role secretaire
      this.editMatDiffAllowed = this.permission.editNumerosAllowed;
      let role_id = getCurrentUserRoleId();
      if(role_id && !isNaN(role_id) && [Number(process.env.VUE_APP_MO_ROLE_ID), Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)].includes(Number(role_id))) {
        this.editMatDiffAllowed = true;
      }
    },

    /**
     * Define if element is visible or not
     */
    showPermissions() {
      let role_id = getCurrentUserRoleId();

      let typeAffaire_modification_all = [
        this.typesAffaires_conf.modification,
        this.typesAffaires_conf.modification_visa,
        this.typesAffaires_conf.modification_duplicata,
        this.typesAffaires_conf.modification_abandon_partiel,
        this.typesAffaires_conf.modification_mutation,
        this.typesAffaires_conf.modification_ppe
      ];
      
      this.show = {
        numeros_reserves_card: typeAffaire_modification_all.concat([
          this.typesAffaires_conf.mutation, 
          this.typesAffaires_conf.ppe, 
          this.typesAffaires_conf.pcop
        ]).includes(this.affaire.type_id),
        
        numeros_references_card: [
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.mat_diff,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.servitude,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.modification_abandon_partiel
        ].includes(this.affaire.type_id),

        numeros_reserves_immeuble_base: [
          this.typesAffaires_conf.pcop,
          this.typesAffaires_conf.modification_pcop,
          this.typesAffaires_conf.modification_ppe,
          this.typesAffaires_conf.ppe
        ].includes(this.affaire.type_id),

        reservation_numeros_mo: [
          this.typesAffaires_conf.mutation, 
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.modification,
          this.typesAffaires_conf.modification_mutation,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.art35,
          this.typesAffaires_conf.retablissement_pfp3
        ].includes(this.affaire.type_id),

        balance: [
          this.typesAffaires_conf.mutation,
          this.typesAffaires_conf.modification_mutation,
          this.typesAffaires_conf.modification_visa,
          this.typesAffaires_conf.modification_duplicata
        ].includes(this.affaire.type_id),

        deleteReferencedNumberColumn: [
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.mat_diff,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.servitude,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.modification_abandon_partiel
        ].includes(this.affaire.type_id)
          && role_id && !isNaN(role_id) && Number(process.env.VUE_APP_ADMIN_ROLE_ID) === Number(role_id),
      }
    },

    /**
     * Retourne les numéros en vigueur et en projet dans le cadastre sélectionné
     */
    async getNumerosBase() {
      let types = process.env.VUE_APP_NUMERO_TYPE_BF + "," + process.env.VUE_APP_NUMERO_TYPE_DDP;
      return new Promise ((resolve) => {
        if (this.affaire.type_id === this.typesAffaires_conf.pcop) {
          types += ',' + process.env.VUE_APP_NUMERO_TYPE_PPE;
        }

        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT +
          "?cadastre_id=" + this.affaire.cadastre_id +
          "&type_id=" + types +
          "&etat_id=" + process.env.VUE_APP_NUMERO_PROJET_ID + "," +  process.env.VUE_APP_NUMERO_VIGUEUR_ID,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.numerosBaseListe = stringifyAutocomplete(response.data, "numero_sitn");
            resolve(response);
          }
        }).catch(err => handleException(err, this));
      })
    },


    /**
     * Fonction appelée lorsque des numéros sont référencés à l'affaire 
     */
    async saveReferenceNumeros(numeros) {
      let numeros_ = numeros.map(x => ({
        numero_id: x.id,
        etat_id: x.etat_id
      }));

      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("numeros_liste", JSON.stringify(numeros_));

      return new Promise((resolve, reject) => {
        this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_REFERENCE_NUMEROS_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: { Accept: "application/json" }
            }
          )
          .then(response => {
            this.$root.$emit("searchAffaireNumeros");
            this.$root.$emit("ShowMessage", "Le(s) numéro(s) sélectionné(s) ont été correctement ajouté(s) à l'affaire");
            this.$root.$emit("updateNumerosFactureList");
            this.$root.$emit("searchAffaireFactures");
            resolve(response);
          }).catch(err => reject(err));
      });
    },

  /**
   * Remove link referenced Number
   */
  onRemoveNumeroReference(item) {
    // Control if numeros relations are based on current item
    let testBaseNumber = this.affaire_numeros_nouveaux.some(x => x.numero_base_id === item.numero_id);

    if (testBaseNumber) {
      this.$root.$emit("ShowAlert", {
        title: "Action impossible",
        content: "Le numéro " + item.numero + " du cadastre de " + item.numero_cadastre + " est utilisé comme bien-fonds de base pour des numéros dans cette affaire."
      });
    } else {
      
      let content = "Confirmer la suppression du lien entre le numéro "  + item.numero + " du cadastre de " + item.numero_cadastre + " et l'affaire " + this.affaire.id + "."
      if (this.affaire.type_id === this.typesAffaires_conf.cadastration) {
        content += " Les factures liées à ce numéro seront également supprimée automatiquement."
      }
      
      this.$root.$emit("ShowConfirmation", {
        title: "Demande de confirmation",
        content: content,
        onConfirm: () => { this.deleteNumeroAffaire(item) }
      })

    }
  },


  /**
   * Supprimer lien numéro_affaire
   */
  async deleteNumeroAffaire(item) {
    this.$http.delete(
      process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT
        + "?affaire_id=" + item.affaire_id + "&numero_id=" + item.numero_id,
      {
        withCredentials: true,
        headers: { Accept: "application/json" }
      }
    ).then(response => {
      if (response && response.data) {
        this.searchAffaireNumeros();
        this.$root.$emit("ShowMessage", "Le numéro " + item.numero + " du cadastre de " + item.numero_cadastre + " a bien été délié de l'affaire");
        this.$root.$emit("searchAffaireFactures");
      }
    }).catch(err => handleException(err, this));
  }


  },
  mounted: function() {
    this.searchAffaireNumeros();
    this.getNumerosBase();

    this.showPermissions();
    this.setMatDiffEdition();

    this.$root.$on('searchAffaireNumeros', () => this.searchAffaireNumeros());
    this.$root.$on("getNumerosBase", () => this.getNumerosBase());

  }
};
</script>



