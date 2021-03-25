<style src="./mapHandler.css" scoped></style>
<template src="./mapHandler.html"></template>

<script>
import "ol/ol.css";
import {defaults as defaultInteractions, Snap, Modify} from 'ol/interaction';
import Map from "ol/Map";
import View from "ol/View";
//import {defaults as defaultControls, ScaleLine} from 'ol/control';
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";
import {WMTSCapabilities} from "ol/format";
import WMTS from "ol/source/WMTS";
import {optionsFromCapabilities} from "ol/source/WMTS";
import proj4 from "proj4";
import {register as proj_register} from "ol/proj/proj4";
import {Projection} from "ol/proj";
import { Style, Circle, Fill, Stroke, RegularShape, Text } from "ol/style";
import GeoJSON from 'ol/format/GeoJSON';

import { handleException } from "@/services/exceptionsHandler";
import { getFeatures } from '@/services/helper'

export default {
  name: "MapHandler",
  props: {
    msg: String,
  },
  data: () => ({
    affaire: {},
    affaire_data: {},
    map: null,
    center: { x: null, y: null },
    view: null,
    vectorLayer: null,
    vectorSource: null,
    graphicsLayer: null,
    graphicsLayerSource: null,
    markerStyle: null
  }),

  methods: {
    /**
     * Init map
     */
    initMap: function(center, zoom) {

      this._crs = process.env.VUE_APP_MAP_PROJECTION;
      proj4.defs(this._crs,
       '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333'
       + ' +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel '
       + '+towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs');
      const _extent = [2420000, 1030000, 2900000, 1360000];
      proj_register(proj4);

      //Init marker style
      this.initMarkerStyle();

      // Init GeoJSON reader
      this.geojsonFormat = new GeoJSON();

      // WMTS
      this.wmtsLayer = new TileLayer();

      // Vector layer
      this.vectorSource = new VectorSource();
      this.vectorLayer = new VectorLayer({
        source: this.vectorSource
      });

      // Second vector layer holding all current affaires
      const featureStyle = new Style({
        image: new Circle({
          radius: 6,
          fill: new Fill({
            color: 'rgba(255, 0, 255, 0.7)'
          }),
          stroke: new Stroke({
            color: [120, 120, 120],
            width: 1
          })
        }),
        text: new Text({
          font: '12px Calibri,sans-serif',
          overflow: true,
          offsetY: 14,
          fill: new Fill({
            color: '#000',
          }),
          stroke: new Stroke({
            color: '#fff',
            width: 3,
          })
        }),
      });

      const featureStyleFunction = function (feature) {
        featureStyle.getText().setText(feature.get("number"));
        return featureStyle;
      };

      this.featureSource = new VectorSource();
      const featureLayer = new VectorLayer({
        source: this.featureSource,
        style: featureStyleFunction
      });

      this.initWmtsSource();

      // Graphics layer
      this.initGraphicsLayer();

      // Map layers
      const layers = [this.wmtsLayer, this.vectorLayer, this.graphicsLayer, featureLayer];


      const _projection = new Projection({
        code: this._crs,
        extent: _extent,
      });

      this.view = new View({
        projection: _projection,
        center: center
          ? [center.x, center.y]
          : process.env.VUE_APP_MAP_DEFAULT_CENTER,
        zoom: zoom,
        minZoom: 0,
        maxZoom: 17
        });
      if (!this.map) {

        const interactions = new defaultInteractions({
          altShiftDragRotate: false,
          pinchRotate: false
        });
    
        this.map = new Map({
          layers: layers,
          target: document.getElementById("mapDiv"),
          view: this.view,
          interactions: interactions
        });
        let me = this;

        this.map.on('pointermove', function(e) {
          if (me.modify.getActive() === true) {
            if (e.dragging) {
              me.map.getTarget().style.cursor = 'grabbing';
            } else {
              let pixel = me.map.getEventPixel(e.originalEvent);
              let hit = me.map.hasFeatureAtPixel(pixel);
              me.map.getTarget().style.cursor = hit ? 'pointer' : '';
            }
          }
        });

        this.modify = new Modify({
          source: this.vectorSource
        });

        this.snap = new Snap({
          source: this.vectorSource
        });

      } else {
        this.map
          .getView()
          .setCenter(
            center
              ? [center.x, center.y]
              : process.env.VUE_APP_MAP_DEFAULT_CENTER
          );
      }    
      // Workaround to draw markers in the good position when zooming
      // inside the browser. VueJS applies transforms to canvas elements
      this.makeWorkaroundCanvasTransform();

    },

    /**
     * Make work around canvas transform
     */
    makeWorkaroundCanvasTransform: function() {
      let _this = this;
      this.vectorSource.once("addfeature", function() {
        _this.setCanvasTransform();
        _this.map.addInteraction(_this.modify);
        _this.map.addInteraction(_this.snap);
      });
      this.vectorLayer.once("postrender", function() {
        _this.setCanvasTransform();
      });
      window.onresize = function() {
        setTimeout(function() {
          _this.setCanvasTransform();
        }, 500);
      };
      this.view.on("change:resolution", function() {
        _this.setCanvasTransform();
      });
      this.map.on("moveend", function() {
        _this.setCanvasTransform();
      });
    },
    /**
     * Handle map click event
     */
    setCanvasTransform: function() {
      let canvasList = document.getElementById("mapDiv").querySelectorAll("canvas");
      if (canvasList && canvasList.length > 1) {
        canvasList.forEach(canvas => {
          if (Math.round(window.devicePixelRatio * 100) < 100) {
            const ctx = canvas.getContext('2d');
            ctx.resetTransform();
          } else {
            canvas.style.transform = "inherit";
          }
        });
      }
    },

    /**
     * Init marker style
     */
    initMarkerStyle: function() {
      this.markerStyle = new Style({
        image: new Circle({
          radius: 7,
          fill: new Fill({ color: "yellow" }),
          stroke: new Stroke({
            color: [0, 0, 0],
            width: 2
          })
        })
      });
    },

    /**
     * Init graphics layer
     */
    initGraphicsLayer: function(){
      this.graphicsLayerSource = new VectorSource();
      this.graphicsLayer = new VectorLayer({
        source: this.graphicsLayerSource,
        style: new Style({
          fill: new Fill({ color: '#b3ffff' }),
          stroke: new Stroke({ color: 'red', width: 8 }),
          image: new RegularShape({
            fill: new Fill({ color: 'yellow' }),
            stroke: new Stroke({ color: 'red', width: 4 }),
            points: 4,
            radius: 10,
            radius2: 0,
            angle: Math.PI / 4,
          }),
        }),
        opacity: 0.5
      });
    },

    initWmtsSource: function() {
      this.$http
          .get(
            process.env.VUE_APP_WMTS_GETCAPABILITIES_URL
          )
          .then(response => {
            const parser = new WMTSCapabilities();
            const result = parser.read(response.data);
            const WMTSoptions = optionsFromCapabilities(
              result,{
                layer: process.env.VUE_APP_WMTS_LAYER,
                matrixSet: this._crs
              }
            )
            const source = new WMTS(WMTSoptions);
            this.wmtsLayer.setSource(source);
         });

    },
    /**
     * Add graphic to graphics layer
     */
    addGraphic: function(feature){
      this.graphicsLayerSource.clear();

      const nGeom = feature.geometry.coordinates.length;

      // Geometry is not empty
      if (nGeom !== 0) {
        this.graphicsLayerSource.addFeatures(this.geojsonFormat.readFeatures(feature));

      // Geometry is empty
      } else if (feature.bbox.length > 1) {
        const point = new Point(feature.bbox[0], feature.bbox[1]);
        const pointFeature = new Feature(point);
        this.graphicsLayer.addFeatures(pointFeature);
      }

      // Zoom to feature
      if (feature.geometry.type === 'Point') {
        this.view.fit(feature.bbox);
        this.view.setZoom(12);
      } else {
        this.view.fit(feature.bbox, {padding: [50, 50, 50, 50]});
      }
    },

    /**
     * Add marker
     */
    addMarker: function(x, y, zoom) {
      this.vectorSource.clear();
      const marker = new Feature({
        geometry: new Point([x, y])
      });
      marker.setStyle(this.markerStyle);
      this.vectorSource.addFeature(marker);

      if(zoom){
        this.view.setCenter([x, y]);
        this.view.setZoom(process.env.VUE_APP_MAP_DEFAULT_AFFAIRE_ZOOM);
      }
    },

    /**
     * Clear markers
     */
    clearMarkers: function() {
      this.vectorSource.clear();
    },

    async addFeatures() {
      getFeatures()
      .then(response => {
        const features = this.geojsonFormat.readFeatures(response.data);
        this.featureSource.addFeatures(features);
      }).catch(err => handleException(err, this))
    }
  },

  mounted: function() {
    this.addFeatures();
    this.$root.$emit("mapHandlerReady");
  }
};
</script>
