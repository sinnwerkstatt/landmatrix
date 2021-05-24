<template>
  <div id="app">
    <Navbar />
    <Messages />
    <BreadcrumbBar />
    <main class="content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
  import BreadcrumbBar from "$components/BreadcrumbBar";
  import Footer from "$components/Footer";
  import Messages from "$components/Messages";
  import Navbar from "$components/Navbar";

  export default {
    name: "Landmatrix",
    components: { Navbar, Messages, BreadcrumbBar, Footer },
    metaInfo: {
      title: "Land Matrix",
      titleTemplate: "%s | Land Matrix",
    },
  };
</script>

<style lang="scss" scoped>
  .content {
    min-height: calc(100vh - 60px - 31px - 31px);
  }
</style>
