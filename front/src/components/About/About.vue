<style src="./about.css" scoped></style>
<template src="./about.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
const moment = require('moment');

export default {
  name: 'About',
  props: {
    msg: String
  },
  data: () => {
    return {
      expandNotes: false,
      notes: [],
      // notes_: {
      //   mdCount: null,
      //   mdPage: null,
      //   mdData: [],
      // },
      // rowsPerPage: 15,
    }
  },
  methods: {
    // updatePagination (page, pageSize, sort, sortOrder) {
    //   console.log('pagination has updated', page, pageSize, sort, sortOrder);
    //   if (!(page && pageSize && sort && sortOrder)) return false;
    //   this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT + 
    //     "?page=" + page +
    //     "&per_page=" + pageSize +
    //     ((sort && sort !== undefined)? ("&sort=" + sort): "") +
    //     ((sortOrder && sortOrder !== undefined)? ("&sort_order=" + sortOrder): ""),
    //     {
    //       withCredentials: true,
    //       headers: {"Accept": "application/json"}
    //     }
    //   ).then(({data: resp}) => {
    //     console.log("resp = ", resp)
    //     if (resp) {
    //       this.rowsPerPage = resp.per_page;
    //       this.notes_ = {
    //         mdCount: resp.total,
    //         mdPage: resp.page,
    //         mdTotalPages: resp.total_pages,
    //         mdData: resp.data
    //       };
    //       console.log("this.notes_ = ", this.notes_)
    //     }
    //   }).catch(err => handleException(err, this));
    // },


    /**
     * Get Notes
     */
    getNotesMAJ() {
      this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          let tmp = response.data;
          tmp.forEach( x => {
            x.date_client = moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            x.delai_client = moment(x.delai, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
          });
          this.notes = tmp;
        }
      }).catch(err => handleException(err, this));
    },
  },
  mounted: function(){
    this.getNotesMAJ();
    // this.updatePagination(1, 15, "id", "desc"); // pagination
  }
}
</script>

