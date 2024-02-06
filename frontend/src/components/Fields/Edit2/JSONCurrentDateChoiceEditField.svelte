<script lang="ts">
  // TODO WIP -> Is current radio or checkbox ?
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  export let value: JSONCurrentDateChoiceFieldType
  export let fieldname: string

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  const createEmptyEntry = (): JSONCurrentDateChoiceFieldType[number] => ({
    choice: null,
    date: null,
    current: false,
  })

  let valueCopy = structuredClone<JSONCurrentDateChoiceFieldType>(
    value.length ? value : [createEmptyEntry()],
  )
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1

  $: value = valueCopy.filter(val => !!val.choice)

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  const removeEntry = (index: number) => {
    if (valueCopy[index].current) current = -1
    valueCopy = valueCopy.filter((_val, i) => i !== index)
  }
  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
  }
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class="flex flex-col gap-4 border p-3">
      <label class="flex flex-wrap items-center justify-between gap-4" for={undefined}>
        {$_("Choice")}
        <ChoicesEditField
          bind:value={val.choice}
          extras={{
            choices: extras.choices,
            required: !!val.date,
          }}
          fieldname="{fieldname}_{i}_choice"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Date")}
        <LowLevelDateYearField
          bind:value={val.date}
          name="{fieldname}_{i}_date"
          class="w-36"
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
          disabled={!val.choice}
          on:change={() => updateCurrent(i)}
          class:ring-2={value.length > 0 && current < 0}
          value={i}
        />
      </label>

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
