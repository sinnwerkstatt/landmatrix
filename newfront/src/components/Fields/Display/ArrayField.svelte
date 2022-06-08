<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "$components/Fields/fields";
  import {
    flat_intention_of_investment_map,
    intention_of_investment_map,
  } from "./choices";

  export let formfield: FormField;
  export let value: string[];

  //  BIOFUELS: ["Biofuels", PlaneIcon],

  export function parseValues(value) {
    let ret = "";
    if (formfield.choices) {
      ret += value.map((v) => formfield.choices[v]).join(", ");
    } else ret += value.join(", ");
    return ret;
  }
</script>

<div class="array_field">
  {#if formfield.name === "current_intention_of_investment"}
    {#each value as ioi}
      <span class="ioi-label">
        {#if intention_of_investment_map[ioi] != null}
          <svelte:component this={intention_of_investment_map[ioi]} />
        {/if}
        {$_(flat_intention_of_investment_map[ioi])}
      </span>
    {/each}
  {:else}
    {@html parseValues(value)}
  {/if}
</div>
