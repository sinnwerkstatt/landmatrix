<template>
  <component :is="pageType"></component>
</template>

<script>
  import store from "/store";
  import WagtailPage from "./WagtailPage";
  import BlogIndexPage from "./BlogIndexPage";
  import BlogPage from "./BlogPage";
  import ObservatoryPage from "./ObservatoryPage";

  export default {
    components: { BlogIndexPage, BlogPage, WagtailPage, ObservatoryPage },
    computed: {
      pageType() {
        let page = this.$store.state.page.wagtailPage;
        switch (page.meta.type) {
          case "blog.BlogIndexPage":
            return BlogIndexPage;
            break;
          case "blog.BlogPage":
            return BlogPage;
            break;
          case "wagtailcms.RegionPage":
            return ObservatoryPage;
            break;
          case "wagtailcms.CountryPage":
            return ObservatoryPage;
            break;
          default:
            return WagtailPage;
        }
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
