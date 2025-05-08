<style src="./operatorSelect.css" scoped></style>
<template src="./operatorSelect.html"></template>


<script>

import { handleException } from "@/services/exceptionsHandler";
import { getOperateurs, stringifyAutocomplete2, getCurrentUserRoleId } from '@/services/helper';


const moment = require('moment');

export default {

  name: "OperatorSelect",


  props: {
    operator_id: {
      type: Array,
      default: () => [],
    },
    role: {
      type: Object,
    }
  },

  emits: ['update:operator_id'],

  data() {
    return {
      operator_list: {},
    };
  },

  computed: {
    localOperatorId: {
      get() {
        return this.operator_id;
      },
      set(value) {
        this.$emit('update:operator_id', value);
      }
    }
  },

  methods: {
    /**
     * Get operateurs
     */
    async getOperateursList() {
      return new Promise((resolve, reject) => {
        getOperateurs()
          .then(response => {
            if (response && response.data) {
              let tmp = response.data;

              // set operateur by default if he is chef_equipe
              let currentUserID = JSON.parse(localStorage.getItem("infolica_user")).id;
              let currentUserRoleID = getCurrentUserRoleId();
              if (tmp.some(x => (x.id === currentUserID) && x.chef_equipe) && (currentUserRoleID && [this.role.mo, this.role.ppe, this.role.mo_ppe].includes(currentUserRoleID))) {
                this.localOperatorId = [Number(currentUserID)];
              }


              let chef_equipe = tmp.filter(x => x.chef_equipe === true)
              let operateurs_actifs = chef_equipe.filter(x => x.sortie === null || (moment(x.sortie, process.env.VUE_APP_DATEFORMAT_WS) - new Date()) > 0)
              let operateurs_inactifs = chef_equipe.filter(x => x.sortie !== null || (moment(x.sortie, process.env.VUE_APP_DATEFORMAT_WS) - new Date()) <= 0)

              this.operator_list = {
                operateurs_actifs: stringifyAutocomplete2(operateurs_actifs, "prenom_nom", null, "prenom_nom"),
                operateurs_inactifs: stringifyAutocomplete2(operateurs_inactifs, "prenom_nom", null, "prenom_nom"),
              }

              resolve(tmp);
            }
          }).catch(err => {
            handleException(err, this);
            reject(err);
          });
      });
    },

    updateSelection(mode) {
      if (mode === 'tout') {
        let tmp = [];
        Object.keys(this.operator_list).forEach(x => {
          this.operator_list[x].forEach(y => {
            tmp.push(y.id);
          });
        });
        this.localOperatorId = tmp;
      }
      if (mode === 'aucun') {
        this.localOperatorId = [];
      }
    }
  },

  mounted: function () {
    this.getOperateursList();
  }

};

</script>
