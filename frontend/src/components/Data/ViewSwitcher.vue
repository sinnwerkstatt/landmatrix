<template>
  <div class="viewswitcher">
    <router-link :to="{name:'data_list'}">Data</router-link>
    <router-link :to="{name:'map'}">Map</router-link>
  </div>
</template>

<script>
  export default {
    name: "ViewSwitcher"
  }
</script>

<style lang="scss">
  .viewswitcher {
    position: absolute;
    left: 50%;
    z-index: 5000;
  }
</style>
