<template>
  <Streamfield :content="content" />
</template>

<script>
  import Streamfield from "/components/Streamfield";

  export default {
    components: { Streamfield },
    computed: {
      content() {
        let page = this.$store.state.page.wagtailPage;
        return page ? page.body : [];
      },
    },
  };
</script>

<style scoped></style>
