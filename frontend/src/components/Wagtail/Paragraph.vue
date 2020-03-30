<template>
  <div class="container">
    <div class="paragraph" v-html="value"></div>
  </div>
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
