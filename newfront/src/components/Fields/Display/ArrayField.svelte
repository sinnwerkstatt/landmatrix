<script lang="ts">
  import { flatten_choices } from "./index";
  import { intention_of_investment_map } from "./choices";
  import type { FormField } from "$components/Fields/fields";
  import { _ } from "svelte-i18n";

  export let formfield: FormField;
  export let value: string[];
  export let model: string;

  export function parseValues(value) {
    if (formfield.name === "current_intention_of_investment") {
      return value
        .map((ioi) => {
          let [intention, icon] = intention_of_investment_map[ioi];
          return `<span class="ioi-label">
                    <i class="${icon}"></i> ${$_(intention)}
                    </span>`;
        })
        .join(" ");
    }

    let ret = "";
    if (formfield.choices) {
      let choices = flatten_choices(formfield.choices);
      ret += value.map((v) => choices[v]).join(", ");
    } else ret += value.join(", ");
    return ret;
  }
</script>

<div class="array_field">
  <!-- eslint-disable-next-line vue/no-v-html -->
  ${parseValues(value)}
</div>
template>
