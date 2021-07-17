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
  .paragraph {
    a {
      color: var(--color-lm-orange);
    }
  }
</style>
