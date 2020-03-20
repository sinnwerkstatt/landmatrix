import Vue from "vue";
import VueResource from "vue-resource";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vSelect from 'vue-select';

Vue.use(VueResource);

Vue.use(BootstrapVue);
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import "./scss/main.scss";

Vue.component('v-select', vSelect);
import 'vue-select/dist/vue-select.css';

import { LMap, LTileLayer, LGeoJson, LControlLayers } from 'vue2-leaflet';
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-control-layers', LControlLayers);
Vue.component('l-geo-json', LGeoJson);
import 'leaflet/dist/leaflet.css';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

export default new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
