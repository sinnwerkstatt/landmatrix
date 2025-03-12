<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"
  import type { Model } from "$lib/types/data"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

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
</script>

{#if isNotEmpty(value)}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if showLabel}
      <Label2
        value={richField?.label}
        class={labelClass}
        contextHelp={richField.displayContextHelp}
      />
    {/if}

    <div class={valueClass}>
      <div class="flex">
        {#if richField && richField.displayField}
          {@const RichDisplayField = richField.displayField}

          <RichDisplayField {value} {fieldname} extras={allExtras} />
        {:else}
          <div class="italic text-red-400">unknown field: {fieldname}</div>
        {/if}

        <SourcesDisplayButton {model} path={[fieldname]} />
      </div>
    </div>
  </div>
{/if}
