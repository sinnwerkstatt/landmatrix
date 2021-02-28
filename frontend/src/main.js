import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Multiselect from "vue-multiselect";
import VCalendar from "v-calendar";
import dayjs from "dayjs";
import VueApollo from "vue-apollo";
import { apolloClient } from "apolloclient";
import ScrollLoader from "vue-scroll-loader";
import VueI18n from "vue-i18n";
import VueMatomo from "vue-matomo";

import en_messages from "./i18n_messages.en.json";
import es_messages from "./i18n_messages.es.json";
import fr_messages from "./i18n_messages.fr.json";

import "@fortawesome/fontawesome-free/css/all.css";
import "bootstrap";
import "vue-multiselect/dist/vue-multiselect.min.css";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

import "./scss/main.scss";

// needs to be registered globally for streamfield loops
import Title from "components/Wagtail/Title";
import Heading from "components/Wagtail/Heading";
import Image from "components/Wagtail/Image";
import Paragraph from "components/Wagtail/Paragraph";
import Columns1on1 from "components/Wagtail/Columns1on1";
import Columns3 from "components/Wagtail/Columns3";
import FullWidthContainer from "components/Wagtail/FullWidthContainer";
import Slider from "components/Wagtail/Slider";
import Gallery from "components/Wagtail/Gallery";
import FaqsBlock from "components/Wagtail/FaqsBlock";
import Twitter from "components/Wagtail/Twitter";
import LatestNews from "components/Wagtail/LatestNews";
import LatestDatabaseModifications from "components/Wagtail/LatestDatabaseModifications";
import Statistics from "components/Wagtail/Statistics";
import SectionDivider from "components/Wagtail/SectionDivider";
import RawHTML from "components/Wagtail/RawHTML";

Vue.use(BootstrapVue);
Vue.use(VCalendar);
Vue.use(VueI18n);
Vue.use(VueApollo);
Vue.use(ScrollLoader);

Vue.use(VueMatomo, {
  host: "https://stats.landmatrix.org",
  siteId: 1,
  trackerFileName: "matomo", // or piwik.php ?
  router: router,
  enableLinkTracking: true,
  trackInitialView: true,

  // Require consent before sending tracking information to matomo
  // Default: false
  requireConsent: false,
  // track without cookies? :)
  disableCookies: false,

  // Enable the heartbeat timer (https://developer.matomo.org/guides/tracking-javascript-guide#accurately-measure-the-time-spent-on-each-page)
  // Default: false
  enableHeartBeatTimer: false,
  heartBeatTimerInterval: 15,

  debug: false,

  // UserID passed to Matomo (see https://developer.matomo.org/guides/tracking-javascript-guide#user-id)
  // Default: undefined
  userId: undefined,

  // domains: '*.landmatrix.org',
});

Vue.component("Multiselect", Multiselect);

/* eslint-disable vue/component-definition-name-casing */
Vue.component("wagtail-title", Title);
Vue.component("wagtail-heading", Heading);
Vue.component("wagtail-image", Image);
Vue.component("wagtail-slider", Slider);
Vue.component("wagtail-gallery", Gallery);
Vue.component("wagtail-linked_image", Image);
Vue.component("wagtail-paragraph", Paragraph);
Vue.component("wagtail-columns_1_1", Columns1on1);
Vue.component("wagtail-columns_3", Columns3);
Vue.component("wagtail-section_divider", SectionDivider);
Vue.component("wagtail-html", RawHTML);
Vue.component("wagtail-full_width_container", FullWidthContainer);
Vue.component("wagtail-faqs_block", FaqsBlock);
Vue.component("wagtail-twitter", Twitter);
Vue.component("wagtail-latest_news", LatestNews);
Vue.component("wagtail-latest_database_modifications", LatestDatabaseModifications);
Vue.component("wagtail-statistics", Statistics);

Vue.filter("defaultdate", function (value) {
  return dayjs(value).format("YYYY-MM-DD HH:mm");
});

const i18n = new VueI18n({
  // eslint-disable-next-line no-undef
  locale: LANGUAGE || "en",
  fallbackLocale: "en",
  messages: { en: en_messages, es: es_messages, fr: fr_messages },
  silentTranslationWarn: true,
});

let vue_app = new Vue({
  router,
  store,
  i18n,
  apolloProvider: new VueApollo({
    defaultClient: apolloClient,
  }),
  render: (h) => h(App),
});

// eslint-disable-next-line no-undef
store.dispatch("fetchFields", LANGUAGE || "en");
store.dispatch("fetchMessages");
store.dispatch("fetchBasicData").then(() => {
  vue_app.$mount("#app");
});

export default vue_app;
