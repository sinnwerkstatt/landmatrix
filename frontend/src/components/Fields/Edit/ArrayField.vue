<template>
  <div>
    <select v-model="val" multiple :name="formfield.name">
      <option v-for="(v, k) in formfield.choices" :key="k" :value="k">{{ v }}</option>
    </select>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
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
