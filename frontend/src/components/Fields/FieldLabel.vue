<template>
  <div :class="labelClasses">
    {{ label }}
  </div>
</template>

<script>
  import { mapState } from "vuex";

  export default {
    name: "FieldLabel",
    props: {
      fieldname: {
        type: String,
        required: true,
      },
      model: { type: String, default: "deal" },
      labelClasses: { type: Array, default: () => ["label", "col-md-5", "col-lg-4"] },
    },
    computed: {
      label() {
        return this.formfields[this.model][this.fieldname].label;
      },
      ...mapState({
        formfields: (state) => state.formfields,
      }),
    },
  };
</script>

<style lang="scss" scoped>
  @import "src/scss/colors";

  .label {
    font-weight: 500;
  }
</style>
