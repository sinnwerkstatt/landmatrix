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
  import { flatten_choices } from "/utils";

  export default {
    props: ["formfield", "value"],
    methods: {
      parseVal(val) {
        if (val) {
          let choices = flatten_choices(this.formfield.choices);
          if (choices) return choices[val];
          return val;
        }
        return "n/a";
      },
    },
  };
</script>
