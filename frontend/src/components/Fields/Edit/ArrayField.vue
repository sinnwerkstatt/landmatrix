<template>
  <div>
    <div v-if="formfield.choices">
      <!--      <label class="mr-sm-2 mb-0 sr-only" :for="formfield.name">-->
      <!--        {{ formfield.label }}-->
      <!--      </label>-->
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
      value: { type: Array, required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {};
    },
    computed: {
      val: {
        get() {
          return this.value || [];
        },
        set(v) {
          this.$emit("input", v);
        },
      },
      freetext_values() {
        return [...this.val, ""];
      },
    },
  };
</script>
