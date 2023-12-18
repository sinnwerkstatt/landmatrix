<script lang="ts">
  import { _ } from "svelte-i18n"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: boolean | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"
</script>

{#if value !== null}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if value === true}
        {$_("Yes")}
      {:else if value === false}
        {$_("No")}
      {:else}
        —
      {/if}
    </div>
  </div>
{/if}
