<template>
  <component :is="pageType"></component>
</template>

<script>
  import store from "/store";
  import WagtailPage from "./WagtailPage";
  import BlogIndexPage from "./BlogIndexPage";
  import BlogPage from "./BlogPage";

  export default {
    componthisents: { BlogIndexPage, BlogPage, WagtailPage },
    computed: {
      pageType() {
        let page = this.$store.state.page.wagtailPage;
        if (page.meta.type === "blog.BlogIndexPage") {
          return BlogIndexPage;
        }
        if (page.meta.type === "blog.BlogPage") {
          return BlogPage;
        }
        return WagtailPage;
      },
    },
    beforeRouteEnter: (to, from, next) => {
      store
        .dispatch("fetchWagtailPage", to.path)
        .then(() => next())
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
    beforeRouteUpdate(to, from, next) {
      store
        .dispatch("fetchWagtailPage", to.path)
        .then(() => next())
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
  };
</script>

<style scoped></style>
