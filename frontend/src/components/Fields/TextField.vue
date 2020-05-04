<template>
  <div class="input-group">
    <input
      :id="`type-${formfield.name}`"
      :type="formfield.type || `text`"
      class="form-control"
      :placeholder="formfield.placeholder"
      :aria-label="formfield.placeholder"
      v-model="val"
      @input="emitVal"
    />
    <div class="input-group-append">
      <span class="input-group-text">{{ formfield.unit }}</span>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
