<template>
  <div class="container">
    <div v-html="map_introduction"></div>
    <FilterBar />
    <big-map :options="{zoom:2}" />
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import FilterBar from "@/components/FilterBar";

  export default {
    name: "GlobalMap",
    components: { BigMap, FilterBar },
    data() {
      return {
        map_introduction: MAP_INTRODUCTION,
      };
    },
    beforeRouteEnter(to, from, next) {
      let title = "Global: Map";
      store.dispatch("setPageContext", {
        title,
        breadcrumbs: [{ link: { name: "wagtail" }, name: "Home" }, { name: title }],
      });
      next();
    },
  };
</script>

<style lang="scss" scoped></style>
