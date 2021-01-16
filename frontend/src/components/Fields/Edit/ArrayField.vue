<template>
  <div>
    <div v-if="formfield.choices">
      <label class="mr-sm-2 mb-0 sr-only" :for="formfield.name">
        {{ formfield.label }}
      </label>
      <select v-model="val" multiple :name="formfield.name" class="form-control">
        <option v-if="!formfield.required" :value="null">--------</option>
        <option v-for="(v, k) in formfield.choices" :key="k" :value="k">{{ v }}</option>
      </select>
    </div>
    <div v-else>
      <textarea v-model="val" class="form-control"></textarea>
      <small class="form-text text-muted">
        {{ $t("Put each value on a new line, i.e. press enter between each name") }}
      </small>
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
          let retval = this.value || [];
          if (!this.formfield.choices) {
            retval = retval.join("\n");
          }
          return retval;
        },
        set(v) {
          if (this.formfield.choices) {
            // deal with weird "[null]" array
            v = v.length === 1 && v[0] === null ? [] : v;
            this.$emit("input", v);
          } else {
            this.$emit("input", v.split("\n"));
          }
        },
      },
    },
  };
</script>
