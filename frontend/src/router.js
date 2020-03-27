import Vue from "vue";
import Router from "vue-router";
import GlobalMap from "./views/GlobalMap";
import DealList from "./views/DealList";
import DealEdit from "./views/DealEdit";
import DealDetail from "./views/DealDetail";
import Charts from "./views/Charts";
import WagtailPage from "./views/WagtailPage";
import NotFound from "./views/NotFound";

import store from "./store";

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
      name: "charts",
      redirect: "/charts/web-of-transnational-deals/",
    },
    {
      path: "/charts/web-of-transnational-deals/",
      // name: "charts_web_o",
      component: Charts,
      props: true,
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
      beforeEnter: (to, from, next) => {
        let target = to.path.replace("/newdeal", ""); // TODO: Remove this eventually
        store.dispatch("fetchWagtailPage", target);
        next();
      },
    },
  ],
  //   {
  //     // catch requests not mapping any path and redirect to home
  //     path: '*',
  //     redirect: {
  //       name: 'home'
  //     }
  //   },
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
