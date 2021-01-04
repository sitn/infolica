<style src="./balance.css" scoped></style>
<template src="./balance.html"></template>

<script>
import { handleException } from "@/services/exceptionsHandler";
import { getTypesNumeros, getCadastres, stringifyAutocomplete } from "@/services/helper";
import moment from 'moment'

export default {
  name: "Balance",
  props: {
    affaire: { type: Object },
    affaire_numeros_all: { type: Array }
  },
  data: () => {
    return {
      // numeros_liste = [],
      cadastres_liste: [],
      checkBFBalance: {
        show: false,
        title: "",
        content: ""
      },
      mutation_names: [],
      numeros_anciens: [],
      numeros_nouveaux: [],
      numeros_relations: [],
      numeros_relations_bk: [],
      numeros_relations_matrice: [],
      numeros_types_liste: [],
      oldBF_toCreate: [],
      selectedMutation: {
        nom: null,
        numeros: []
      },
      showConfirmationCreateNumber: false,
      tableau_balance: []
    };
  },
  methods: {
    /**
     * Séparer les anciens numéros et les numéros projetés
     */
    initBFArrays() {
      this.numeros_anciens = this.affaire_numeros_all.filter(
        x =>
          x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID) &&
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF)
      );

      this.numeros_nouveaux = this.affaire_numeros_all.filter(
        x =>
          x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID) &&
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF) &&
          x.numero_etat_id !== Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
      );

      this.initTableRelation();
    },

