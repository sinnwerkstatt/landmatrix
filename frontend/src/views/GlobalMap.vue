<template>

</template>

<script>
  import store from "@/store";

  export default {
    name: "GlobalMap",
    beforeRouteEnter(to, from, next) {
      store.dispatch('setPageContext', {
        title: "Global: Map",
        breadcrumbs: [{name: "Map"}]
      });
      next()
    },
  }
</script>

<style scoped>

</style>
