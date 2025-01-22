<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"
  import type { DataSource, Model, QuotationItem } from "$lib/types/data"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
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

  const quotes: QuotationItem[] = $derived(
    page.data[model]?.selected_version?.ds_quotations?.[fieldname] ?? {},
  )
  const dataSources: DataSource[] = $derived(
    page.data[model]?.selected_version?.datasources ?? [],
  )

  let showDSQuotationModal = $state(false)
</script>

{#if isNotEmpty(value)}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if showLabel}
      <Label2 value={richField?.label} class={labelClass} />
    {/if}

    <div class={valueClass}>
      <div class="flex gap-5">
        {#if richField && richField.displayField}
          {@const RichDisplayField = richField.displayField}

          <RichDisplayField {value} extras={allExtras} />
        {:else}
          <div class="italic text-red-400">unknown field: {fieldname}</div>
        {/if}

        {#if richField?.useQuotation && quotes.length > 0}
          <div>
            <button
              class="italic text-purple-400"
              type="button"
              onclick={() => {
                showDSQuotationModal = true
              }}
            >
              {$_("Sources")}: {quotes.length}
            </button>

            <DSQuotationsModal
              bind:open={showDSQuotationModal}
              {quotes}
              {dataSources}
              label={richField.label}
            />
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}
