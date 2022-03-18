<style src="./about.css" scoped></style>
<template src="./about.html"></template>


<script>
// import { handleException } from "@/services/exceptionsHandler";
import Vuetable from 'vuetable-2/src/components/Vuetable'
import VuetablePagination from 'vuetable-2/src/components/VuetablePagination'
// import VuetablePaginationInfo from 'vuetable-2/src/components/VuetablePaginationInfo'
// const moment = require('moment');
import CssForBootstrap4 from "/src/assets/vuetable-css-bootstrap/VuetableCssBootstrap4.js"
// import CssForBootstrap4 from "datatables.net-bs4/js/dataTables.bootstrap4.js"

export default {
  name: 'About',
  components: {
    Vuetable,
    VuetablePagination,
    // VuetablePaginationInfo,
  },
  props: {
    msg: String
  },
  data: () => {
    return {
      expandNotes: false,

      api_url: process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT,

      notes: [],

      sortOrder: [
        {
          field: 'version',
          direction: 'desc'
        }
      ],

      fields: [
        {
          name: 'date',
          title: 'Date',
          sortField: 'date'
        },
        {
          name: 'version',
          title: 'Version',
          sortField: 'version'
        },
        {
          name: 'titre',
          title: 'Titre',
          sortField: 'titre'
        },
        {
          name: 'message',
          title: 'Message',
          sortField: 'message'
        },
      ],
      css: CssForBootstrap4,
    }
  },
  methods: {
    /**
     * Get Notes
     */
    async getNotesMAJ(_, httpOptions) {
      httpOptions['withCredentials'] = true;
      httpOptions['headers'] = {"Accept": "application/json"};

      return this.$http.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_NOTESMAJ_ENDPOINT,
        httpOptions
      );
    },


    // from https://www.vuetable.com/guide/pagination.html#binding-pagination-component-to-vuetable
    
    // when the pagination data is available, set it to pagination component
    onPaginationData (paginationData) {
      this.$refs.pagination.setPaginationData(paginationData);
    },
    // when the user click something that causes the page to change,
    // call "changePage" method in Vuetable, so that that page will be
    // requested from the API endpoint.
    onChangePage (page) {
      this.$refs.vuetable.changePage(page);
    }
  }
}
</script>

