<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/data"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: JSONCurrentDateAreaFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const emptyEntry: JSONCurrentDateAreaFieldType = {
    current: false,
    date: null,
    area: null,
  }

  let valueCopy: JSONCurrentDateAreaFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  let updateVal = () => {
    value = valueCopy.filter(val => !!val.area)
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

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
