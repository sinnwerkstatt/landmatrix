<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONJobsFieldType } from "$lib/types/newtypes"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import CurrentRadio from "$components/Fields/Edit2/JSONFieldComponents/CurrentRadio.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  export let value: JSONJobsFieldType[]
  export let fieldname: string

  const createEmptyEntry = (): JSONJobsFieldType => ({
    current: false,
    date: null,
    jobs: null,
    employees: null,
    workers: null,
  })

  let valueCopy = structuredClone<JSONJobsFieldType[]>(
    value.length ? value : [createEmptyEntry()],
  )
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1

  $: value = valueCopy.filter(val => !!(val.jobs || val.employees || val.workers))

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  const removeEntry = (index: number) => {
    if (valueCopy[index].current) current = -1
    valueCopy = valueCopy.filter((_val, i) => i !== index)
  }

  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
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
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" />

      <CurrentRadio
        bind:group={current}
        name="{fieldname}_current"
        required={value.length > 0 && current < 0}
        disabled={!val.jobs && !val.employees && !val.workers}
        value={i}
        on:change={() => updateCurrent(i)}
      />

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