// =============================================================

    /**
     * Init list of number types
     */
    async initNumeroTypes() {
      getTypesNumeros().then(response => {
        if (response && response.data) {
          this.numeros_types_liste = stringifyAutocomplete(response.data).filter(x => {
            return x.id === Number(process.env.VUE_APP_NUMERO_TYPE_BF) || x.id === Number(process.env.VUE_APP_NUMERO_TYPE_DDP)
          });
        }
      }).catch(err => handleException(err, this));
    },

    async initCadastres() {
      getCadastres().then(response => {
        if (response && response.data) {
          this.cadastres_liste = stringifyAutocomplete(response.data);
        }
      }).catch(err => handleException(err, this));
    },


    /**
     * Check existing old bf
     */
    async checkOldBF(numero, cadastre_id, type_id) {
      return new Promise((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT +
          "?numero=" + numero + "&cadastre_id=" + cadastre_id + "&type_id=" + type_id,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

    /**
     * Create old BF found in balance
     */
    async onCreateOldBF() {
      this.oldBF_toCreate.forEach(x => {
        this.postNumero(x)
        .then(() => this.showConfirmationCreateNumber = false)
        .catch(err => handleException(err, this));
      });
    },

    /**
     * Create numero
     */
    async postNumero(numero) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("numero", numero.numero);
        formData.append("cadastre_id", numero.cadastre.id);
        formData.append("type_id", numero.type.id);
        formData.append("etat_id", Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID));

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            const numero_id = Number(response.data)
            this.postNumeroAffaire(numero_id);
            this.postNumeroHistory(numero_id);
          }
          resolve(response);
        })
        .catch(err => reject(err));
      })
    },

    /**
     * Create link between affaire and numero
     */
    async postNumeroAffaire(numero_id) {
      return new Promise((resolve) => {
        let formData = new FormData();
        formData.append("affaire_id", this.affaire.id);
        formData.append("numero_id", numero_id);
        formData.append("type_id", Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID));
        formData.append("actif", true);

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_NUMEROS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => handleException(err, this));
      });
    },

    /**
     * Create history of new number
     */
    async postNumeroHistory(numero_id) {
      return new Promise((resolve) => {
        let formData = new FormData();
        formData.append("numero_id", numero_id);
        formData.append("numero_etat_id", Number(process.env.VUE_APP_NUMERO_VIGUEUR_ID));
        formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_NUMEROS_ETAT_HISTO_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept : "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => handleException(err, this));
      });
    },

    /**
     * Post numero_relation
     */
    async postNumerosRelations(numero_id_base, numero_id_associe) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("numero_id_base", numero_id_base);
        formData.append("numero_id_associe", numero_id_associe);
        formData.append("relation_type_id", Number(process.env.VUE_APP_RELATION_TYPE_MUTATION_ID));
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







    // =======================================================

    /**
     * Update variable numeros_relations
     */
    updateNumerosRelations() {
      this.numeros_relations = [];

      var tmp = [];
      this.numeros_relations_matrice.forEach(num_ancien => {
        let keys_ = Object.keys(num_ancien.destination); // keys_ = nouveaux numéros
        keys_.forEach(key_ => {
          if (num_ancien.destination[key_] === true) {
            let destination_numero_id = this.getNumeroId(
              key_, // nouveau numéro
              this.numeros_nouveaux // liste des nouveaux numéros
            );

            var relation_id = this.numeros_relations_bk.find(rel_bk => {
              return rel_bk.source_numero_id === num_ancien.source_numero_id && rel_bk.destination_numero_id === destination_numero_id
            })
            if (relation_id) {
              relation_id = relation_id.relation_id;
            } else {
              relation_id = null
            }

            tmp.push({
              relation_id: relation_id,
              source_numero: num_ancien.source_numero,
              source_numero_id: num_ancien.source_numero_id,
              destination_numero: key_,
              destination_numero_id: destination_numero_id
            });
          }
        });
      });
      this.numeros_relations = tmp;
    },

    /**
     * Recherche du numero_id à partir du numero
     */
    getNumeroId(numero_, liste_numeros) {
      const result = liste_numeros.filter(
        x =>
          x.numero === Number(numero_)
      );
      return result[0].numero_id;
    },

    /**
     * Get balance (numeros_relations)
     */
    async getNumerosRelations() {
      return new Promise((resolve, reject) => {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_RELATIONS_BY_AFFAIREID_ENDPOINT +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            let numeros_relations = response.data
              .filter(x =>
                x.numero_relation_type_id === Number(process.env.VUE_APP_RELATION_TYPE_MUTATION_ID)
              )
              .map(x => ({
                relation_id: x.numero_relation_id,
                source_numero_id: x.numero_base_id,
                source_numero: x.numero_base,
                destination_numero_id: x.numero_associe_id,
                destination_numero: x.numero_associe
              }));
            resolve(numeros_relations);
          }
        })
        .catch(err => reject(err));
      })
    },

    // /**
    //  * Save new balance
    //  */
    // saveBalance() {
    //   // Ajouter les relations qui ont été établies
    //   let relations_id = []; // enregistrer une liste des ID des relations existantes dans la BD
    //   let promises = [];
    //   this.numeros_relations.forEach(rel => {
    //     if (rel.relation_id) {
    //       relations_id.push(rel.relation_id);
    //     } else {
    //       // Si la relation est nouvelle (i.e. n'existe pas dans la BD)
    //       promises.push(this.postRelation(rel));
    //     }
    //   });

    //   // Supprimer les relations qui n'existent plus
    //   this.numeros_relations_bk.forEach(rel => {
    //     if (!relations_id.includes(rel.relation_id)) {
    //       promises.push(this.deleteRelation(rel));
    //     }
    //   })
    
    //   Promise.all(promises)
    //   .then(() => {
    //     this.$root.$emit("ShowMessage", "La balance a bien été mise à jour")
    //   })
    //   .catch(err => handleException(err, this));
    // },

    /**
     * Create relation in db
     */
    async postRelation(rel) {
      var formData = new FormData();
      formData.append("numero_id_base", rel.source_numero_id);
      formData.append("numero_id_associe", rel.destination_numero_id);
      formData.append("relation_type_id", process.env.VUE_APP_RELATION_TYPE_MUTATION_ID); 
      formData.append("affaire_id", this.$route.params.id);
      
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      })
    },


    /**
     * Delete relation in db
     */
    async deleteRelation(rel) {
      return new Promise((resolve, reject) => {
        this.$http.delete(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_NUMEROS_RELATIONS_ENDPOINT + "?numero_relation_id=" +  rel.relation_id,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * Refresh balance table
     */
    async refreshBalanceTable() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_BALANCE_GENERATE_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(() => {})
      .catch(err => handleException(err, this));
    },

    /**
     * Get mutation names from geos balance table
     */
    async getMutationNames() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_BALANCE_MUTATION_NAMES_ENDPOINT,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.mutation_names = JSON.parse(response.data);
          // this.mutation_names = response.data;
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Get balance from mutation name
     */
    async getBalanceByMutationName() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_BALANCE_ENDPOINT + "?mutation_name=" + this.selectedMutation.nom,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          let relation = [];

          tmp.forEach(x => {
            // prepare relation array
            x.relation_old = [x.cad_old, x.parcel_old].join("_");
            if (x.parcel_old.toLowerCase().includes("dp")) {
              x.relation_old = "DP";
            }
            
            x.relation_new = [x.cad_new, x.parcel_new].join("_");
            if (x.parcel_new.toLowerCase().includes("dp")) {
              x.relation_new = "DP";
            }
            // keep relation
            relation.push([x.relation_old, x.relation_new]);
          });

          this.tableau_balance = this.constructTableauBalance(relation)
        }
      }).catch(err => handleException(err, this));
    },
    
    /**
     * Construct tableau balance
     */
    constructTableauBalance(relation) {
      let oldBF = [];
      let newBF = [];
      [oldBF, newBF] = this.transpose(relation);
      oldBF = [...new Set(oldBF)].sort();
      newBF = [...new Set(newBF)].sort();

      // include DP
      if (!oldBF.includes("DP")) {
        oldBF.push("DP");
      }
      if (!newBF.includes("DP")) {
        newBF.push("DP");
      }
      
      // // include RP
      // if (!oldBF.includes("RP")) {
      //   oldBF.push("RP");
      // }
      // if (!newBF.includes("RP")) {
      //   newBF.push("RP");
      // }

      // Construct false balance object
      let tableau = [];
      oldBF.forEach(line => {
        let oldBF_line = {oldBF: line};
        let newBF_col = {};
        newBF.forEach(col => {
          newBF_col[col] =  relation.some(x => x.join(",") === [line, col].join(","));
        });
        oldBF_line["newBF"] = newBF_col;
        tableau.push(oldBF_line)
      });
      return tableau;
    },

    /** 
     * transpose matrix
     */
    transpose(m) {
      return m[0].map((x,i) => m.map(x => x[i]))
    },

    /**
     * Save balance
     */
    saveBalance() {
      let relations = this.getRelations();
      let checkBF = this.checkExistingBF(relations);
      if (checkBF.newBF_not_in_numeros_reserves.length > 0) {
        this.checkBFBalance = {
          show: true,
          title: "Balance incorrecte !",
          content: "<p>Les numéros " + checkBF.newBF_not_in_numeros_reserves.join(", ") + " ne figurent pas dans les biens-fonds réservés.</p>\
                    <p>La balance n'est pas enregistrée.\n</p>"
        }
        return;
      }
      // postBalance();

    },

    /**
     * Get relations from tableauBalance
     */
    getRelations() {
      let relations = [];

      // detect modifications from initial
      this.tableau_balance.forEach(tb => {
        for (let prop in tb["newBF"]) {
          if (tb["newBF"][prop]) {
            relations.push([tb["oldBF"], prop])
          }
        }
      });
      return relations;
    },

    /**
     * Check existing BF from relations
     */
    checkExistingBF(relations) {
      // get old and new BF lists
      // eslint-disable-next-line no-unused-vars
      let oldBF = []; // currently unused variable, update comment above
      let newBF = [];
      [oldBF, newBF] = this.transpose(relations);

      // get simplified list of reserved BF (cadastreId_BF)
      let reservedBF = [];
      this.affaire_numeros_all.forEach(x => {
        if (x.affaire_numero_type_id === Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID)) {
          reservedBF.push([x.numero_cadastre_id, x.numero].join("_"));
        }
      });

      let newBF_not_in_numeros_reserves = [];
      let numeros_reserves_not_in_newBF = [];
      // let old_not_existing_in_db = [];

      //Check if new BF are reserved in this affaire
      newBF.forEach(x => {
        if (x.toLowerCase() !== "dp") {
          if (!reservedBF.includes(x)) {
            newBF_not_in_numeros_reserves.push(x);
          }
        }
      });

      //Check if reserved BF are all in newBF (potential DDP)
      reservedBF.forEach(x => {
        if (!newBF.includes(x)) {
          numeros_reserves_not_in_newBF.push(x);
        }
      });

      //Check if oldBF already exist in DB
      // let promises = [];
      
      return {newBF_not_in_numeros_reserves: newBF_not_in_numeros_reserves,
              numeros_reserves_not_in_newBF: numeros_reserves_not_in_newBF};
    },


  },
  mounted: function() {
    this.getNumerosRelations();
    this.initNumeroTypes();
    this.initCadastres();
  }
};
</script>
