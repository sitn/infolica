import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

//Vue material
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import routes from './routes';
import VueMoment from 'vue-moment'
import moment from 'moment-timezone'
import { Map, TileLayer, WmtsSource, WmsSource, OsmSource  } from 'vuelayers'
import 'vuelayers/lib/style.css' // needs css-loader


Vue.config.productionTip = false;


Vue.use(VueMaterial)
Vue.use(VueRouter)
Vue.use(VueAxios, axios)

Vue.use(VueMoment, {
  moment,
})

//Vue layers components
Vue.use(Map, {
  dataProjection: 'EPSG:4326',
})
Vue.use(TileLayer)
Vue.use(WmtsSource)
Vue.use(WmsSource)
Vue.use(OsmSource)
const router = new VueRouter({
  mode: 'history',
  routes: routes
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
