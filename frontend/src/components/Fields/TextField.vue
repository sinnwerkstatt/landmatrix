<template>
  <b-input-group :append="formfield.unit">
    <b-form-input
      :id="`type-${formfield.class}`"
      :type="formfield.type || `text`"
      :placeholder="formfield.placeholder"
      v-model="val"
    />
  </b-input-group>
</template>

<script>
  export default {
    props: ["formfield", "value"],
    computed: {
      val: {
        get() {
          return this.value[this.formfield.class];
        },
        set(value) {
          this.value[this.formfield.class] = value;
        },
      },
    },
  };
</script>
