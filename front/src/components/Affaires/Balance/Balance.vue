<style src="./balance.css" scoped></style>
<template src="./balance.html"></template>

<script>
import { handleException } from "@/services/exceptionsHandler";

export default {
  name: "Balance",
  props: {
    affaire_numeros_all: { type: Array }
  },
  data: () => {
    return {
      numeros_anciens: [],
      numeros_nouveaux: [],
      numeros_relations: [],
      numeros_relations_bk: [],
      numeros_relations_matrice: [],
      tmp: []
    };
  },
  methods: {
    /**
     * Séparer les anciens numéros et les numéros projetés
     */
    initBFArrays() {
      this.numeros_anciens = this.affaire_numeros_all.filter(
        x =>
          x.affaire_numero_type_id ===
            Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID) &&
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF)
      );

      this.numeros_nouveaux = this.affaire_numeros_all.filter(
        x =>
          x.affaire_numero_type_id ===
            Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID) &&
          x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF) &&
          x.numero_etat_id !== Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
      );

      this.initTableRelation();
    },

    /**
     * Initialiser la table des relations
     */
    initTableRelation() {
      // 1. retourne les relations
      this.getNumerosRelations()
      .then(response => {
        this.numeros_relations = response;
        this.numeros_relations_bk = response

      // 2. construire la matrice des relations
      this.numeros_relations_matrice = [];

      this.numeros_anciens.forEach(x => {
        var tmp_nouveaux = {};

        this.numeros_nouveaux.forEach(y => {
          var tmp = false;
          tmp = this.numeros_relations.some(rel => {
            if (rel.source_numero_id === x.numero_id && rel.destination_numero_id === y.numero_id) {
              return true
            } else {
              return false
            }
          })
          if (tmp) {
            tmp_nouveaux[y.numero] = true;
          } else {
            tmp_nouveaux[y.numero] = false;
          }
        });

        this.numeros_relations_matrice.push({
          source_numero: x.numero,
          source_numero_id: x.numero_id,
          destination: Object.assign({}, tmp_nouveaux)
        });
      });
    })
    .catch(err => handleException(err, this))
    },

    /**
     * Update variable numeros_relations
     */
    updateNumerosRelations() {
      this.numeros_relations = [];

      var tmp = [];
      this.numeros_relations_matrice.forEach(num_ancien => {
        let keys_ = Object.keys(num_ancien.destination);
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
            resolve(numeros_relations)
          }
        })
        .catch(err => reject(err));
      })
    },

    /**
     * Save new balance
     */
    saveBalance() {
      // Ajouter les relations qui ont été établies
      var relations_id = []; // enregistrer une liste des ID des relations existantes dans la BD
      var promises = [];
      this.numeros_relations.forEach(rel => {
        if (rel.relation_id) {
          relations_id.push(rel.relation_id)
        } else {
          // Si la relation est nouvelle (i.e. n'existe pas dans la BD)
          promises.push(this.postRelation(rel))
        }
      });

      // Supprimer les relations qui n'existent plus
      this.numeros_relations_bk.forEach(rel => {
        if (!relations_id.includes(rel.relation_id)) {
          promises.push(this.deleteRelation(rel));
        }
      })
    
      Promise.all(promises)
      .then(() => {
        this.$root.$emit("ShowMessage", "La balance a bien été mise à jour")
      })
      .catch(err => handleException(err, this));
    },

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
        .catch(err => reject(err))
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
        .catch(err => reject(err))
      })
    },


  },
  mounted: function() {
    this.getNumerosRelations();
  }
};
</script>
