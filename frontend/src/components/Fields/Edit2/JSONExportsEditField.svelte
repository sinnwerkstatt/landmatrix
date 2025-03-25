<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/fieldChoices"
  import type {
    JSONExportsFieldType,
    JSONFieldQuotations,
    QuotationItem,
  } from "$lib/types/data"

  import { getMutableObject } from "$components/Data/stores"
  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import SourcesEditButton from "$components/Quotations/SourcesEditButton.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value?: JSONExportsFieldType[]
    fieldname: string
    extras?: { choices: ValueLabelEntry[] }
  }

  let { value = $bindable([]), fieldname, extras = { choices: [] } }: Props = $props()

  const mutableObj = getMutableObject("deal")

  const emptyEntry: JSONExportsFieldType = {
    current: false,
    date: null,
    choices: [],
    area: null,
    yield: null,
    export: null,
  }

  let valueCopy: JSONExportsFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )

  const isEmpty = (val: JSONExportsFieldType) => !val.choices.length
  const getJsonQuotes = () =>
    ($mutableObj.selected_version.ds_quotations[fieldname] ??
      new Array(value.length || 1).fill([])) as JSONFieldQuotations

  let jsonQuotes = $state(getJsonQuotes())

  const updateVal = () => {
    const keep = valueCopy.map(val => !isEmpty(val))

    value = valueCopy.filter((_, i) => keep[i])
    const filteredQuotes = jsonQuotes.filter((_, i) => keep[i])

    if (filteredQuotes.some(q => q.length)) {
      $mutableObj.selected_version.ds_quotations[fieldname] = filteredQuotes
    } else {
      const { [fieldname]: _ignore, ...rest } =
        $mutableObj.selected_version.ds_quotations ?? {}
      $mutableObj.selected_version.ds_quotations = { ...rest }
    }
  }

  const addEntry = () => {
    jsonQuotes = [...jsonQuotes, []]
    valueCopy = [...valueCopy, structuredClone(emptyEntry)]
    updateVal()
  }

  const removeEntry = (index: number) => {
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    jsonQuotes = jsonQuotes.filter((_val, i) => i !== index)
    updateVal()
  }

  let isCurrentRequired = $derived(
    value.length ? !value.some(val => val.current) : false,
  )

  const getQuotes = (i: number) => () => jsonQuotes[i] ?? []
  const setQuotes = (i: number) => (quotes: QuotationItem[]) => {
    jsonQuotes[i] = quotes
    updateVal()
  }
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choices")}
        <ChoicesEditField
          bind:value={val.choices}
          {extras}
          fieldname="{fieldname}_{i}_choices"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          name="{fieldname}_{i}_area"
          unit="ha"
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Yield")}
        <LowLevelDecimalField
          bind:value={val.yield}
          unit="tons"
          name="{fieldname}_{i}_yield"
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Export")}
        <LowLevelDecimalField
          bind:value={val.export}
          name="{fieldname}_{i}_export"
          unit="%"
          max={100}
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" onchange={updateVal} />

      <CurrentCheckbox
        bind:checked={val.current}
        name="{fieldname}_{i}_current"
        required={isCurrentRequired}
        disabled={!val.choices || !val.choices.length}
        onchange={updateVal}
      />

      <div class="mt-2 flex justify-between">
        <SourcesEditButton
          fieldname="{fieldname}-{i}"
          bind:quotes={getQuotes(i), setQuotes(i)}
          dataSources={$mutableObj.selected_version.datasources}
          disabled={isEmpty(val)}
        />
        <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
      </div>
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
