<template>
  <div>
    <span v-html="parseValues(value)"></span>
  </div>
</template>

<script>
  import { flatten_choices } from "utils";
  import { intention_of_investment_map } from "choices";

  export default {
    props: ["formfield", "value", "model"],
    methods: {
      parseValues: function (value) {
        if (this.formfield.name === "current_intention_of_investment") {
          return value
            .map((ioi) => {
              let [intention, icon] = intention_of_investment_map[ioi];
              return `<span class="ioi-label">
                    <i class="${icon}"></i> ${this.$t(intention)}
                    </span>`;
            })
            .join(" ");
        }

        let choices = flatten_choices(this.formfield.choices);
        let ret = "";
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
