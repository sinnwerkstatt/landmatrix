<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  interface Props {
    value: unknown | null
    fieldname: string
    wrapperClass?: string
    labelClass?: string
    valueClass?: string
    showLabel?: boolean
    model?: "deal" | "investor"
    extras?: unknown | undefined
  }

  let {
    value,
    fieldname,
    wrapperClass = WRAPPER_CLASS,
    labelClass = LABEL_CLASS,
    valueClass = VALUE_CLASS,
    showLabel = false,
    model = "deal",
    extras = undefined,
  }: Props = $props()

  let richField = $derived(
    model === "deal" ? $dealFields[fieldname] : $investorFields[fieldname],
  )

  let allExtras = $derived(
    richField?.extras && extras
      ? { ...richField.extras, ...extras }
      : (richField?.extras ?? extras),
  )
</script>

{#if isNotEmpty(value)}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if showLabel}
      <Label2 value={richField?.label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if richField && richField.displayField}
        {#if allExtras}
          <richField.displayField {value} extras={allExtras} />
        {:else}
          <richField.displayField {value} />
        {/if}
      {:else}
        <div class="italic text-red-400">unknown field: {fieldname}</div>
      {/if}
    </div>
  </div>
{/if}
