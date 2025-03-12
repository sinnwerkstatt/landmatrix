<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { dealChoices } from "$lib/fieldChoices"
  import type {
    JSONElectricityGenerationFieldType,
    JSONFieldQuotations,
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
    value: JSONElectricityGenerationFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const mutableObj = getMutableObject("deal")

  const emptyEntry: JSONElectricityGenerationFieldType = {
    current: false,
    date: null,
    area: null,
    choices: [],
    export: null,
    windfarm_count: null,
    current_capacity: null,
    intended_capacity: null,
  }

  let valueCopy: JSONElectricityGenerationFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )

  const isEmpty = (val: JSONElectricityGenerationFieldType) => !val.choices.length
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
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    jsonQuotes = jsonQuotes.filter((_val, i) => i !== index)
    updateVal()
  }

  let isCurrentRequired = $derived(
    value.length ? !value.some(val => val.current) : false,
  )
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choices")}
        <ChoicesEditField
          bind:value={val.choices}
          extras={{
            choices: $dealChoices.electricity_generation,
            multipleChoices: true,
            required: !!(val.date || val.area),
          }}
          fieldname="{fieldname}_{i}_choices"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area covered by installations")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[9rem] grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Export")}
        <LowLevelDecimalField
          bind:value={val.export}
          unit="%"
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
          max={100}
          onchange={updateVal}
        />
      </label>
      {#if val.choices?.find(v => v === "WIND")}
        <label class={labelClass} for={undefined} transition:slide>
          {$_("Number of turbines")}
          <LowLevelDecimalField
            bind:value={val.windfarm_count}
            name="{fieldname}_{i}_windfarm_count"
            class="w-12 max-w-[6rem] grow"
            decimals={0}
            onchange={updateVal}
          />
        </label>
      {/if}

      <label class={labelClass} for={undefined}>
        {$_("Currently installed capacity")}
        <LowLevelDecimalField
          bind:value={val.current_capacity}
          unit={$_("MW")}
          name="{fieldname}_{i}_current_capacity"
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Intended capacity")}
        <LowLevelDecimalField
          bind:value={val.intended_capacity}
          unit={$_("MW")}
          name="{fieldname}_{i}_intended_capacity"
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
