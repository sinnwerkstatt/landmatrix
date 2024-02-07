<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type ValueLabelEntry } from "$lib/stores"
  import type { JSONExportsFieldType } from "$lib/types/newtypes"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  export let value: JSONExportsFieldType[] = []
  export let fieldname: string

  export let extras: { choices: ValueLabelEntry[] } = { choices: [] }

  const createEmptyEntry = (): JSONExportsFieldType => ({
    current: false,
    date: null,
    choices: [],
    area: null,
    yield: null,
    export: null,
  })

  let valueCopy = structuredClone<JSONExportsFieldType[]>(
    value.length ? value : [createEmptyEntry()],
  )

  $: value = valueCopy.filter(val => val.choices.length > 0)

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  function removeEntry(index: number) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }

  $: isCurrentRequired = value.length ? !value.some(val => val.current) : false
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choices")}
        <ChoicesEditField
          bind:value={val.choices}
          {extras}
          fieldname="{fieldname}_{i}_choices"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          name="{fieldname}_{i}_area"
          unit="ha"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Yield")}
        <LowLevelDecimalField
          bind:value={val.yield}
          unit="tons"
          name="{fieldname}_{i}_yield"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Export")}
        <LowLevelDecimalField
          bind:value={val.export}
          name="{fieldname}_{i}_export"
          unit="%"
          max={100}
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" />

      <CurrentCheckbox
        bind:checked={val.current}
        name="{fieldname}_{i}_current"
        required={isCurrentRequired}
        disabled={!val.choices || !val.choices.length}
      />

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
