<template>
  <div class="paragraph" v-html="value"></div>
</template>

<script>
  export default {
    name: "WagtailParagraph",
    props: ["value"],
  };
</script>

<style lang="scss">
  @import "../../scss/colors";
  .paragraph {
    a {
      color: $primary;
    }
  }
</style>
