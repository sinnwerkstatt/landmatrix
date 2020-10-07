<template>
  <div id="app">
    <Navbar />
    <div class="content">
      <Messages />
      <BreadcrumbBar />
      <div v-if="$store.state.page.title" class="container">
        <div class="row">
          <div class="col-md-12">
            <h1>
              <span v-html="$store.state.page.title"></span>
            </h1>
          </div>
        </div>
      </div>
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
  import Navbar from "/components/Navbar";
  import Messages from "/components/Messages";
  import BreadcrumbBar from "/components/BreadcrumbBar";
  import Footer from "/components/Footer";

  export default {
    components: { Navbar, Messages, BreadcrumbBar, Footer },
  };
</script>

<style lang="scss" scoped>
  @import "scss/colors";
  @import "scss/fonts";

  .content {
    min-height: calc(100vh - 60px - 31px);
  }
</style>
