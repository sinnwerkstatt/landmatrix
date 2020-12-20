<template>
  <div style="white-space: nowrap;">
    {{ value.toLocaleString() }}
    <span v-if="formfield.name === 'deal_size'">ha</span>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
  };
</script>
