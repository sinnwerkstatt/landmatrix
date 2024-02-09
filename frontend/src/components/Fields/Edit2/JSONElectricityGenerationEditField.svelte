<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { fieldChoices } from "$lib/stores.js"
  import type { JSONElectricityGenerationFieldType } from "$lib/types/newtypes"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  export let value: JSONElectricityGenerationFieldType[]
  export let fieldname: string

  const createEmptyEntry = (): JSONElectricityGenerationFieldType => ({
    current: false,
    date: null,
    area: null,
    choices: [],
    export: null,
    windfarm_count: null,
    current_capacity: null,
    intended_capacity: null,
  })

  let valueCopy: JSONElectricityGenerationFieldType[] = structuredClone(
    value.length ? value : [createEmptyEntry()],
  )

  $: value = valueCopy.filter(val => val.choices.length > 0)

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  const removeEntry = (index: number) =>
    (valueCopy = valueCopy.filter((_val, i) => i !== index))

  $: isCurrentRequired = value.length ? !value.some(val => val.current) : false
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Choices")}
        <ChoicesEditField
          bind:value={val.choices}
          extras={{
            choices: $fieldChoices.deal.electricity_generation,
            multipleChoices: true,
            required: !!(val.date || val.area),
          }}
          fieldname="{fieldname}_{i}_choices"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area covered by installations")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[9rem] grow"
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
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Intended capacity")}
        <LowLevelDecimalField
          bind:value={val.intended_capacity}
          unit={$_("MW")}
          name="{fieldname}_{i}_intended_capacity"
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
