<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONFieldQuotations, JSONLeaseFieldType } from "$lib/types/data"

  import { getMutableObject } from "$components/Data/stores"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import HomeIcon from "$components/icons/HomeIcon.svelte"
  import UsersIcon from "$components/icons/UsersIcon.svelte"
  import SourcesEditButton from "$components/Quotations/SourcesEditButton.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: JSONLeaseFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const mutableObj = getMutableObject("deal")

  const emptyEntry: JSONLeaseFieldType = {
    current: false,
    date: null,
    area: null,
    farmers: null,
    households: null,
  }
  let valueCopy: JSONLeaseFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  const isEmpty = (val: JSONLeaseFieldType) =>
    !(val.area || val.farmers || val.households)
  const getJsonQuotes = () =>
    ($mutableObj.selected_version.ds_quotations[fieldname] ??
      new Array(value.length || 1).fill([])) as JSONFieldQuotations

  let jsonQuotes = $state(getJsonQuotes())

  const updateVal = () => {
    const keep = valueCopy.map(val => !isEmpty(val))

    value = valueCopy.filter((_, i) => keep[i])
    const filtered = jsonQuotes.filter((_, i) => keep[i])
    if (filtered.some(q => q.length)) {
      $mutableObj.selected_version.ds_quotations[fieldname] = filtered
    } else {
      delete $mutableObj.selected_version.ds_quotations[fieldname]
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
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit={$_("ha")}
          name="{fieldname}_{i}_area"
          class="w-36"
          required={!!(val.date && !(val.farmers || val.households))}
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Farmers")}
        <LowLevelDecimalField
          bind:value={val.farmers}
          unit={UsersIcon}
          name="{fieldname}_{i}_farmers"
          class="w-36"
          decimals={0}
          required={!!(val.date && !(val.households || val.area))}
          onchange={updateVal}
        />
      </label>
      <label class={labelClass} for={undefined}>
        {$_("Households")}
        <LowLevelDecimalField
          bind:value={val.households}
          unit={HomeIcon}
          name="{fieldname}_{i}_households"
          class="w-36"
          decimals={0}
          required={!!(val.date && !(val.area || val.farmers))}
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Date")}
        <LowLevelDateYearField
          bind:value={val.date}
          name="{fieldname}_{i}_date"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass}>
        {$_("Current")}
        <input
          type="radio"
          bind:group={current}
          name="{fieldname}_current"
          required={valueCopy.length > 0}
          class="h-5 w-5 accent-violet-400 ring-red-600"
          disabled={!val.area && !val.farmers && !val.households}
          onchange={() => updateCurrent(i)}
          class:ring-2={value.length > 0 && current < 0}
          value={i}
        />
      </label>

      <div class="mt-2 flex justify-between">
        <SourcesEditButton
          fieldname="{fieldname}-{i}"
          bind:quotes={jsonQuotes[i]}
          dataSources={$mutableObj.selected_version.datasources}
          disabled={isEmpty(val)}
        />
        <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
      </div>
    </div>
  {/each}
  <AddButton onclick={addEntry} />
</div>
