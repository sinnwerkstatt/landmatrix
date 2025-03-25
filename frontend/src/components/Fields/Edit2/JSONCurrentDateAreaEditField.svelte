<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import type {
    JSONCurrentDateAreaFieldType,
    JSONFieldQuotations,
    QuotationItem,
  } from "$lib/types/data"

  import { getMutableObject } from "$components/Data/stores"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import SourcesEditButton from "$components/Quotations/SourcesEditButton.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: JSONCurrentDateAreaFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const mutableObj = getMutableObject("deal")

  const emptyEntry: JSONCurrentDateAreaFieldType = {
    current: false,
    date: null,
    area: null,
  }

  let valueCopy: JSONCurrentDateAreaFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  const isEmpty = (val: JSONCurrentDateAreaFieldType) => !val.area
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
    if (valueCopy[index].current) current = -1

    valueCopy = valueCopy.filter((_val, i) => i !== index)
    jsonQuotes = jsonQuotes.filter((_val, i) => i !== index)
    updateVal()
  }

  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
    updateVal()
  }

  const getQuotes = (i: number) => () => jsonQuotes[i] ?? []
  const setQuotes = (i: number) => (quotes: QuotationItem[]) => {
    jsonQuotes[i] = quotes
    updateVal()
  }
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <!-- todo marcus: area is string? -->
        <LowLevelDecimalField
          bind:value={val.area}
          unit={$_("ha")}
          name="{fieldname}_{i}_area"
          class="w-36"
          required={!!(val.current || val.date)}
          onchange={updateVal}
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" onchange={updateVal} />

      <label class={labelClass}>
        {$_("Current")}
        <input
          type="radio"
          class={twMerge(
            "size-5 accent-violet-400 ",
            valueCopy.length > 0 && current < 0 ? "ring-2 ring-red-600" : "",
          )}
          bind:group={current}
          name="{fieldname}_current"
          required={valueCopy.length > 0 && current < 0}
          disabled={!val.area}
          value={i}
          onchange={() => updateCurrent(i)}
        />
      </label>

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
