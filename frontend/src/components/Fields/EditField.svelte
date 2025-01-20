<script lang="ts">
  import type { Snippet } from "svelte"
  import { _ } from "svelte-i18n"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import type { Model } from "$lib/types/data"

  import { getMutableObject } from "$components/Data/stores"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import DSQuotationsModal from "$components/New/DSQuotationsModal.svelte"

  interface Props {
    value: unknown | null
    fieldname: string
    wrapperClass?: string
    labelClass?: string
    valueClass?: string
    showLabel?: boolean
    model?: Model
    extras?: { [key: string]: unknown }
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
  const quotes = $derived($mutableObj.selected_version.ds_quotations[fieldname] ?? [])

  let showDSQuotationModal = $state(false)
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if showLabel}
    <Label2 value={richField?.label} class={labelClass} />
  {/if}

  {#if richField?.useQuotation}
    <div>
      <button
        class="italic text-purple-400"
        type="button"
        onclick={() => {
          showDSQuotationModal = true
        }}
      >
        {quotes.length}
        {$_("quotations")}
      </button>

      <DSQuotationsModal
        bind:open={showDSQuotationModal}
        {fieldname}
        {model}
        label={richField.label}
        editable
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
