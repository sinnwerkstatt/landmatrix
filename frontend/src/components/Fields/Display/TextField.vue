<template>
  <div>
    <template v-if="formfield.type === 'url'">
      <a :href="value" target="_blank">{{ value }}</a>
    </template>
    <template v-else>
      {{ parseVal(value) }}
    </template>
  </div>
</template>

<script>
  import { parseFormFieldValue } from "../fieldHelpers";

  export default {
    props: ["formfield", "value"],
    methods: {
      parseVal(val) {
        return parseFormFieldValue(this.formfield, val);
      },
    },
  };
</script>
