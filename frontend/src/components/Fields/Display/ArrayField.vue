<template>
  <div>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <span v-html="parseValues(value)"></span>
  </div>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import { flatten_choices } from "$utils";
  import { intention_of_investment_map } from "$utils/choices";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    methods: {
      parseValues(value: string[]) {
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

        let ret = "";
        if (this.formfield.choices) {
          let choices = flatten_choices(this.formfield.choices);
          ret += value.map((v) => choices[v]).join(", ");
        } else ret += value.join(", ");
        return ret;
      },
    },
  });
</script>
