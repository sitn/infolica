<style src="./mapHandler.css" scoped></style>
<template src="./mapHandler.html"></template>



<script>
import { checkLogged } from "@/services/helper";

export default {
  name: "MapHandler",
  props: {
    msg: String
  },
  data: () => ({
    affaire_data: {},
    map: null,
    dataProjection: "EPSG:2056", // vl-map
    zoom: 18,
    center: [], // vl-view
    affaire_coord: [0, 0], // vl-view
    center_str: "", // vl-view
    projection: "EPSG:2056", // vl-view
    // center: [6.93, 46.99], // vl-view
    // center: [2548125, 1204613], // vl-view
    // url: "https://sitn.ne.ch/mapproxy95/service/", // vl-source-wmts
    // layerName: "plan_cadastral", // vl-source-wmts
    // matrixSet: "EPSG2056", // vl-source-wmts
    // format: "image/png", // vl-source-wmts
    // styleName: "default",  // vl-source-wmts
    // cr: 'EPSG:2056', // vl-layer-tile
    // url: 'https://sitn.ne.ch/ogc-sitn95-open/wms', // vl-layer-tile
    // layers: 'plan_cadastral_1860', // vl-layer-tile
  }),

  methods: {
    /**
     * Handle map click event
     */
    onMapClick: function(evt) {
      console.log(evt);
      //var viewResolution = this.$refs.view.getResolution();
      var url = this.$refs.wmsSource.getFeatureInfoUrl(
        evt.coordinate,
        null /*viewResolution*/,
        "EPSG:2056",
        { INFO_FORMAT: "text/html" }
      );
      console.log(url);
    },

    /**
     * Handle map mounted event
     */
    onMapMounted: function() {
      console.log(this.$refs.map);
    },

    /**
     * Récupère les coordonnées de l'affaire
     */
    async searchAffaire() {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            this.center = [response.data.localisation_e, response.data.localisation_n];
            this.affaire_coord = [response.data.localisation_e, response.data.localisation_n];
            // alert(this.center)
          }
        }).catch(err => {
          alert("error : " + err.message);
        });
    },
  },

  mounted: function() {
    checkLogged();
    this.searchAffaire();
  }
};
</script>

