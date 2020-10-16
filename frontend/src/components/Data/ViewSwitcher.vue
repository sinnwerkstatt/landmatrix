<template>
  <div class="viewswitcher">
    <router-link :to="{name:'map'}">Map</router-link>
    <router-link :to="{name:'data_list'}">Data</router-link>
  </div>
</template>

<script>
  export default {
    name: "ViewSwitcher"
  }
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  .viewswitcher {
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    top: 10px;
    left: 0;
    right: 0;
    text-align: center;
    z-index: 1000;
    font-size: 0;
    filter: drop-shadow(3px 3px 3px rgba(0, 0, 0, 0.5));
    a {
      margin: 0;
      padding: 0.3em 2em;
      background-color: white;
      color: black;
      font-size: 14px;
      font-weight: bold;
      &.router-link-active {
        background-color: $primary;
        color: white;
      }
    }
  }
</style>
