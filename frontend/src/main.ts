import Columns1on1 from "$components/Wagtail/Columns1on1.vue";
import Columns3 from "$components/Wagtail/Columns3.vue";
import FaqsBlock from "$components/Wagtail/FaqsBlock.vue";
import FullWidthContainer from "$components/Wagtail/FullWidthContainer.vue";
import Gallery from "$components/Wagtail/Gallery.vue";
import Heading from "$components/Wagtail/Heading.vue";
import Image from "$components/Wagtail/Image.vue";
import LatestDatabaseModifications from "$components/Wagtail/LatestDatabaseModifications.vue";
import LatestNews from "$components/Wagtail/LatestNews.vue";
import Paragraph from "$components/Wagtail/Paragraph.vue";
import RawHTML from "$components/Wagtail/RawHTML.vue";
import ResourcesTeasers from "$components/Wagtail/ResourcesTeasers.vue";
import SectionDivider from "$components/Wagtail/SectionDivider.vue";
import Slider from "$components/Wagtail/Slider.vue";
import Statistics from "$components/Wagtail/Statistics.vue";
// needs to be registered globally for streamfield loops
import Title from "$components/Wagtail/Title.vue";
import Twitter from "$components/Wagtail/Twitter.vue";
import { apolloClient } from "$utils/apolloclient";
import App from "./App.vue";
import en_messages from "./i18n_messages.en.json";
import es_messages from "./i18n_messages.es.json";
import fr_messages from "./i18n_messages.fr.json";
import ru_messages from "./i18n_messages.ru.json";
import router from "./router";
import "./scss/main.scss";
import store from "./store";
import "@fortawesome/fontawesome-free/css/all.css";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";
import "bootstrap";
import BootstrapVue from "bootstrap-vue";
import dayjs from "dayjs";
import Cookies from "js-cookie";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet/dist/leaflet.css";
import Vue from "vue";
import VueApollo from "vue-apollo";
import VueI18n from "vue-i18n";
// import * as Sentry from "@sentry/vue";
// import { Integrations } from "@sentry/tracing";
// @ts-ignore
import VueMatomo from "vue-matomo";
import VueMeta from "vue-meta";
import MultiSelect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";
// @ts-ignore
import ScrollLoader from "vue-scroll-loader";

Vue.use(BootstrapVue);
Vue.use(VueMeta);
Vue.use(VueI18n);
Vue.use(VueApollo);
Vue.use(ScrollLoader);
Vue.component("MultiSelect", MultiSelect);

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

// if (import.meta.env.PROD)
//   Sentry.init({
//     Vue,
//     dsn: import.meta.env.VITE_SENTRY_DSN,
//     integrations: [
//       new Integrations.BrowserTracing({
//         routingInstrumentation: Sentry.vueRouterInstrumentation(router),
//         tracingOrigins: ["dev.landmatrix.org", "landmatrix.org", /^\//],
//       }),
//     ],
//     // Set tracesSampleRate to 1.0 to capture 100%
//     // of transactions for performance monitoring.
//     // We recommend adjusting this value in production
//     tracesSampleRate: 1.0,
//   });

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
Vue.component("wagtail-resources_teasers", ResourcesTeasers);
Vue.component("wagtail-full_width_container", FullWidthContainer);
Vue.component("wagtail-faqs_block", FaqsBlock);
Vue.component("wagtail-twitter", Twitter);
Vue.component("wagtail-latest_news", LatestNews);
Vue.component("wagtail-latest_database_modifications", LatestDatabaseModifications);
Vue.component("wagtail-statistics", Statistics);

Vue.filter("dayjs", (value: Date, date_format: string) => {
  return dayjs(value).format(date_format);
});

const locale = Cookies.get("django_language") ?? "en";

export const i18n = new VueI18n({
  locale,
  fallbackLocale: "en",
  messages: { en: en_messages, es: es_messages, fr: fr_messages, ru: ru_messages },
  silentTranslationWarn: true,
});

const apolloProvider = new VueApollo({ defaultClient: apolloClient });
let vue_app;

// transfer filters cookie to localstorage and remove it afterwards.
const filters_cookie = Cookies.get("filters");
if (filters_cookie) {
  localStorage.filters = filters_cookie;
  Cookies.remove("filters");
}

const locale_promise = store.dispatch("setLocale", locale);
const basicdata_promise = store.dispatch("fetchBasicData", locale);
store.dispatch("fetchMessages");
Promise.all([locale_promise, basicdata_promise]).then(() => {
  vue_app = new Vue({ router, store, i18n, apolloProvider, render: (h) => h(App) });
  vue_app.$mount("#app");
});
export default vue_app;
