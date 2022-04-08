<template>
  <div class="date_field">
    <LowLevelDateYearField v-model="val" />
  </div>
</template>

<script>
  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField";

  export default {
    name: "DateField",
    components: { LowLevelDateYearField },
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Date, String], required: false, default: null },
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
