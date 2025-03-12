<script lang="ts">
  import type { Snippet } from "svelte"

  import { dealFields, investorFields, isPrefixed } from "$lib/fieldLookups"
  import type { Model, QuotationItem } from "$lib/types/data"
  import { customIsNull } from "$lib/utils/dataProcessing"

  import { getMutableObject } from "$components/Data/stores"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import SourcesEditButton from "$components/Quotations/SourcesEditButton.svelte"

  interface Props {
    value: unknown | null
    fieldname: string
    wrapperClass?: string
    labelClass?: string
    valueClass?: string
    showLabel?: boolean
    model?: Model
    extras?: { [key: string]: unknown }
    disableQuotations?: boolean
    // edit specific
    children?: Snippet
    onchange?: () => void
  }

  let {
    value = $bindable(),
    fieldname,
    wrapperClass = "mb-10 leading-5 flex flex-col",
    labelClass = "font-semibold mb-4 w-full",
    valueClass = "text-gray-700 dark:text-white w-full",
    showLabel = false,
    model = "deal",
    extras = undefined,
    disableQuotations = false,
    children,
    onchange,
  }: Props = $props()

  let richField = $derived(
    model === "deal" ? $dealFields[fieldname] : $investorFields[fieldname],
  )

  let allExtras = $derived(
    richField?.extras && extras
      ? { ...richField.extras, ...extras }
      : (richField?.extras ?? extras),
  )

  const mutableObj = getMutableObject(model)

  // sanity check if mutableObj is defined -> deal/investor edit view
  let isEditView = $derived(!!$mutableObj)
  let isSubmodelField = $derived(isPrefixed(fieldname))

  const getQuotes = (): QuotationItem[] =>
    ($mutableObj.selected_version.ds_quotations[fieldname] ?? []) as QuotationItem[]
  const setQuotes = (quotes: QuotationItem[]): void => {
    if (quotes.length) {
      $mutableObj.selected_version.ds_quotations[fieldname] = quotes
    } else {
      delete $mutableObj.selected_version.ds_quotations[fieldname]
    }
  }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if showLabel}
    <Label2
      value={richField?.label}
      class={labelClass}
      contextHelp={richField.editContextHelp}
    />
  {/if}

  {#if isEditView && !richField.isJson && !isSubmodelField && !disableQuotations}
    <div>
      <SourcesEditButton
        {fieldname}
        bind:quotes={getQuotes, setQuotes}
        dataSources={$mutableObj.selected_version.datasources}
        disabled={customIsNull(value)}
      />
    </div>
  {/if}

  <div class={valueClass}>
    {#if richField && richField.editField}
      {@const RichEditField = richField.editField}

      <RichEditField bind:value extras={allExtras} {fieldname} {onchange}>
        {@render children?.()}
      </RichEditField>
    {:else}
      <div class="italic text-red-400">unknown field: {fieldname}</div>
    {/if}
  </div>
</div>
