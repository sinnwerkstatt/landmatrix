<template>
  <component :is="pageType" v-if="pageType" />
</template>

<script>
  import store from "$store";
  import BlogIndexPage from "./BlogIndexPage";
  import BlogPage from "./BlogPage";
  import ObservatoryPage from "./ObservatoryPage";
  import WagtailPage from "./WagtailPage";

  export default {
    name: "WagtailSwitch",
    components: { BlogIndexPage, BlogPage, WagtailPage, ObservatoryPage },
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
    metaInfo() {
      let ret = { title: this.$store.state.page.title };
      if (this.$route.path === "/") ret.titleTemplate = "Land Matrix";
      return ret;
    },
    computed: {
      pageType() {
        if (!this.$store.state?.page?.wagtailPage) return null;
        let page = this.$store.state.page.wagtailPage;
        switch (page.meta?.type) {
          case "blog.BlogIndexPage":
            return BlogIndexPage;
          case "blog.BlogPage":
            return BlogPage;
          case "wagtailcms.RegionPage":
            return ObservatoryPage;
          case "wagtailcms.CountryPage":
            return ObservatoryPage;
          case "wagtailcms.ObservatoryPage":
            return ObservatoryPage;
          case "wagtailcms.ObservatoryIndexPage":
            // eslint-disable-next-line vue/no-side-effects-in-computed-properties
            this.$router.push("/observatory/global/");
            return;
          case "wagtailcms.AboutIndexPage":
            // eslint-disable-next-line vue/no-side-effects-in-computed-properties
            this.$router.push(
              `/about/${this.$store.state.page.aboutPages[0].meta.slug}/`
            );
            return;
          default:
            return WagtailPage;
        }
      },
    },
  };
</script>

<style scoped></style>
