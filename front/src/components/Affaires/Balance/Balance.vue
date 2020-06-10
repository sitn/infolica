<style src="./balance.css" scoped></style>
<template src="./balance.html"></template>

<script>
export default {
  name: "Balance",
  props: {
    affaire_numeros_all: {type: Array}
  },
  data: () => {
    return {
      numeros_anciens: [],
      numeros_nouveaux: [],
      numeros_relations: [],
      numeros_relations_matrice: []
    };
  },
  methods: {
    /**
     * Séparer les anciens numéros et les numéros projetés
     */
    initBFArrays() {
      this.numeros_anciens = this.affaire_numeros_all
        .filter(
          x =>
            x.affaire_numero_type_id ===
              Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_ANCIEN_ID) &&
            x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF)
        );

      this.numeros_nouveaux = this.affaire_numeros_all
        .filter(
          x =>
            x.affaire_numero_type_id ===
              Number(process.env.VUE_APP_AFFAIRE_NUMERO_TYPE_NOUVEAU_ID) &&
            x.numero_type_id === Number(process.env.VUE_APP_NUMERO_TYPE_BF) &&
            x.numero_etat_id !== Number(process.env.VUE_APP_NUMERO_ABANDONNE_ID)
        );

    //   this.initRelationMatrix();
      this.initTableRelation();
    },

    /**
     * Initialiser la table des relations
     */
    initTableRelation() {
      this.numeros_relations_matrice = [];

      var tmp_nouveaux = {};
      this.numeros_nouveaux.forEach(x => {
        tmp_nouveaux[x.numero] = false;
        // tmp_nouveaux[String(x.numero)] = false;
      })

      this.numeros_anciens.forEach(x => {
        this.numeros_relations_matrice.push({
          numero_old: x.numero,
          numero_old_id: x.numero_id,
          new: Object.assign({}, tmp_nouveaux),
          
        })
      });

    },

    /**
     * Update numeros_relations
     */
    updateNumerosRelations() {
        this.numeros_relations = [];
        
        var tmp = [];
        this.numeros_relations_matrice.forEach(num_ancien => {
            let keys_ = Object.keys(num_ancien.new);
            keys_.forEach(key_ => {
                if (num_ancien.new[key_] === true) tmp.push({source: num_ancien.numero_old, destination: Number(key_)})
            })
        });
        this.numeros_relations = tmp;
    },

  },
  mounted: function() {
  }
};
</script>
