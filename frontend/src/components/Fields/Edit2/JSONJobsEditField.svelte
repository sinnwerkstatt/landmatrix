<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import type { JSONJobsFieldType } from "$lib/types/data"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  interface Props {
    value: JSONJobsFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const emptyEntry: JSONJobsFieldType = {
    current: false,
    date: null,
    jobs: null,
    employees: null,
    workers: null,
  }

  let valueCopy: JSONJobsFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  const updateVal = () => {
    value = valueCopy.filter(val => !!(val.jobs || val.employees || val.workers))
  }

  const addEntry = () => {
    valueCopy = [...valueCopy, structuredClone(emptyEntry)]
    updateVal()
  }

  const removeEntry = (index: number) => {
    if (valueCopy[index].current) current = -1
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    updateVal()
  }

  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
    updateVal()
  }
</script>

<div class="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Jobs")}
        <LowLevelDecimalField
          bind:value={val.jobs}
          required={!!val.date && !(val.employees || val.workers)}
          name="{fieldname}_{i}_jobs"
          decimals={0}
          class="w-36"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Employees")}
        <LowLevelDecimalField
          bind:value={val.employees}
          required={!!val.date && !(val.workers || val.jobs)}
          name="{fieldname}_{i}_employees"
          decimals={0}
          class="w-36"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Workers")}
        <LowLevelDecimalField
          bind:value={val.workers}
          required={!!val.date && !(val.jobs || val.employees)}
          name="{fieldname}_{i}_workers"
          decimals={0}
          class="w-36"
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
          disabled={!val.jobs && !val.employees && !val.workers}
          value={i}
          onchange={() => updateCurrent(i)}
        />
      </label>

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
