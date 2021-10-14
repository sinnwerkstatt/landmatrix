<template>
  <div>
    <PageTitle>{{ page.title }}</PageTitle>
    <Streamfield :content="content" />
  </div>
</template>

<script lang="ts">
  import PageTitle from "$components/PageTitle.vue";
  import Streamfield from "$components/Streamfield.vue";
  import Vue from "vue";
  import type { WagtailPage, WagtailStreamfield } from "$types/wagtail";

  export default Vue.extend({
    components: { PageTitle, Streamfield },
    computed: {
      page(): WagtailPage {
        return this.$store.state.page.wagtailPage;
      },
      content(): WagtailStreamfield {
        return this.page?.body || [];
      },
    },
  });
</script>
