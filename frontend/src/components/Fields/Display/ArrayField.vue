<template>
  <div>
    {{ parseValues(value) }}
  </div>
</template>

<script>
  import { flatten_choices } from "/utils";

  export default {
    props: ["formfield", "value"],
    methods: {
      parseValues: function (value) {
        let ret = "";

        let choices = flatten_choices(this.formfield.choices);

        if (value instanceof Array) {
          if (choices) {
            ret += value.map((v) => choices[v]).join(", ");
          } else ret += value.join(", ");
        } else {
          if (choices) ret += choices[value];
          else ret += value;
        }
        return ret;
      },
    },
  };
</script>
