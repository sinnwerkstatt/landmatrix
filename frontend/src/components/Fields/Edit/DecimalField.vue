<template>
  <div>
    <LowLevelDecimalField
      v-model="val"
      :required="formfield.required"
      :unit="formfield.unit"
      :max-value="formfield.max_value"
      :min-value="formfield.min_value"
      :step="formfield.class === 'IntegerField' ? 1 : 0.01"
    />
  </div>
</template>

<script>
  import LowLevelDecimalField from "./LowLevelDecimalField";
  export default {
    components: { LowLevelDecimalField },
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: false, default: null },
      model: { type: String, required: true },
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", v);
        },
      },
    },
  };
</script>
