import Vue from "vue";
import Router from "vue-router";
import GlobalMap from "./views/GlobalMap";
import DealList from "./views/DealList";
import DealEdit from "./views/DealEdit";
import DealDetail from "./views/DealDetail";
import Charts from "./views/Charts/Base";
import WebOfTransnationalDeals from "./views/Charts/WebOfTransnationalDeals";
import WagtailPage from "./views/WagtailPage";
import NotFound from "./views/NotFound";
import Dashboard from "./views/Dashboard";

import store from "./store";
import ItsABigDeal from "./views/Charts/ItsABigDeal";

Vue.use(Router);

const router = new Router({
  mode: "history",
  base: "/newdeal/", //process.env.BASE_URL,
  routes: [
    {
      path: "/data/",
      name: "deal_list",
      component: DealList,
    },
    {
      path: "/map/",
      name: "map",
      component: GlobalMap,
    },
    {
      path: "/dashboard/",
      name: "dashboard",
      component: Dashboard,
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
      path: "/deal/:deal_id/",
      name: "deal_detail",
      component: DealDetail,
      props: true,
    },
    {
      path: "/charts/",
      component: Charts,
      children: [
        {path: '', name: "charts", redirect: {name: "web-of-transnational-deals"}},
        {
          path: "web-of-transnational-deals/",
          name: "web-of-transnational-deals",
          component: WebOfTransnationalDeals,
        },
        {
          path: "perspective/",
          name: "its-a-big-deal",
          component: ItsABigDeal,
        },
      ]
    },
    {
      path: "/404/",
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
    {
      path: "*",
      name: "wagtail",
      component: WagtailPage,
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

export default router;
