<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import CurrentRadio from "$components/Fields/Edit2/JSONFieldComponents/CurrentRadio.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  export let value: JSONCurrentDateChoiceFieldType[]
  export let fieldname: string

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  const createEmptyEntry = (): JSONCurrentDateChoiceFieldType => ({
    choice: null,
    date: null,
    current: false,
  })

  let valueCopy = structuredClone<JSONCurrentDateChoiceFieldType[]>(
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
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choice")}
        <ChoicesEditField
          bind:value={val.choice}
          extras={{ choices: extras.choices, required: !!val.date }}
          fieldname="{fieldname}_{i}_choice"
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" />

      <CurrentRadio
        bind:group={current}
        name="{fieldname}_current"
        required={value.length > 0 && current < 0}
        disabled={!val.choice}
        value={i}
        on:change={() => updateCurrent(i)}
      />

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
