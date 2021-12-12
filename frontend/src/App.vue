<template>
  <div id="app">
    <Navbar />
    <Messages />
    <BreadcrumbBar v-if="$store.state.showBreadcrumbs" />
    <main class="content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import BreadcrumbBar from "$components/BreadcrumbBar.vue";
  import Footer from "$components/Footer.vue";
  import Messages from "$components/Messages.vue";
  import Navbar from "$components/Navbar.vue";

  export default Vue.extend({
    name: "Landmatrix",
    components: { Navbar, Messages, BreadcrumbBar, Footer },
    metaInfo: {
      title: "Land Matrix",
      titleTemplate: "%s | Land Matrix",
    },
  });
</script>

<style lang="scss" scoped>
  .content {
    // 60px navbar, 56px breadcrumbs, 31px footer
    min-height: calc(100vh - 60px - 56px - 31px);
  }
</style>
