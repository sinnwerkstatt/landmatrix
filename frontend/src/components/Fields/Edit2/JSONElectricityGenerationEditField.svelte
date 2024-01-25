<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { fieldChoices } from "$lib/stores.js"
  import type { JSONElectricityGenerationFieldType } from "$lib/types/newtypes"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import ChoicesField from "$components/Fields/Edit2/ChoicesField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  export let fieldname: string
  export let value: JSONElectricityGenerationFieldType[] = []

  let valueCopy: JSONElectricityGenerationFieldType[] = structuredClone(
    value.length
      ? value
      : [
          {
            current: false,
            date: null,
            area: null,
            choices: [],
            export: null,
            windfarm_count: null,
            current_capacity: null,
            intended_capacity: null,
          },
        ],
  )
  $: value = valueCopy.filter(val => val.choices.length > 0)

  function addEntry() {
    valueCopy = [
      ...valueCopy,
      {
        current: false,
        date: null,
        area: null,
        choices: [],
        export: null,
        windfarm_count: null,
        current_capacity: null,
        intended_capacity: null,
      },
    ]
  }

  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }

  const anySelectedAsCurrent = values => values.some(val => val.current)
  const isCurrentRequired = values => values.length > 0 && !anySelectedAsCurrent(values)
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-orange={val.current} class="flex flex-col gap-4 border p-3">
      <label class="flex items-center justify-between gap-2">
        {$_("Current")}
        <input
          type="checkbox"
          bind:checked={val.current}
          name="{fieldname}_{i}_current"
          required={isCurrentRequired(valueCopy)}
          disabled={!val.choices || !val.choices.length}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Date")}
        <LowLevelDateYearField
          bind:value={val.date}
          name="{fieldname}_{i}_date"
          class="w-36"
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Area covered by installations")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Choices")}
        <ChoicesField
          bind:value={val.choices}
          extras={{
            choices: $fieldChoices.deal.electricity_generation,
            required: !!(val.date || val.area),
          }}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Export")}
        <LowLevelDecimalField
          bind:value={val.export}
          unit="%"
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>
      {#if val.choices?.find(v => v === "WIND")}
        <label
          class="flex flex-wrap items-center justify-between gap-2"
          for={undefined}
          transition:slide
        >
          {$_("Number of turbines")}

          <LowLevelDecimalField
            bind:value={val.windfarm_count}
            name="{fieldname}_{i}_windfarm_count"
            class="w-12 max-w-[6rem] grow"
            decimals={0}
          />
        </label>
      {/if}

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Currently installed capacity")}
        <LowLevelDecimalField
          bind:value={val.current_capacity}
          unit={$_("MW")}
          name="{fieldname}_{i}_current_capacity"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Intended capacity")}
        <LowLevelDecimalField
          bind:value={val.intended_capacity}
          unit={$_("MW")}
          name="{fieldname}_{i}_intended_capacity"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <div class="text-right">
        <button
          type="button"
          disabled={valueCopy.length <= 1}
          on:click={() => removeEntry(i)}
        >
          <MinusIcon
            class="h-5 w-5 {valueCopy.length > 1 ? 'text-red-600' : 'text-gray-200'}"
          />
        </button>
      </div>
    </div>
  {/each}

  <button
    type="button"
    on:click={addEntry}
    class="flex w-full items-center justify-center border p-2"
  >
    <PlusIcon class="h-7 w-7 text-black" />
  </button>
</div>
