<template>
  <div style="white-space: nowrap;">
    {{ value.toLocaleString() }}
    <span v-if="formfield.unit">{{ formfield.unit }}</span>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
    },
  };
</script>
