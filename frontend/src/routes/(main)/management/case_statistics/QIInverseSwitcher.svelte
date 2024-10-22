<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Model } from "$lib/types/data"

  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"

  export let inverse: boolean
  export let model: Model
</script>

<div class="flex flex-col p-2 font-bold italic text-gray-700 dark:text-gray-100">
  <span>
    {model === "deal" ? $_("Showing deals") : $_("Showing investors")}
  </span>
  <CheckboxSwitch {model} bind:checked={inverse}>
    <svelte:fragment slot="left">
      {$_("Meeting quality indicator condition")}
    </svelte:fragment>
    <svelte:fragment>
      {$_("Not meeting quality indicator condition")}
    </svelte:fragment>
  </CheckboxSwitch>
</div>
