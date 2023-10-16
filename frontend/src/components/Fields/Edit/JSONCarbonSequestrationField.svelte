<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"
  import TypedChoicesField from "./TypedChoicesField.svelte"
  import LowLevelNullBooleanField from "$components/Fields/Edit/LowLevelNullBooleanField.svelte"
  import { slide } from "svelte/transition"

  interface JSONCarbonSequestrationField {
    current?: boolean
    date?: string
    area?: number
    choices?: string[]
    projected_lifetime_sequestration?: number
    projected_annual_sequestration?: number
    certification_standard: boolean | null
    certification_standard_name: string
    certification_standard_comment: string
  }

  export let formfield: FormField
  export let value: JSONCarbonSequestrationField[] | null

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
    <div class:border-lm-orange={val.current} class="flex  flex-col gap-4 border p-3">
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
        {$_("Projected carbon sequestration during project lifetime")}
        <LowLevelDecimalField
          bind:value={val.projected_lifetime_sequestration}
          unit={$_("tCO2e")}
          name="{formfield.name}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Projected annual carbon sequestration")}
        <LowLevelDecimalField
          bind:value={val.projected_annual_sequestration}
          unit={$_("tCO2e")}
          name="{formfield.name}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Certification standard")}

        <LowLevelNullBooleanField
          bind:value={val.certification_standard}
          nullable
          fieldname="certification_standard"
          wrapperClass="space-x-3"
        />
      </label>
      {#if val.certification_standard === true}
        <label
          class="flex flex-wrap items-center justify-between gap-2"
          for={undefined}
          transition:slide
        >
          {$_("Name of certification standard")}
          <input
            bind:value={val.certification_standard_name}
            type="text"
            class="inpt"
            placeholder={$_("Name")}
          />
        </label>
      {/if}
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Comment on certification standard")}
        <input
          bind:value={val.certification_standard_comment}
          type="text"
          class="inpt"
          placeholder={$_("Comment on certification standard")}
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
    class="flex w-full items-center justify-center border p-2"
    on:click={addEntry}
    type="button"
  >
    <PlusIcon class="h-7 w-7 text-black" />
  </button>
</div>
