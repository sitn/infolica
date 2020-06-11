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
      this.numeros_relations_matrice = [];

      var tmp_nouveaux = {};
      this.numeros_nouveaux.forEach(x => {
        tmp_nouveaux[x.numero_cadastre_id + "." + x.numero] = false;
      });

      this.numeros_anciens.forEach(x => {
        this.numeros_relations_matrice.push({
          source_numero: x.numero_cadastre_id + "." + x.numero,
          source_numero_id: x.numero_id,
          destination: Object.assign({}, tmp_nouveaux)
        });
      });
    },

    /**
     * Update numeros_relations
     */
    updateNumerosRelations() {
      this.numeros_relations = [];

      var tmp = [];
      this.numeros_relations_matrice.forEach(num_ancien => {
        let keys_ = Object.keys(num_ancien.destination);
        keys_.forEach(key_ => {
          if (num_ancien.destination[key_] === true) {
            let destination_numero_id = this.getNumeroId(
              key_,
              this.numeros_nouveaux
            );
            tmp.push({
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
     * Recherche du numero_id à partir du numero_cadastre_id "." numero
     */
    getNumeroId(cadastre_numero, liste_numeros) {
      const [cadastre_id, numero_] = cadastre_numero.split(".");
      const result = liste_numeros.filter(
        x =>
          x.numero_cadastre_id === Number(cadastre_id) &&
          x.numero === Number(numero_)
      );
      return result[0].numero_id;
    },

    /**
     * Get balance (numeros_relations)
     */
    async getNumerosRelations() {
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
            this.tmp = response.data
              .filter(
                x =>
                  x.numero_relation_type_id ===
                  Number(process.env.VUE_APP_RELATION_TYPE_MUTATION_ID)
              )
              .map(x => ({
                source_numero_id: x.numero_base_id,
                source_numero: x.numero_base,
                destination_numero_id: x.numero_associe_id,
                destination_numero: x.numero_associe
              }));
          }
        })
        .catch(err => handleException(err, this));
    }
  },
  mounted: function() {
    this.getNumerosRelations();
  }
};
</script>
