<template>
  <div class="container">
    <charts-navbar/>
    <div class="my-3"></div>
    <div class="my-3"></div>
    <router-view></router-view>
  </div>
</template>

<script>
  import Navbar from "@/components/ChartsNavbar";

  export default {
    name: "Charts",
    components: {
      'charts-navbar': Navbar,
    },
  };
</script>

<style scoped></style>
