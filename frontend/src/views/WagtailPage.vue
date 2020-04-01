<template>
  <Streamfield :content="wagtailPage" />
</template>

<script>
  import Streamfield from "../components/Streamfield";
  import store from "../store";

  export default {
    // name: "WagtailPage",
    components: { Streamfield },
    computed: {
      wagtailPage() {
        return this.$store.state.wagtailPage;
      },
    },
    beforeRouteUpdate(to, from, next) {
      let target = to.path.replace("/newdeal", ""); // TODO: Remove this eventually
      store.dispatch("fetchWagtailPage", target);
      next();
    },
  };
</script>

<style scoped></style>
