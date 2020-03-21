<template>
  <div class="container my-2">
    <div class="row">
      <div class="col-md-4 mr-auto">
        <ul class="breadcrumb">
          <li><a href="/">Home</a></li>
          <li v-for="bcrumb in this.$store.state.breadcrumbs" :key="bcrumb.name">
            <a v-if="bcrumb.href" :href="bcrumb.href">{{ bcrumb.name }}</a>
            <template v-else>{{ bcrumb.name }}</template>
          </li>
        </ul>
      </div>
      <div class="col-auto">
        <ul class="subnav nav nav-pills">
          <li class="nav-item" v-for="nav in this.$store.state.breadNav">
            <router-link v-if="!isCurrentRoute(nav.route)" :to="{ name: nav.route }">
              <i :class="nav.icon"></i> {{ nav.name }}
            </router-link>
            <span v-else> <i :class="nav.icon"></i> {{ nav.name }} </span>
          </li>
          <li class="divider"></li>
          <li role="presentation"></li>
          <li role="presentation"></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    methods: {
      isCurrentRoute(route) {
        return this.$route.name.startsWith(route);
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";

  .breadcrumb {
    clear: both;
    background: none;
    margin: 0 0 10px;
    padding: 0;
    font-size: 14px;
    list-style: none;
    border-radius: 4px;

    > li {
      text-shadow: none !important;
      display: inline-block;
      font-family: "Open Sans", sans-serif;
      color: $lm_dark;
      font-weight: 400;

      & ~ li:before {
        padding: 0 5px;
        color: #ccc;
        content: "/\00a0";
      }
    }
  }

  ul.subnav {
    > li > span {
      color: $lm_offwhite;
      background-color: $lm_dark;
      border-radius: 4px;
    }

    > li > a {
      padding: 2px 5px;
      border-radius: 4px;
      display: inline-block;
      color: $lm_dark;
    }
  }
</style>
