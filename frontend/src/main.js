import Vue from "vue";
import VueResource from "vue-resource";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import BootstrapVue from "bootstrap-vue";

// import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import { LMap, LTileLayer, LMarker, LFeatureGroup, LPolygon, LGeoJson } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';

// require('@/styles/style.scss');

// Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.use(VueResource);


Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-polygon', LPolygon);
Vue.component('l-feature-group', LFeatureGroup);
Vue.component('l-geo-json', LGeoJson);


export default new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
