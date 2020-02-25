<style src="./mapHandler.css" scoped></style>
<template src="./mapHandler.html"></template>


<script>
import {checkLogged} from '@/services/helper'

export default {
  name: 'MapHandler',
  props: {
    msg: String
  },
  data: () => ({
      map: null,
      zoom: 15,
      center: [6.93, 46.99],
      cr: 'EPSG:4326',
      // url: 'https://sitn.ne.ch/mapproxy95/service',
      // layers: 'plan_cadastral',
      url: 'https://sitn.ne.ch/ogc-sitn95-open/wms',
      layers: 'plan_cadastral_1860'
  }),

  methods:{

    /**
     * Handle map click event
     */
    onMapClick: function(evt){
      console.log(evt);
      //var viewResolution = this.$refs.view.getResolution();
      var url = this.$refs.wmsSource.getFeatureInfoUrl(
        evt.coordinate, null/*viewResolution*/, 'EPSG:3857',
        {'INFO_FORMAT': 'text/html'});
        console.log(url)
    },

    /**
     * Handle map mounted event
     */
    onMapMounted: function(){
      console.log(this.$refs.map)
    }
  },

  mounted: function(){
    checkLogged();
    
  }
}
</script>

