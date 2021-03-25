<style src="./balanceFromFile.css" scoped></style>
<template src="./balanceFromFile.html"></template>

<script>
import { handleException } from "@/services/exceptionsHandler";
import { getTypesNumeros, getCadastres, stringifyAutocomplete } from "@/services/helper";
import ReferenceNumeros from "@/components/Affaires/NumerosAffaire/ReferenceNumeros/ReferenceNumeros.vue";

// import moment from 'moment'

export default {
  name: "balanceFromFile",
  components: {
    ReferenceNumeros
  },
  props: {
    affaire: { type: Object },
    numeros_nouveaux: { type: Array },
    numeros_anciens: { type: Array }
  },
  data: () => {
    return {
      // numeros_liste = [],
      balanceContainsDP: false,
      cadastres_liste: [],
      checkBFBalance: {
        show: false,
        title: "",
        content: ""
      },
      editionBalance: false,
      etapeSetBalance: Number(process.env.VUE_APP_ETAPE_SET_BALANCE_ID),
      mutation_names: [],
      numero_DP_id: Number(process.env.VUE_APP_NUMERO_DP_ID),
      numeros_relations: [],
      numeros_relations_bk: [],
      numeros_relations_matrice: [],
      numeros_types_liste: [],
      selectedMutation: {
        nom: null,
        numeros: []
      },
      tableau_balance: [],
      showBalanceMenu: false,
      showAskDDPCreation: false,
    };
  },
  methods: {

    /**
     * Séparer les anciens numéros et les numéros projetés
     */
    initBFArrays() {
      this.numeros_anciens = this.numeros_anciens.filter(
        x =>
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF)
      );

      this.numeros_nouveaux = this.numeros_nouveaux.filter(
        x =>
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF) &&
          x.numero_etat_id !== Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
      );
    },


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
     * Get balance (numeros_relations)
     */
    async getNumerosRelations() {
      let oldBF;
      let newBF;

      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_NUMEROS_RELATIONS_BY_AFFAIREID_ENDPOINT +
            this.affaire.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response && response.data) {
            let numeros_relations = [];
            
            // Récupère toutes les relations de type mutation
            response.data.forEach(x => {
              if (x.numero_relation_type_id === Number(process.env.VUE_APP_RELATION_TYPE_MUTATION_ID)) {
                
                // Check DP in oldBF
                if (x.numero_base_id === Number(process.env.VUE_APP_NUMERO_DP_ID)){
                  oldBF = "DP";
                } else {
                  oldBF = [x.numero_base_cadastre_id, x.numero_base].join("_");
                }

                // Check DP in newBF
                if (x.numero_associe_id === Number(process.env.VUE_APP_NUMERO_DP_ID)){
                  newBF = "DP";
                } else {
                  newBF = [x.numero_associe_cadastre_id, x.numero_associe].join("_");
                }

                numeros_relations.push([ oldBF , newBF ]);
              }
            });

            // Construct balance
            this.tableau_balance = this.constructTableauBalance(numeros_relations);
          }
        })
        .catch(() => this.editionBalance = true);
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
      ).then(() => this.getMutationNames() )
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
     * Get balance from mutation name (DES)
     */
    async getBalanceFromDes() {
      this.showBalanceMenu = false;
      
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_BALANCE_FROM_FILE_ENDPOINT + "?affaire_id=" + this.affaire.id,
        {
          withCredentials: true,
          headers: {Accept: "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = JSON.parse(response.data);
          let relation = [];

          tmp.forEach(x => {
            // prepare relation array
            x.relation_old = [this.affaire.cadastre_id, x.old].join("_");
            if (String(x.old).toLowerCase().includes("dp")) {
              x.relation_old = "DP";
            }
            
            x.relation_new = [this.affaire.cadastre_id, x.new].join("_");
            if (String(x.new).toLowerCase().includes("dp")) {
              x.relation_new = "DP";
            }
            // keep relation
            relation.push([x.relation_old, x.relation_new]);
          });

          this.tableau_balance = this.constructTableauBalance(relation);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Generate "balance" in case of immatriculation 
     * Reservation de numéros must be done previously
     */
    getBalanceImmatriculationBF() {
      this.showBalanceMenu = false;

      if (this.numeros_nouveaux.length === 0) {
        this.$root.$emit("ShowError", "Aucun numéro de BF n'a été réservé dans l'affaire");
        return;
      }

      let relation = [];
      this.numeros_nouveaux.forEach(x => relation.push(["DP", [x.numero_cadastre_id, x.numero].join("_")]));
      this.tableau_balance = this.constructTableauBalance(relation);
    },
   
   /**
     * Référencer des numéros pour l'exmatriculation
     * This operation need to reference numbers
     */
    referencerNumeros() {
      // Referencer des numéros
      this.$refs.formReference.openReferenceDialog();
    },

   /**
     * Generate "balance" in case of exmatriculation 
     * This operation need to reference numbers first
     */
    getBalanceExmatriculationBF() {
      this.showBalanceMenu = false;

      // Pour chaque numéro référencé, le lier au DP
      if (this.numeros_anciens.length === 0) {
        this.$root.$emit("ShowError", "Aucun BF n'a été référencé à l'affaire!")
        return;
      }
      
      let relation = [];
      this.numeros_anciens.forEach(x => relation.push([[x.numero_cadastre_id, x.numero].join("_"), "DP"]));
      this.tableau_balance = this.constructTableauBalance(relation);

    },
    
    /**
     * Construct tableau balance
     */
    constructTableauBalance(relation) {
      /**
       * relation = [
       *  [oldBF, newBF]
       *  [oldBF, newBF]
       *  [  ⋮  ,   ⋮  ]
       *  [oldBF, newBF]
       * ]
       */
      let oldBF = [];
      let newBF = [];
      [oldBF, newBF] = this.transpose(relation);
      oldBF = [...new Set(oldBF)].sort();
      newBF = [...new Set(newBF)].sort();

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
    async saveBalance() {
      let relations = this.getRelations();
      let checkBF = await this.checkExistingBF(relations);

      // Raise error if more newBF than reserved numbers
      if (checkBF.newBF_not_in_numeros_reserves.length > 0) {
        this.checkBFBalance = {
          show: true,
          title: "Balance incorrecte !",
          content: "<p>Les numéros " + checkBF.newBF_not_in_numeros_reserves.join(", ") + " ne figurent pas dans les biens-fonds réservés.</p>\
                    <p>La balance n'est pas enregistrée.\n</p>"
        }
        return;
      } 
      
      await this.postBalance(checkBF);

      // Ask what to do with supplementary reserved numbers
      if (checkBF.ddp.length > 0){
        this.showAskDDPCreation = true;
      }


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
    async checkExistingBF(relations) {
      // get old and new BF lists
      let oldBF = [];
      let newBF = [];
      [oldBF, newBF] = this.transpose(relations);

      // get simplified list of reserved BF (cadastreId_BF)
      let reservedBF = [];
      let newBF_obj = [];
      this.numeros_nouveaux.forEach(x => {
        reservedBF.push([x.numero_cadastre_id, x.numero].join("_"));
        
        // Save newBF as number objects
        newBF_obj.push({
          id: x.numero_id,
          cadastre_id: x.numero_cadastre_id,
          type_id: x.numero_type_id,
          numero: x.numero,
          suffixe: x.numero_suffixe,
          etat_id: x.numero_etat_id,
          no_access: [x.numero_cadastre_id, x.numero].join("_")
        });
      });

      let newBF_not_in_numeros_reserves = [];
      let numeros_reserves_not_in_newBF = [];

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

          // remove newBF corresponding to this number
          newBF_obj.filter(y => y.no_access === x).pop();
        }
      });

      //Check if oldBF already exist in DB otherwise create it
      // Get unique set of oldBF
      oldBF = [...new Set(oldBF)];

      // Exclude dp from list to check existence
      let oldBF_lowercase = oldBF.map(x => x.toLowerCase());
      let dpIndex = oldBF_lowercase.indexOf("dp");
      if (dpIndex >= 0) {
        oldBF.splice(dpIndex);
      }

      if (oldBF.length > 0) {
        await this.checkExistingOldBF(oldBF)
        .then(response => {
          if (response && response.data) {
            oldBF = response.data;
          }
        }).catch(err => handleException(err, this));
      }

      if (dpIndex >= 0) {
        oldBF.push(Number(process.env.VUE_APP_NUMERO_DP_ID));
      }


      return {newBF_not_in_numeros_reserves: newBF_not_in_numeros_reserves,
              ddp: numeros_reserves_not_in_newBF,
              newBF: newBF_obj,
              oldBF: oldBF};
    },

    /**
     * Check existing old BF
     */
    async checkExistingOldBF(oldBF) {
      let formData = new FormData();
      formData.append("affaire_id", this.affaire.id);
      formData.append("oldBF", JSON.stringify(oldBF));
      
      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_BALANCE_CHECK_EXISTING_OLDBF_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {Accept: "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

    /**
     * Post Balance
     */
    async postBalance(checkBF) {
      let promises = [];
      let numero_id_base;
      let numero_id_associe;

      // Go through old BF
      this.tableau_balance.forEach(oldBF_i => {

        // Go through new BF
        for (let newBF_i in oldBF_i.newBF) {
          
          // append relation
          if (oldBF_i.newBF[newBF_i]) {
            // Old number + check DP
            if (oldBF_i.oldBF.toLowerCase().includes("dp")) {
              numero_id_base = process.env.VUE_APP_NUMERO_DP_ID;
            } else {
              numero_id_base = checkBF.oldBF.filter(x => [x.cadastre_id, x.numero].join("_") === oldBF_i.oldBF)[0].id;
            }
            
            // New number + check DP
            if (newBF_i.toLowerCase().includes("dp")) {
              numero_id_associe = process.env.VUE_APP_NUMERO_DP_ID;
            } else {
              numero_id_associe = checkBF.newBF.filter(x => [x.cadastre_id, x.numero].join("_") === newBF_i)[0].id;
            }

            promises.push( this.postNumerosRelation(numero_id_base, numero_id_associe) );
          }
        }
      });
      
      Promise.all(promises)
      .then(() => {
        this.editionBalance = false;
        this.$root.$emit("ShowMessage", "La balance a bien été enregistrée");
      }).catch(err => handleException(err, this));

    },

    /**
     * Post numero_relation
     */
    async postNumerosRelation(numero_id_base, numero_id_associe, relation_type_id=null) {
      return new Promise((resolve, reject) => {
        let formData = new FormData();
        formData.append("numero_id_base", numero_id_base);
        formData.append("numero_id_associe", numero_id_associe);
        formData.append("relation_type_id", relation_type_id? relation_type_id: Number(process.env.VUE_APP_RELATION_TYPE_MUTATION_ID));
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

  },
  mounted: function() {
    this.getNumerosRelations();
    this.initNumeroTypes();
    this.initCadastres();
    this.getMutationNames();
    setTimeout(() => { this.initBFArrays(); }, 1000);
    this.$root.$on("searchAffaireNumeros", () => { setTimeout(() => { this.initBFArrays(); }, 1000); });
  }
};
</script>
