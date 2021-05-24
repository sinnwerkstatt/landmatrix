<template>
  <div>
    <PageTitle :title="page.title" />
    <Streamfield :content="content" />
  </div>
</template>

<script>
  import PageTitle from "$components/PageTitle";
  import Streamfield from "$components/Streamfield";

  export default {
    components: { PageTitle, Streamfield },
    computed: {
      page() {
        return this.$store.state.page.wagtailPage;
      },
      content() {
        return this.page ? this.page.body : [];
      },
    },
  };
</script>
