<template>
  <div>
    <PageTitle :title="page.title"></PageTitle>
    <Streamfield :content="content" />
  </div>
</template>

<script>
  import Streamfield from "/components/Streamfield";
  import PageTitle from "../../components/PageTitle";

  export default {
    components: {PageTitle, Streamfield },
    computed: {
      content() {
        let page = this.$store.state.page.wagtailPage;
        return page ? page.body : [];
      },
    },
  };
</script>

<style scoped></style>
