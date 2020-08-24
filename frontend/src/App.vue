<template>
  <div id="app">
    <Navbar />
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

<style lang="scss">
  @import "scss/colors";
  @import "scss/fonts";
</style>
