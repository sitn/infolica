<style src="./mapHandler.css" scoped></style>
<template src="./mapHandler.html"></template>



<script>
import { checkLogged } from "@/services/helper";
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
//import {defaults as defaultControls, ScaleLine} from 'ol/control';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature'
// import Circle from 'ol/geom/Circle'
import Point from 'ol/geom/Point';
//import {transform} from 'ol/proj';

export default {
  name: "MapHandler",
  props: {
    msg: String
  },
  data: () => ({
    affaire_data: {},
    map: null,
    vectorLayer: null,
    vectorSource: null
  }),

  methods: {

    /**
     * Init map
     */
    initMap: function(center) {

      //WMS
      var wmsSource = new TileWMS({
        url: process.env.VUE_APP_WMS_URL,
        params: {
          'LAYERS': 'plan_cadastral_couleur',
          'TILED': false
        }
      });

      var wmsLayer = new TileLayer({
        source: wmsSource
      });


      // Vector layer
      this.vectorSource = new VectorSource({
        projection: process.env.VUE_APP_MAP_PROJECTION,
      })
      this.vectorLayer = new VectorLayer({
        source: this.vectorSource,
        isFixed : true
      });

      // Map layers
      var layers = [wmsLayer, this.vectorLayer];

      if(!this.map){
        this.map = new Map({
          layers: layers,
          target: 'mapDiv',
          view: new View({
            projection: process.env.VUE_APP_MAP_PROJECTION,
            center: center ? [center.x, center.y] : process.env.VUE_APP_MAP_DEFAULT_CENTER,
            zoom: process.env.VUE_APP_MAP_DEFAULT_ZOOM
          })
        });

        // Add click listener
        this.map.on('click', this.onMapClick);
      }
      else{
        this.map.getView().setCenter(center ? [center.x, center.y] : process.env.VUE_APP_MAP_DEFAULT_CENTER)
      }

      // Add marker
      this.addMarker(center.x, center.y);
    },


    /**
     * Handle map click event
     */
    onMapClick: function(evt) {
      console.log(evt);
      //var viewResolution = this.$refs.view.getResolution();
      /*var url = this.$refs.wmsSource.getFeatureInfoUrl(
        evt.coordinate,
        null, //viewResolution,
        "EPSG:2056",
        { INFO_FORMAT: "text/html" }
      );
      console.log(url);*/
    },

    /**
     * Handle map mounted event
     */
    /*onMapMounted: function() {
      console.log(this.$refs.map);
    },*/

    /**
     * Add marker
     */
    addMarker: function(x, y) {
      var marker = new Feature({
        geometry: new Point([x, y]) //, 2)
      });

      this.vectorSource.addFeature(marker);
    },

    /**
     * Récupère les coordonnées de l'affaire
     */
    async searchAffaire() {
      return new Promise((resolve, reject) => {
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_AFFAIRE_BY_ID_ENDPOINT +
            this.$route.params.id
        ).then(response => {
          if (response.data) {
            resolve({x: response.data.localisation_e, y: response.data.localisation_n});
          }
        })
        .catch(() => reject)
      });
    }
  },

  mounted: function() {
    checkLogged();
    let _this = this;
    this.searchAffaire().then(function(center){
      _this.initMap(center);
    });
    
  }
};
</script>

