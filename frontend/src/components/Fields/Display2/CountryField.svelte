<script lang="ts">
  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: Country
  export let fieldname: string
  export let label = ""
  export let hideLabel = false
</script>

{#if value}
  <div class="mb-3 flex flex-wrap leading-5" data-fieldname={fieldname}>
    {#if !hideLabel}
      <Label2 value={label} class="md:w-5/12 lg:w-4/12" />
    {/if}
    <div class="text-lm-dark dark:text-white md:w-7/12 lg:w-8/12">
      {$countries.find(c => c.id === value.id)?.name ?? ""}
    </div>
  </div>
{/if}
