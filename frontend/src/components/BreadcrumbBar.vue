<template>
  <div class="breadcrumb-bar container">
    <div class="row">
      <div class="col-md-8 mr-auto">
        <ul class="breadcrumb">
          <li v-for="bcrumb in $store.state.breadcrumbs" :key="bcrumb.name">
            <router-link v-if="bcrumb.link" :to="bcrumb.link">{{
              bcrumb.name
            }}</router-link>
            <template v-else>{{ bcrumb.name }}</template>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import Vue from "vue";

  export default Vue.extend({
    name: "BreadcrumbBar",
  });
</script>

<style lang="scss" scoped>
  .breadcrumb-bar {
    margin-bottom: 0.5rem;
  }
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
      color: var(--color-lm-dark);
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
      color: var(--color-lm-dark);
    }
    .router-link-active {
      color: #fcfcfc;
      background-color: var(--color-lm-dark);
      border-radius: 4px;
    }
  }
</style>
