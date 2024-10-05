<script lang="ts">
  import { _ } from "svelte-i18n"

  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"

  export let inverse: boolean
  export let model: "deal" | "investor"
</script>

<div class="flex gap-2 p-2 font-bold italic text-gray-700">
  {$_(
    "Show inverse ({dealsOrInvestors} not fulfilling the quality indicator condition):",
    {
      values: {
        dealsOrInvestors: `${model}s`,
      },
    },
  )}
  <CheckboxSwitch {model} bind:checked={inverse}>
    <svelte:fragment slot="left">
      {$_("No")}
    </svelte:fragment>
    <svelte:fragment>
      {$_("Yes")}
    </svelte:fragment>
  </CheckboxSwitch>
</div>
