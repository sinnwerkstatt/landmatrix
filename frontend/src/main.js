import Vue from "vue";
import VueResource from "vue-resource";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";


// import "bootstrap4/dist/css/bootstrap.css";
// import "bootstrap-vue/dist/bootstrap-vue.css";

import { LMap, LTileLayer, LGeoJson, LControlLayers } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// require('@/styles/style.scss');

Vue.use(VueResource);
Vue.use(BootstrapVue);

Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-control-layers', LControlLayers);
Vue.component('l-geo-json', LGeoJson);


export default new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
