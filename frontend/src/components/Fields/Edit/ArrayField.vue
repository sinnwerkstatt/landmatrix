<template>
  <div>
    <div v-if="formfield.choices">
      <select v-model="val" multiple :name="formfield.name" class="form-control">
        <option v-for="(v, k) in formfield.choices" :key="k" :value="k">{{ v }}</option>
      </select>
    </div>
    <div v-else>
      <div v-for="v in freetext_values">
        <input class="form-text" type="text" :value="v" />
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    data() {
      return {
        freetext_values: [...this.value, ""],
      };
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
