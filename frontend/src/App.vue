<template>
  <div id="app">
    <Navbar/>
    <BreadcrumbBar/>
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1><span>{{this.$store.state.title}}</span></h1>
        </div>
      </div>
      <router-view/>
    </div>

  </div>
</template>

<script>
  import Navbar from "@/components/Navbar";
  import BreadcrumbBar from "@/components/BreadcrumbBar";

  export default {
    components: {Navbar, BreadcrumbBar},
    data() {
      return {}
    }
  }
</script>

<style lang="scss">
  @import "scss/colors";
  @import "scss/fonts";

</style>
