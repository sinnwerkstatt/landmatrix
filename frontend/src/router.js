import Vue from 'vue';
import Router from 'vue-router';
import DealDetail from "./views/DealDetail";
import DealList from "./views/DealList";

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: 'newdeal', //process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'deal_list',
      component: DealList,
    },
    {
      path: '/:deal_id',
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
