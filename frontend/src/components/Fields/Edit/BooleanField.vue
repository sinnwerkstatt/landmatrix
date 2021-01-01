<template>
  <div>
    <div v-if="formfield.class === 'NullBooleanField'">
      <select
        :value="value"
        :name="formfield.name"
        class="form-control"
        @input="emitVal"
      >
        <option v-if="!formfield.required" value=""></option>
        <option :value="true">{{ $t("Yes") }}</option>
        <option :value="false">{{ $t("No") }}</option>
      </select>
    </div>
    <input
      v-else
      class="form-check-input"
      type="checkbox"
      :name="formfield.name"
      :value="value"
    />
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Boolean, required: true },
      model: { type: String, required: true },
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
