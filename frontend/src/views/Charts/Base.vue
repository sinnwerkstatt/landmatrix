<template>
  <div class="container">
    <charts-navbar/>
    <div class="my-3"></div>
    <FilterBar/>
    <div class="my-3"></div>
    <router-view></router-view>
  </div>
</template>

<script>
  import Navbar from "@/components/ChartsNavbar";
  import FilterBar from "@/components/FilterBar";

  export default {
    name: "Charts",
    components: {
      'charts-navbar': Navbar,
      FilterBar
    },
  };
</script>

<style scoped></style>
