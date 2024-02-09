<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: unknown | null
  export let fieldname: string
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let showLabel = false
  export let model: "deal" | "investor" = "deal"

  export let extras: unknown | undefined = undefined

  $: richField = model === "deal" ? $dealFields[fieldname] : $investorFields[fieldname]

  $: allExtras =
    richField?.extras && extras
      ? { ...richField.extras, ...extras }
      : richField?.extras ?? extras
</script>

<!-- TODO probably need to handle booleanfield (when the field is !== null, we show it. also when it's `false` -->
{#if isNotEmpty(value)}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if showLabel}
      <Label2 value={richField?.label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if richField && richField.displayField}
        {#if allExtras}
          <svelte:component this={richField.displayField} {value} extras={allExtras} />
        {:else}
          <svelte:component this={richField.displayField} {value} />
        {/if}
      {:else}
        <div class="italic text-red-400">unknown field</div>
      {/if}
    </div>
  </div>
{/if}
