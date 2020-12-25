<template>
  <div class="row">
    <div class="col-sm-12">
      <div class="paragraph" v-html="value"></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "WagtailParagraph",
    props: {
      value: { type: String, required: true },
    },
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
