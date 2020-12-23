<template>
  <div class="container mb-2" v-if="$store.state.page.showBreadcrumbs">
    <div class="row">
      <div class="col-md-8 mr-auto">
        <ul class="breadcrumb">
          <li v-for="bcrumb in $store.state.page.breadcrumbs" :key="bcrumb.name">
            <a v-if="bcrumb.link" :href="getUrl(bcrumb.link)">{{ bcrumb.name }}</a>
            <template v-else>{{ bcrumb.name }}</template>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    methods: {
      getUrl(route_name) {
        return this.$router.resolve(route_name).href;
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
    padding: 5px 0 0 0;
    font-size: 14px;
    list-style: none;
    border-radius: 4px;

    > li {
      text-shadow: none !important;
      display: inline-block;
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
    > li > a {
      padding: 2px 5px;
      border-radius: 4px;
      display: inline-block;
      color: $lm_dark;
    }
    .router-link-active {
      color: $lm_offwhite;
      background-color: $lm_dark;
      border-radius: 4px;
    }
  }
</style>
