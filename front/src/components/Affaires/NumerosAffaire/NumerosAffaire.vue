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
      alertDialog: {
        show: false,
        title: "",
        content: ""
      },
      confirmDialog: {
        show: false,
        title: '',
        content: '',
        onConfirm: () => {}
      },
      editMatDiffAllowed: false,
      editMatDiffCtrlAllowed: false,
      numerosBaseListe: [],
      numerosLoading: false,
      numerosMoLoading: true,
      show: {
        balance: false,
        deleteReferencedNumberBtn: false,
        updateReferencedNumberBtn: false,
        numeros_references_card: false,
        numeros_reserves_card: false,
        numeros_reserves_immeuble_base: false,
        reservation_numeros_mo: false
      },
      showNumerosMO: true,
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
      },
      modificationNumeroBaseId: null,
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
            this.affaire.id,
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
              if ([Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID), Number(process.env.VUE_APP_NUMERO_SUPPRIME_ID)].includes(element.numero_etat_id)) {
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
      let numerosAssocies = this.affaire_numeros_nouveaux.filter(x => {
        return parseInt(x.numero_base_id) == parseInt(numero.numero_id);
      });
      // Créer un array avec les numéros pour l'affichage du message
      let numerosAssociesArray = [];
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
      let numero_ = {};
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
            let etat = "Abandonné";
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
      this.affaire_id = Number(this.affaire.id);
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
          // si numéro est en projet, on ne peut pas radier la mat diff !
          if (numero.numero_etat_id === this.etatNumeros_conf.projet) {
            this.alertDialog = {
              show: true,
              title: "Radiation impossible",
              content: "La mat diff ne peut pas être radiée sur un bien-fonds en projet !"
            };
          } else {
            this.confirmDialog = {
              title: "Matérialisation différée",
              content: "Le numéro " + numero.numero + " a été matérialisé et la mention 'mat diff' va être supprimée.",
              show: true,
              onConfirm: () => this.doUpdateDiffererNumero(numero, "date_sortie")
            };
          }
        } else {
          this.confirmDialog = {
            title: "Matérialisation différée",
            content: "La mention 'mat diff' du numéro " + numero.numero + " doit être supprimée. Aucune requisition ne sera produite.",
            show: true,
            onConfirm: () => this.doDeleteDiffererNumero(numero)
          };
        }
      } else if (etat === "controle") {
        if (this.affaire.date_envoi !== null) {
          this.confirmDialog = {
            title: "Matérialisation différée",
            content: "Le numéro " + numero.numero + " a été contrôlé.",
            show: true,
            onConfirm: () => this.doUpdateDiffererNumero(numero, "date_controle")
          };
        }
      }
    },

    /**
     * Créer Différer un numéro
     */
    async doCreateDiffererNumero(numero) {
      let formData = new FormData();
      formData.append("numero_id", numero.numero_id);
      formData.append("affaire_id", this.affaire.id)
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
    async doUpdateDiffererNumero(numero, date_type) {
      let formData = new FormData();
      formData.append("numero_diff_id", numero.numero_diff_id);
      formData.append(date_type, moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

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
            this.$root.$emit("ShowMessage", "Le numéro " + numero.numero + " a été mis à jour avec succès.");
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Supprimer la mat diff
     */
    async doDeleteDiffererNumero(numero) {
      this.$http.delete(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_DIFFERES_ENDPOINT + "?numero_id=" + numero.numero_id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.searchAffaireNumeros();
            this.$root.$emit("ShowMessage", "Le numéro " + numero.numero + " a été mis à jour avec succès.");
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
    //     let numeros_base_id_list = this.affaire_numeros_anciens.map(x => x.numero_id);

    //     let formData = new FormData();
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
      if (role_id && !isNaN(role_id) && [Number(process.env.VUE_APP_MO_ROLE_ID), Number(process.env.VUE_APP_MO_PPE_ROLE_ID), Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)].includes(Number(role_id))) {
        this.editMatDiffAllowed = true;
      }
      if (role_id && !isNaN(role_id) && [Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID), Number(process.env.VUE_APP_ADMIN_ROLE_ID)].includes(Number(role_id))) {
        this.editMatDiffCtrlAllowed = true;
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
        this.typesAffaires_conf.modification_ppe,
        this.typesAffaires_conf.modification_retour_etat_juridique,
      ];

      this.show = {
        numeros_reserves_card: typeAffaire_modification_all.concat([
          this.typesAffaires_conf.mutation,
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.pcop,
          this.typesAffaires_conf.remaniement_parcellaire
        ]).includes(this.affaire.type_id),

        numeros_references_card: [
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.pcop,
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.mat_diff,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.servitude,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.modification_ppe,
          this.typesAffaires_conf.modification_abandon_partiel,
          this.typesAffaires_conf.remaniement_parcellaire
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

        deleteReferencedNumberBtn: [
          this.typesAffaires_conf.cadastration,
          this.typesAffaires_conf.mat_diff,
          this.typesAffaires_conf.revision_abornement,
          this.typesAffaires_conf.autre,
          this.typesAffaires_conf.servitude,
          this.typesAffaires_conf.mpd,
          this.typesAffaires_conf.modification_abandon_partiel
        ].includes(this.affaire.type_id)
          && role_id && !isNaN(role_id),

        updateReferencedNumberBtn: [
          this.typesAffaires_conf.ppe,
          this.typesAffaires_conf.pcop
        ].includes(this.affaire.type_id)
          && (this.affaire.operateur_id === JSON.parse(localStorage.getItem("infolica_user")).id || role_id && !isNaN(role_id) && Number(process.env.VUE_APP_ADMIN_ROLE_ID) === Number(role_id)),
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
     * Fonction appelée lorsque des numéros référencés sont modifiés
     */
    async saveModifReferenceNumeros(data) {
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("numero_id_old", this.modificationNumeroBaseId);
      formData.append("numero_id_new", data.id);

      return new Promise((resolve, reject) => {
        this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_MODIFICATION_REFERENCE_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          this.$root.$emit("searchAffaireNumeros");
          this.$root.$emit("ShowMessage", "Les modifications ont été apportées correctement");
          this.$root.$emit("updateNumerosFactureList");
          this.$root.$emit("searchAffaireFactures");
          resolve(response);
          this.modificationNumeroBaseId = null;
        }).catch(err => {
          reject(err);
          this.modificationNumeroBaseId = null;
        });
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
        });

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
    },


    /**
     * Modifier numéro de base (PPE/PCOP)
     */
    onUpdateBaseNumber(data) {
      this.modificationNumeroBaseId = data.numero_id;
      /** Ouvrir la boîte de dialogue de référence de numéros **/
      this.$refs.formModifReference.openReferenceDialog();
    },

    checkFile(inputFile, file_extension, file_size=0) {
      if (inputFile && inputFile.name.endsWith(file_extension) && inputFile.size>file_size) {
        return true;
      }
      return false;
    },


    async saveNumerosFromExcel_remaniementParcellaire(data){
      let formData = new FormData();
      formData.append('affaire_id', this.affaire.id);
      formData.append('num_projet', JSON.stringify(data[1].data));
      formData.append('num_vigueur', JSON.stringify(data[0].data));

      this.numerosLoading = true;

      return new Promise((resolve, reject) => {
        this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_SAVE_BF_REMANIEMENT_PARCELLAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        ).then(response => {
          this.$root.$emit("ShowMessage", "Les biens-fonds ont été correctement enregistrés et liés à l'affaire.")
          this.$root.$emit("searchAffaireNumeros");
          this.numerosLoading = false;
          resolve(response);
        }).catch(err => {
          handleException(err, this);
          this.numerosLoading = false;
          reject(err);
        });
      });

    },


    async onConfirmLoadNumerosFromExcel_remaniementParcellaire(){
      let file = document.getElementById('inputFile').files[0];
      let test = this.checkFile(file, '.xlsx');
      let allowConfirm = true;

      if(test===false){
        return;
      }

      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("file", file);

      return new Promise((resolve, reject) => {
        this.$http.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_POST_FILE_REMANIEMENT_PARCELLAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          let content = "";

          response.data.forEach(x => {
            // source Infolica or Terris
            content += "<h3>" + x.source + "</h3>";
            content += "<table border='1'><thead><tr><th>Cadastre</th><th>Biens-fonds</th></tr></thead><tbody>";
              x.data.forEach(y => {
                // data cadastre, liste_numeros.
                content += "<tr>";
                content += "<td style='width: 100px;'>" + y.cadastre + "</td>";
                content += "<td style='width: 1000px;'>"

                let sep = '';
                y.liste_numeros.forEach(z => {
                  // parcourir liste_numeros
                  content += sep + "<span style='color: " + z.font_color + ";'>" + z.numero + "</span>";
                  sep = ', ';
                  if (allowConfirm && z.error) {
                    allowConfirm = false;
                  }
                });
                content += "</td>";
                content += "<tr>";
              });
            content += "</tbody></table>";

          });
          content += "<p style='font-style: italic;'>Les numéros de biens-fonds en <span style='color: green;'>vert</span> sont ceux qui ont déjà été réservés dans l'affaire, ceux en <span style='color: blue;'>bleu</span> ont été réservés dans une autre affaire et ceux en <span style='color: red;'>rouge</span> seront créés en cliquant sur 'confimer'.</p>";

          if (allowConfirm) {
            this.confirmDialog= {
              show: true,
              title: 'Biens-fonds chargés',
              content: content,
              onConfirm: () => { this.saveNumerosFromExcel_remaniementParcellaire(response.data) }
            };
          } else {
            content += "<p style='font-weight: bold; color: blue;'>Les numéros réservés dans une autre affaire ou les DDP doivent être manuellement supprimés dans le fichier Excel afin de valider le processus.</p>";

            this.alertDialog= {
              show: true,
              title: 'Biens-fonds chargés',
              content: content,
            };
          }

          resolve(response)
        }).catch(err => {
          handleException(err, this);
          reject(err);
        });
      });

    },

    /**
     * on loadNumerosFromExcel_remaniementParcellaire
     */
    async loadNumerosFromExcel_remaniementParcellaire() {
      this.confirmDialog= {
        show: true,
        title: 'Importer les biens-fonds depuis un fichier EXCEL',
        content: "Le fichier excel doit être enregistré au format .xlsx et avoir la même structure que le fichier de comparaison Terris/Infolica.<br>\
                  Contacter l'administrateur en cas de question.<br><br>\
                  <input id='inputFile' type='file' accept='.xlsx' />",
        onConfirm: () => { this.onConfirmLoadNumerosFromExcel_remaniementParcellaire() }
      };

    },

    // confirm delete reserved number
    confirmDeleteReservedNumber(item) {
      this.confirmDialog = {
        show: true,
        title: "Confirmer la suppression d'un numéro de bien-fonds",
        content: `En cliquant sur "confirmer", le bien-fonds ${item.numero} (cadastre: ${item.numero_cadastre}) sera retiré de la balance (si déjà saisie) et délié de l'affaire. <br> S'il n'est lié à aucune autre affaire, il sera définitivement supprimé.`,
        onConfirm: () => this.deleteReservedNumber(item),
      }
    },

    // delete reserved number
    async deleteReservedNumber(item) {
      this.numerosLoading = true;
      this.$http.delete(process.env.VUE_APP_API_URL + process.env.VUE_APP_DELETE_NUMERO_ENDPOINT + item.numero_id + "?affaire_id=" + this.affaire.id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then((response) => {
        if (response && response.data) {
          this.alertDialog = {
            show: true,
            title: "Numéro correctement délié de l'affaire",
            content: response.data.message,
          }
          this.$root.$emit("ShowMessage", "Modification enregistrée avec succès.");
          this.$root.$emit("searchAffaireNumeros");
          this.$root.$emit("getNumerosRelations");
        }
      }).catch(err => {
        handleException(err, this);
      }).finally(() => {
        this.numerosLoading = false;
      });
    },


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



