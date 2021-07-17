<template>
  <div class="">
    {{ value }}
    {{ formfield }}
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Array, Object], required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        current: -1,
      };
    },
    computed: {
      vals: {
        get() {
          return this.value || [{ date: null, value: null }];
        },
        set(val) {
          this.updateValue(val);
        },
      },
    },
  };
</script>
<style lang="scss" scoped>
  .input-group {
    padding: 0.4em;
  }

  .multiselect {
    width: 60%;
  }
</style>
