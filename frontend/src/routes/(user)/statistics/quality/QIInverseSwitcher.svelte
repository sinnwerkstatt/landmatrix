<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Model } from "$lib/types/data"

  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"

  interface Props {
    inverse: boolean
    model: Model
  }

  let { inverse = $bindable(), model }: Props = $props()
</script>

<div class="flex flex-col p-2 font-bold italic text-gray-700 dark:text-gray-100">
  <span>
    {model === "deal" ? $_("Showing deals") : $_("Showing investors")}
  </span>
  <CheckboxSwitch {model} id="inverse" bind:checked={inverse}>
    {#snippet left()}
      {$_("Meeting quality indicator condition")}
    {/snippet}

    {$_("Not meeting quality indicator condition")}
  </CheckboxSwitch>
</div>
