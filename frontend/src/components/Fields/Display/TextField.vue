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
  import { flatten_choices } from "$utils";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
    },
    methods: {
      parseVal(val) {
        if (val) {
          let choices = flatten_choices(this.formfield.choices, true);
          return choices ? choices[val] : val;
        }
        return "n/a";
      },
    },
  };
</script>
