<template>
  <div style="white-space: nowrap">
    {{ thousandsep(value) }}
    <span v-if="formfield.unit">{{ formfield.unit }}</span>
  </div>
</template>

<script>
  import { thousandsep } from "$utils/filters";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
    },
    data() {
      return {
        thousandsep,
      };
    },
  };
</script>
