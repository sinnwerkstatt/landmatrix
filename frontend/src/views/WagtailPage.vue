<template>
  <Streamfield :content="content" />
</template>

<script>
  import Streamfield from "/components/Streamfield";
  import store from "/store";

  export default {
    components: { Streamfield },
    computed: {
      content() {
        let page = this.$store.state.page.wagtailPage;
        return page ? page.body : null;
      },
    },
    beforeRouteEnter: (to, from, next) => {
      store.dispatch("fetchWagtailPage", to.path);
      next();
    },
    beforeRouteUpdate(to, from, next) {
      store.dispatch("fetchWagtailPage", to.path);
      next();
    },
  };
</script>

<style scoped></style>
