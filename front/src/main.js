import Vue from 'vue';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';
import App from './App.vue';

Vue.config.productionTip = false;

//Vue material
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.css';
import VueRouter from 'vue-router';
import axios from 'axios';
import VueAxios from 'vue-axios';
import routes from './routes';
import VueMoment from 'vue-moment';
import moment from 'moment-timezone';
import proj4 from 'proj4';
import {register} from 'ol/proj/proj4';
import {checkLogged} from '@/services/helper'
import Clipboard from 'v-clipboard'

proj4.defs('EPSG:2056',
'+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333'
+ ' +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel '
+ '+towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs');
register(proj4);

Vue.config.productionTip = false;

Vue.use(VueMaterial);
Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.use(Clipboard);

Vue.use(VueMoment, {
  moment,
});

Vue.material.locale.dateFormat = "dd.MM.yyyy";
Vue.material.locale.months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
Vue.material.locale.shortMonths = ['Jan', 'Fév', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'];
Vue.material.locale.shorterMonths = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
Vue.material.locale.days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
Vue.material.locale.shortDays = ['Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'];
Vue.material.locale.shorterDays = ['Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'];
Vue.material.locale.firstDayOfAWeek = 1;
Vue.material.locale.cancel = 'Annuler';
Vue.material.locale.confirm = 'Ok';

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format(process.env.VUE_APP_DATEFORMAT_CLIENT)
  }
});

const router = new VueRouter({
  mode: 'history',
  routes: routes
});

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !checkLogged()) {
    next({name: 'Login'});
  } else {
    if (to.name === 'Login') {
      localStorage.setItem('infolica_redirectPath', from.path);
      next();
    } else {
      next();
    }
  }      
});


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
