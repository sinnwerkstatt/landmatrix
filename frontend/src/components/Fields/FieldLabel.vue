<template>
  <div :class="labelClasses">
    {{ $t(label) }}
  </div>
</template>

<script>
  export default {
    name: "FieldLabel",
    props: {
      fieldname: { type: String, required: true },
      model: { type: String, default: "deal" },
      labelClasses: { type: Array, default: () => ["label", "col-md-5", "col-lg-4"] },
    },
    computed: {
      label() {
        return this.$store.state.formfields[this.model][this.fieldname].label;
      },
    },
  };
</script>

<style lang="scss" scoped>
  .label {
    font-weight: 500;
  }
</style>
