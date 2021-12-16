<template>
  <component :is="pageType" v-if="pageType" />
</template>

<script lang="ts">
  import BlogIndexPage from "./BlogIndexPage.vue";
  import BlogPage from "./BlogPage.vue";
  import ObservatoryPage from "./ObservatoryPage.vue";
  import Vue from "vue";
  import WagtailPage from "./WagtailPage.vue";
  import store from "$store";

  export default Vue.extend({
    name: "WagtailSwitch",
    components: { BlogIndexPage, BlogPage, WagtailPage, ObservatoryPage },
    beforeRouteEnter: (to, from, next) => {
      store
        .dispatch("fetchWagtailPage", to.path)
        .then(() => next())
        // the params are fine, this is a vue-router "hack" to keep the path
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
    beforeRouteUpdate(to, from, next) {
      store
        .dispatch("fetchWagtailPage", to.path)
        .then(() => next())
        // the params are fine, this is a vue-router "hack" to keep the path
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
    metaInfo() {
      const title = this.$store.state.title;
      if (this.$route.path === "/") return { title, titleTemplate: "Land Matrix" };
      return { title };
    },
    computed: {
      pageType() {
        if (!this.$store.state?.wagtailPage) return null;
        let page = this.$store.state.wagtailPage;
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
            this.$router.push(`/about/${this.$store.state.aboutPages[0].meta.slug}/`);
            return;
          default:
            return WagtailPage;
        }
      },
    },
  });
</script>
