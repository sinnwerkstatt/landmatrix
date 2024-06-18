<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/data"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentRadio from "$components/Fields/Edit2/JSONFieldComponents/CurrentRadio.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  export let value: JSONCurrentDateAreaFieldType[]
  export let fieldname: string

  let valueCopy = structuredClone<JSONCurrentDateAreaFieldType[]>(
    value.length ? value : [{ current: false, date: null, area: null }],
  )
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1

  $: value = valueCopy.filter(val => !!val.area)

  const addEntry = () =>
    (valueCopy = [...valueCopy, { current: false, date: null, area: null }])

  const removeEntry = (index: number) => {
    if (valueCopy[index].current) current = -1
    valueCopy = valueCopy.filter((_val, i) => i !== index)
  }

  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
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
          required={!!(val.current || val.date)}
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" />

      <CurrentRadio
        bind:group={current}
        name="{fieldname}_current"
        required={valueCopy.length > 0 && current < 0}
        disabled={!val.area}
        value={i}
        on:change={() => updateCurrent(i)}
      />

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
