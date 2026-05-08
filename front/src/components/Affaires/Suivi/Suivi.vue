<style src="./suivi.css" scoped></style>
<style lang="css">.md-menu-content { z-index: 9000 !important; }</style>
<template src="./suivi.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";

import moment from "moment";

export default {
  name: "suivi",
  data: () => {
    return {
      affaire_suivi: [],
      affaire_suivi_bk: [],
      cb_showDetail: false
    };
  },


  methods: {
    /*
     * SEARCH AFFAIRE SUIVI
     */
    async searchAffaireSuivi() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_SUIVI_ENDPOINT +
            this.$route.params.id,
          {
            withCredentials: true,
            headers: { Accept: "application/json" }
          }
        )
        .then(response => {
          if (response.data) {
            let tmp = response.data;

            // set date format and sort by date
            let max_next_datetime_sort = 0;
            tmp.forEach(x => {
              x.next_datetime_sort = new Date(x.next_datetime).getTime();
              if (max_next_datetime_sort < x.next_datetime_sort) {
                max_next_datetime_sort = x.next_datetime_sort;
              }
              x.datetime = x.datetime? moment(new Date(x.datetime)).format(process.env.VUE_APP_DATEFORMAT_CLIENT): null;
              x.next_datetime = x.next_datetime? moment(new Date(x.next_datetime)).format(process.env.VUE_APP_DATEFORMAT_CLIENT): null;

              // custom realisation's period to show
              if (x.etape_priorite === 1) {
                if (x.datetime && x.next_datetime) {
                  x.realisation_period_txt = x.datetime + " - " + x.next_datetime;
                } else {
                  if (x.etape_id) {
                    if (x.etape_id === Number(process.env.VUE_APP_FIN_PROCESSUS_ID)) {
                      x.realisation_period_txt = x.datetime;
                    } else {
                      x.realisation_period_txt = x.datetime + " - ...";
                    }
                  }
                  else {
                    x.realisation_period_txt = x.next_datetime;
                  }
                }
              } else {
                // priority 2
                x.realisation_period_txt = x.datetime;
              }
              });

            let primaryKeys = [];
            tmp.forEach(x => {
              // fix duplicate primary key due to duplicate first step (see view in database)
              if (primaryKeys.includes(x.id)) {
                x.id = 0;
              }
              primaryKeys.push(x.id);

              // set sort by date value where it is null
              if (x.next_datetime_sort === 0) {
                x.next_datetime_sort = max_next_datetime_sort + 1;
              }
            });


            this.affaire_suivi_bk = tmp;
            this.updateAffaireSuiviShowList();
          }
        })
        .catch(err => handleException(err, this));
    },


    /**
     * Update list of suivi affaire list on set priority
     */
    updateAffaireSuiviShowList() {
      if (this.cb_showDetail) {
        this.affaire_suivi = this.affaire_suivi_bk;
      } else {
        this.affaire_suivi = this.affaire_suivi_bk.filter(x => x.etape_priorite === 1);
      }
    }
  },

  mounted: function() {
    this.searchAffaireSuivi();

    // Event listener
    this.$root.$on('getAffaireSuivi', () => this.searchAffaireSuivi());
  }
};
</script>



