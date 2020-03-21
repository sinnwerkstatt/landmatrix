<template>
  <div v-html="wagtailPage"></div>
</template>

<script>
  import store from '../store';

  export default {
    name: "WagtailPage",
    computed: {
      wagtailPage() {
        return this.$store.state.wagtailPage;
      },
    }
  }
</script>

<style scoped>

</style>
