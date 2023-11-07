<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"
  import TypedChoicesField from "./TypedChoicesField.svelte"

  interface JSONElectricityGenerationField {
    current?: boolean
    date?: string
    area?: number
    choices?: string[]
    export?: number
    windfarm_count?: number
    current_capacity?: number
    intended_capacity?: number
  }

  export let formfield: FormField
  export let value: JSONElectricityGenerationField[] | null

  let valueCopy = createValueCopy(value)
  $: value = syncValue(val => !!val.choices, valueCopy)

  function addEntry() {
    valueCopy = [...valueCopy, {}]
  }

  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }

  const anySelectedAsCurrent = values => values.some(val => val.current)
  const isCurrentRequired = values => values.length > 0 && !anySelectedAsCurrent(values)
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-lm-orange={val.current} class="flex flex-col gap-4 border p-3">
      <label class="flex items-center justify-between gap-2">
        {$_("Current")}
        <input
          type="checkbox"
          bind:checked={val.current}
          name="{formfield.name}_{i}_current"
          required={isCurrentRequired(valueCopy)}
          disabled={!val.choices}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Date")}
        <LowLevelDateYearField
          bind:value={val.date}
          name="{formfield.name}_{i}_date"
          class="w-36"
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Area covered by installations")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{formfield.name}_{i}_area"
          class="w-24 grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Choices")}
        <TypedChoicesField
          bind:value={val.choices}
          formfield={{ ...formfield, name: `${formfield.name}_${i}_choices` }}
          required={!!(val.date || val.area)}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Export")}
        <LowLevelDecimalField
          bind:value={val.export}
          unit="%"
          name="{formfield.name}_{i}_area"
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
            name="{formfield.name}_{i}_windfarm_count"
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
          name="{formfield.name}_{i}_current_capacity"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Intended capacity")}
        <LowLevelDecimalField
          bind:value={val.intended_capacity}
          unit={$_("MW")}
          name="{formfield.name}_{i}_intended_capacity"
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
