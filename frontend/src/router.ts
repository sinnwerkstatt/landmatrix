import Vue from "vue";
import Router from "vue-router";
import store from "./store";

Vue.use(Router);

const DataList = () => import("$views/Data/List.vue");
const DealEdit = () => import("$views/Deal/Edit.vue");
const InvestorEdit = () => import("$views/Investor/Edit.vue");

const router = new Router({
  mode: "history",
  base: "/",
  routes: [
    // map
    {
      path: "/map/",
      name: "map",
      component: () => import("$views/Data/GlobalMap.vue"),
      meta: { hideBreadcrumbs: true },
    },
    // lists
    {
      path: "/list/deals/",
      name: "list_deals",
      component: DataList,
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/list/investors/",
      name: "list_investors",
      component: DataList,
      meta: { hideBreadcrumbs: true },
    },
    // charts
    {
      path: "/charts/",
      name: "charts",
      redirect: { name: "web-of-transnational-deals" },
    },
    {
      path: "/charts/web-of-transnational-deals/",
      name: "web-of-transnational-deals",
      component: () => import("$views/Data/Charts/WebOfTransnationalDeals.vue"),
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/charts/gmap/",
      name: "gmap",
      component: () => import("$views/Data/Charts/GlobalMapOfInvolvements.vue"),
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/charts/country_profiles/",
      name: "country_profiles",
      component: () => import("$views/Data/Charts/CountryProfile.vue"),
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/charts/produce-info/",
      name: "produce-info",
      component: () => import("$views/Data/Charts/ProduceInfoTreeMap.vue"),
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/charts/dynamics-overview/",
      name: "dynamics-overview",
      component: () => import("$views/Data/Charts/DynamicsOverview.vue"),
      meta: { hideBreadcrumbs: true },
    },
    // deal
    { path: "/deal/", redirect: { name: "list_deals" } },
    {
      path: "/deal/add/",
      name: "deal_add",
      component: DealEdit,
      props: true,
      meta: { requiresAuth: true, requiresEditPerms: true },
    },
    {
      path: "/deal/edit/:dealId/:dealVersion?/",
      name: "deal_edit",
      component: DealEdit,
      props: true,
      meta: { requiresAuth: true, requiresEditPerms: true, hideBreadcrumbs: true },
    },
    {
      path: "/deal/:dealId/:dealVersion?/",
      name: "deal_detail",
      component: () => import("$views/Deal/Detail.vue"),
      props: true,
      meta: { hideBreadcrumbs: true },
    },
    {
      path: "/deal/:dealId/compare/:fromVersion/:toVersion/",
      name: "deal_compare",
      component: () => import("$views/Deal/Compare.vue"),
      props: true,
      meta: { hideBreadcrumbs: true },
    },
    // investor
    { path: "/investor/", redirect: { name: "list_investors" } },
    {
      path: "/investor/add/",
      name: "investor_add",
      component: InvestorEdit,
      props: true,
      meta: { requiresAuth: true, requiresEditPerms: true },
    },
    {
      path: "/investor/edit/:investorId/:investorVersion?/",
      name: "investor_edit",
      component: InvestorEdit,
      props: true,
      meta: { requiresAuth: true, requiresEditPerms: true, hideBreadcrumbs: true },
    },
    {
      path: "/investor/:investorId/:investorVersion?/",
      name: "investor_detail",
      component: () => import("$views/Investor/Detail.vue"),
      props: true,
      meta: { hideBreadcrumbs: true },
    },
    // manager
    {
      path: "/management/",
      name: "manager",
      component: () => import("$views/Manager/Management.vue"),
      meta: { requiresAuth: true, hideBreadcrumbs: true },
    },
    {
      path: "/management/dashboard/",
      name: "dashboard",
      component: () => import("$views/Manager/Dashboard.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/management/case_statistics/",
      name: "case_statistics",
      component: () => import("$views/Manager/CaseStatistics.vue"),
      meta: { requiresAuth: true },
    },
    //
    {
      path: "/login/",
      name: "login",
      component: () => import("$views/Login.vue"),
    },

    // redirects
    { path: "/data/", redirect: { name: "list_deals" } },
    { path: "/data/investors/", redirect: { name: "list_investors" } },
    { path: "/list/", redirect: { name: "list_deals" } },
    { path: "/stay-informed/:rest?", redirect: "/resources/:rest?" },
    { path: "/partners-and-donors", redirect: "/about/partners-and-donors" },
    { path: "/privacy-policy", redirect: "/about/privacy-policy" },
    { path: "/disclaimer", redirect: "/about/disclaimer" },
    { path: "/impressum-legal-notice", redirect: "/about/impressum-legal-notice" },
    { path: "/get-involved", redirect: "/contribute" },
    { path: "/region/:region", redirect: "/observatory/:region" },
    { path: "/country/:country", redirect: "/observatory/:country" },
    { path: "/global", redirect: "/observatory/global" },

    {
      path: "/the-land-matrix-initiative",
      redirect: "/about/the-land-matrix-initiative",
    },

    // wagtail
    {
      path: "*",
      name: "wagtail",
      component: () => import("$views/Wagtail/WagtailSwitch.vue"),
    },
    {
      path: "*",
      name: "404",
      component: () => import("$views/NotFound.vue"),
      beforeEnter(to, from, next) {
        store.dispatch("setPageContext", { breadcrumbs: [] }).then(next);
      },
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresEditPerms)) {
    if (import.meta.env.VITE_ALLOW_EDITING?.toLowerCase() !== "true") next("/");
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.getters.userAuthenticated) {
      next({ name: "login", query: { next: to.fullPath } });
    } else next();
  } else next();
});

router.afterEach((to) => {
  Vue.nextTick(() => {
    store.dispatch(
      "breadcrumbBar",
      !to.matched.some((record) => record.meta.hideBreadcrumbs)
    );
  });
});

export default router;
