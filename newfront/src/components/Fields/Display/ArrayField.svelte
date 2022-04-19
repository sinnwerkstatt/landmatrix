<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "$components/Fields/fields";
  import { intention_of_investment_map } from "./choices";

  export let formfield: FormField;
  export let value: string[];

  export function parseValues(value) {
    if (formfield.name === "current_intention_of_investment") {
      return value
        .map((ioi) => {
          let [intention, icon] = intention_of_investment_map[ioi];
          // TODO: Charlotte hier noch SVGS
          return `<span class="ioi-label">
                    <i class="${icon}"></i> ${$_(intention)}
                    </span>`;
        })
        .join(" ");
    }

    let ret = "";
    if (formfield.choices) {
      ret += value.map((v) => formfield.choices[v]).join(", ");
    } else ret += value.join(", ");
    return ret;
  }
</script>

<div class="array_field">
  {@html parseValues(value)}
</div>
