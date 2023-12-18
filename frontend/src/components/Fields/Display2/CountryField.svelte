<script lang="ts">
  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: Country | undefined | number
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {$countries.find(c => c.id === (value?.id ?? value))?.name ?? ""}
    </div>
  </div>
{/if}
