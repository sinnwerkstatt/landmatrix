<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/data"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  interface Extras {
    choices: ValueLabelEntry[]
  }

  interface Props {
    value: JSONCurrentDateChoiceFieldType[]
    fieldname: string
    extras?: Extras
  }

  let { value = $bindable(), fieldname, extras = { choices: [] } }: Props = $props()

  const emptyEntry: JSONCurrentDateChoiceFieldType = {
    choice: null,
    date: null,
    current: false,
  }

  let valueCopy: JSONCurrentDateChoiceFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  const updateVal = () => {
    value = valueCopy.filter(val => !!val.choice)
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

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choice")}
        <ChoicesEditField
          bind:value={val.choice}
          extras={{ choices: extras.choices, required: !!val.date }}
          fieldname="{fieldname}_{i}_choice"
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
          disabled={!val.choice}
          value={i}
          onchange={() => updateCurrent(i)}
        />
      </label>

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
