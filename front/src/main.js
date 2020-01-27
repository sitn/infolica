import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

//Vue material
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'
Vue.use(VueMaterial)

new Vue({
  render: h => h(App),
}).$mount('#app')
