import Vue from "vue";
import Router from "vue-router";
import store from "/store";
import DataMap from "./views/Data/GlobalMap";
import DataList from "./views/Data/List";
import DealEdit from "./views/Deal/Edit";
import DealDetail from "./views/Deal/Detail";
// import Charts from "./views/Charts/Base";
// import WebOfTransnationalDeals from "./views/Charts/WebOfTransnationalDeals";
import WebOfTransnationalDeals from "./views/Data/Charts/WebOfTransnationalDeals";
// import ProduceInfoTreeMap from "./views/Charts/ProduceInfoTreeMap";
// import DynamicsOverview from "/views/Charts/DynamicsOverview";
import Wagtail from "./views/Wagtail/WagtailSwitch";
import NotFound from "./views/NotFound";
import Dashboard from "./views/Manager/Dashboard";
import InvestorDetail from "./views/Investor/Detail";
import CaseStatistics from "/views/Manager/CaseStatistics";

Vue.use(Router);

const router = new Router({
  mode: "history",
  base: "/newdeal/", //process.env.BASE_URL,
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
      path: "/data/",
      redirect: { name: "list_deals" },
    },
    {
      path: "/data/investors/",
      redirect: { name: "list_investors" },
    },
    // {
    //   path: "/charts/",
    //   component: Charts,
    //   children: [
    //     {
    //       path: "dynamics/",
    //       name: "dynamics-overview",
    //       component: DynamicsOverview,
    //     },
    //     {
    //       path: "produce-info/",
    //       name: "produce-info",
    //       component: ProduceInfoTreeMap,
    //     },
    //   ],
    // },
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
      path: "/deal/edit/:deal_id/",
      name: "deal_edit",
      component: DealEdit,
      props: true,
    },
    {
      path: "/deal/:deal_id/:deal_version?/",
      name: "deal_detail",
      component: DealDetail,
      props: true,
    },
    {
      path: "/investor/:investor_id/",
      name: "investor_detail",
      component: InvestorDetail,
      props: true,
    },
    {
      path: "/dashboard/",
      name: "dashboard",
      component: Dashboard,
    },
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
router.afterEach((to, from) => {
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
