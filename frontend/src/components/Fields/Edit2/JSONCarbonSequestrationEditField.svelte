<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import { slide } from "svelte/transition"

  import { fieldChoices } from "$lib/stores"
  import type { JSONCarbonSequestrationFieldType } from "$lib/types/newtypes"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import LowLevelNullBooleanField from "$components/Fields/Edit/LowLevelNullBooleanField.svelte"
  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  export let fieldname: string
  export let value: JSONCarbonSequestrationFieldType[] = []

  const CARBON_SEQUESTRATION_CERT_ITEMS = [
    { value: "REDD", label: $_("REDD+") },
    { value: "VCS", label: $_("Verified Carbon Standard (VCS)") },
    { value: "GOLD", label: $_("Gold Standard for the Global Goals (GOLD)") },
    { value: "CDM", label: $_("Clean Development Mechanism (CDM)") },
    { value: "CAR", label: $_("Climate Action Reserve (CAR)") },
    { value: "VIVO", label: $_("Plan Vivo") },
    { value: "OTHER", label: $_("Other (please specify in a comment)") },
  ]

  let valueCopy: JSONCarbonSequestrationFieldType[] = structuredClone(
    value.length
      ? value
      : [
          {
            current: false,
            date: null,
            area: null,
            choices: [],
            projected_lifetime_sequestration: null,
            projected_annual_sequestration: null,
            certification_standard: null,
            certification_standard_name: "",
            certification_standard_comment: "",
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
        projected_lifetime_sequestration: null,
        projected_annual_sequestration: null,
        certification_standard: null,
        certification_standard_name: "",
        certification_standard_comment: "",
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
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Choices")}
        <ChoicesEditField
          bind:value={val.choices}
          extras={{
            choices: $fieldChoices.deal.carbon_sequestration,
            required: !!(val.date || val.area),
          }}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Projected carbon sequestration during project lifetime")}
        <LowLevelDecimalField
          bind:value={val.projected_lifetime_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Projected annual carbon sequestration")}
        <LowLevelDecimalField
          bind:value={val.projected_annual_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Certification standard/mechanism")}
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
          {$_("Name of certification standard/mechanism")}
          <Select
            value={CARBON_SEQUESTRATION_CERT_ITEMS.find(
              i => i.value === val.certification_standard_name,
            )}
            items={CARBON_SEQUESTRATION_CERT_ITEMS}
            on:change={e => (val.certification_standard_name = e.detail.value)}
            on:clear={() => (val.certification_standard_name = null)}
            showChevron
            placeholder={$_("Name of certification standard/mechanism")}
          />
        </label>
      {/if}
      <label class="flex flex-wrap items-center justify-between gap-2" for={undefined}>
        {$_("Comment on certtification standard/mechanism")}
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
