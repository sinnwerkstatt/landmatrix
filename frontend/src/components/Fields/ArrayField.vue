<template>
  <div>
    <div v-if="readonly">
      {{parseValues(val)}}
    </div>
  </div>
</template>

<script>
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

        let choices = this.formfield.choices;
        if (choices) {
          let newchoices = {};
          for (let [key, value] of Object.entries(choices)) {
            if (typeof value == 'string') {
              newchoices[key] = value;
            } else {
              for (let [key, v] of Object.entries(value)) {
                newchoices[key] = v;
              }

            }
          }
          choices = newchoices;
        }

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
