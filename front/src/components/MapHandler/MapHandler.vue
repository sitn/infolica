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
import {Style, Circle, Fill, Stroke} from 'ol/style';

export default {
  name: "MapHandler",
  props: {
    msg: String
  },
  data: () => ({
    affaire_data: {},
    map: null,
    vectorLayer: null,
    vectorSource: null,
    markerStyle: null,
  }),

  methods: {

    /**
     * Init map
     */
    initMap: function(center, zoom) {

      let _this = this;

      //Init marker style
      this.initMarkerStyle();

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
        projection: process.env.VUE_APP_MAP_PROJECTION
      })
      this.vectorLayer = new VectorLayer({
        source: this.vectorSource
      });

      // Map layers
      var layers = [wmsLayer, this.vectorLayer];

      //View
      var view = new View({
        projection: process.env.VUE_APP_MAP_PROJECTION,
        center: center ? [center.x, center.y] : process.env.VUE_APP_MAP_DEFAULT_CENTER,
        zoom: zoom
      });

        if(!this.map){
        this.map = new Map({
          layers: layers,
          target: 'mapDiv',
          view: view
        });

        //Workaround to draw markers in the good position
        this.vectorLayer.once('postrender', function() {
          _this.setCanvasTransform();
        });
        window.onresize = function(){
          setTimeout( function() {_this.setCanvasTransform();}, 500);
        }
        view.on('change:resolution', function() {
          _this.setCanvasTransform();
        });

        // Add click listener
        //this.map.on('click', this.onMapClick);
      }
      else{
        this.map.getView().setCenter(center ? [center.x, center.y] : process.env.VUE_APP_MAP_DEFAULT_CENTER)
      }

      // Add marker
      //this.addMarker(center.x, center.y);
    },

    /**
     * Handle map click event
     */
    setCanvasTransform: function() {
        var canvas = document.getElementById("mapDiv").querySelectorAll("canvas"); 

        if(canvas && canvas.length > 1)
          canvas[1].style.transform = "inherit";  
    },

    /**
     * Init marker style
     */
    initMarkerStyle: function() {
      this.markerStyle = new Style({
        image: new Circle({
          radius: 7,
          fill: new Fill({color: 'yellow'}),
          stroke: new Stroke({
            color: [0,0,0], width: 2
          })
        })
      });
    },

    /**
     * Handle map click event
     */
    /*onMapClick: function(evt) {
      console.log(evt);
      //var viewResolution = this.$refs.view.getResolution();
      var url = this.$refs.wmsSource.getFeatureInfoUrl(
        evt.coordinate,
        null, //viewResolution,
        "EPSG:2056",
        { INFO_FORMAT: "text/html" }
      );
      console.log(url);
    },*/

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
        geometry: new Point([x, y])
      });
      marker.setStyle(this.markerStyle);
      this.vectorSource.addFeature(marker);
    },

    /**
     * Clear markers
     */
    clearMarkers: function() {
      this.vectorSource.clear();
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

    if(this.$route.params.id){
      this.searchAffaire().then(function(center){
        _this.initMap(center, process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM);
      });
    }
  }
};
</script>

