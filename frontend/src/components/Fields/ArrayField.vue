<template>
  <div>
    <div v-if="readonly">
      {{parseValues(val)}}
    </div>
  </div>
</template>

<script>
  import {flatten_choices} from "/utils";

  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
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
