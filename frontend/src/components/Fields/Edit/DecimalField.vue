<template>
  <div style="white-space: nowrap;">
    {{ value }}
    <span v-if="formfield.name === 'deal_size'">ha</span>
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
