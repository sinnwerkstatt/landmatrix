import Vue from "vue";
import Router from "vue-router";
import store from "store";
// const DataMap = () => import("./views/Data/GlobalMap");
import DataMap from "./views/Data/GlobalMap";
import DynamicsOverview from "views/Data/Charts/DynamicsOverview";
import ProduceInfoTreeMap from "./views/Data/Charts/ProduceInfoTreeMap";
import WebOfTransnationalDeals from "./views/Data/Charts/WebOfTransnationalDeals";
import DataList from "./views/Data/List";
import CaseStatistics from "views/Manager/CaseStatistics";
import DealCompare from "./views/Deal/Compare";
import DealDetail from "./views/Deal/Detail";
import DealEdit from "./views/Deal/Edit";
import InvestorDetail from "./views/Investor/Detail";
import Dashboard from "./views/Manager/Dashboard";
import NotFound from "./views/NotFound";
import Wagtail from "./views/Wagtail/WagtailSwitch";

Vue.use(Router);

const router = new Router({
  mode: "history",
  base: process.env.NEW_ROUTES === "False" ? "/newdeal/" : "/",
  routes: [
    {
      path: "/map/",
      name: "map",
      component: DataMap,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/charts/",
      name: "charts",
      redirect: { name: "web-of-transnational-deals" },
    },
    {
      path: "/charts/web-of-transnational-deals/",
      name: "web-of-transnational-deals",
      component: WebOfTransnationalDeals,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/charts/produce-info/",
      name: "produce-info",
      component: ProduceInfoTreeMap,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/charts/dynamics-overview/",
      name: "dynamics-overview",
      component: DynamicsOverview,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/data/",
      redirect: { name: "list_deals" },
    },
    {
      path: "/data/investors/",
      redirect: { name: "list_investors" },
    },
    {
      path: "/list/",
      redirect: { name: "list_deals" },
    },
    {
      path: "/list/deals/",
      name: "list_deals",
      component: DataList,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/list/investors/",
      name: "list_investors",
      component: DataList,
      meta: {
        hideBreadcrumbs: true,
      },
    },
    {
      path: "/deal/add/",
      name: "deal_add",
      component: DealEdit,
      props: true,
    },
    {
      path: "/deal/edit/:dealId/",
      name: "deal_edit",
      component: DealEdit,
      props: true,
    },
    {
      path: "/deal/:dealId/:dealVersion?/",
      name: "deal_detail",
      component: DealDetail,
      props: true,
    },
    {
      path: "/deal/:dealId/compare/:fromVersion/:toVersion/",
      name: "deal_compare",
      component: DealCompare,
      props: true,
    },
    {
      path: "/deal/",
      redirect: { name: "list_deals" },
    },
    {
      path: "/investor/:investorId/:investorVersion?/",
      name: "investor_detail",
      component: InvestorDetail,
      props: true,
    },
    {
      path: "/investor/",
      redirect: { name: "list_investors" },
    },
    {
      path: "/dashboard/",
      name: "dashboard",
      component: Dashboard,
    },
    {
      path: "/the-land-matrix-initiative",
      redirect: "/about/the-land-matrix-initiative",
    },
    { path: "/stay-informed", redirect: "/resources" },
    { path: "/partners-and-donors", redirect: "/about/partners-and-donors" },
    { path: "/privacy-policy", redirect: "/about/privacy-policy" },
    { path: "/disclaimer", redirect: "/about/disclaimer" },
    { path: "/impressum-legal-notice", redirect: "/about/impressum-legal-notice" },
    { path: "/get-involved", redirect: "/contribute" },
    { path: "/region/:region", redirect: "/observatory/:region" },
    { path: "/country/:country", redirect: "/observatory/:country" },
    { path: "/global", redirect: "/observatory/global" },
    {
      path: "/case_statistics/",
      name: "case_statistics",
      component: CaseStatistics,
    },
    {
      path: "*",
      name: "wagtail",
      component: Wagtail,
    },
    {
      path: "*",
      name: "404",
      component: NotFound,
      beforeEnter(to, from, next) {
        store.dispatch("setPageContext", {
          title: "Page not found",
          breadcrumbs: [],
        });
        next();
      },
    },
  ],

  //   // {
  //     // path: '/about',
  //     // name: 'about',
  //     // route level code-splitting
  //     // this generates a separate chunk (about.[hash].js) for this route
  //     // which is lazy-loaded when the route is visited.
  //     // component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
  //   // }
  // ]
});
const DEFAULT_TITLE = "Land Matrix";
router.afterEach((to) => {
  // Use next tick to handle router history correctly
  // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
  Vue.nextTick(() => {
    // document.title = to.meta.title || DEFAULT_TITLE;
    document.title = store.state.page.title || DEFAULT_TITLE;
    if (to.matched.some((record) => record.meta.hideBreadcrumbs)) {
      store.dispatch("breadcrumbBar", false);
    } else {
      store.dispatch("breadcrumbBar", true);
    }
  });
});

export default router;
