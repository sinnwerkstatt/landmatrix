<template>
  <div>
    <div v-if="formfield.class === 'NullBooleanField'">
      <select v-model="val" :name="formfield.name" class="form-control">
        <option v-if="!formfield.required" :value="null">--------</option>
        <option :value="true">{{ $t("Yes") }}</option>
        <option :value="false">{{ $t("No") }}</option>
      </select>
    </div>
    <input v-else v-model="val" type="checkbox" :name="formfield.name" />
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Boolean, required: false },
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
