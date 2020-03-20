import Vue from 'vue';
import Router from 'vue-router';
import DealList from "./views/DealList";
import DealEdit from "./views/DealEdit";
import DealDetail from "./views/DealDetail";
import GlobalMap from "./views/GlobalMap";

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/newdeal/',
      name: 'deal_list',
      component: DealList,
    },
    {
      path: '/newdeal/map',
      name: 'map',
      component: GlobalMap
    },
    {
      path: '/newdeal/add',
      name: 'deal_create',
      component: DealEdit,
      props: true,
    },
    {
      path: '/edit/:deal_id',
      name: 'deal_edit',
      component: DealEdit,
      props: true,
    },
    {
      path: '/newdeal/:deal_id',
      name: 'deal_detail',
      component: DealDetail,
      props: true,
    },
  ]
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
