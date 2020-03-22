<template>
  <Streamfield :content="wagtailPage" />
</template>

<script>
  import Streamfield from "../components/Streamfield";

  export default {
    name: "WagtailPage",
    components: { Streamfield },
    computed: {
      wagtailPage() {
        return this.$store.state.wagtailPage;
      },
    },
  };
</script>

<style scoped></style>
