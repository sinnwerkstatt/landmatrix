<template>
  <div class="label" :class="[this.narrow ? 'col-md-6' : 'col-md-5 col-lg-4']">
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
      narrow: {
        type: Boolean,
        default: false,
      },
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
