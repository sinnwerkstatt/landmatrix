<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { fieldChoices } from "$lib/stores"
  import type { JSONCarbonSequestrationFieldType } from "$lib/types/newtypes"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  export let value: JSONCarbonSequestrationFieldType[]
  export let fieldname: string

  const createEmptyEntry = (): JSONCarbonSequestrationFieldType => ({
    current: false,
    date: null,
    area: null,
    choices: [],
    projected_lifetime_sequestration: null,
    projected_annual_sequestration: null,
    certification_standard: null,
    certification_standard_name: null,
    certification_standard_id: "",
    certification_standard_comment: "",
  })

  let valueCopy = structuredClone<JSONCarbonSequestrationFieldType[]>(
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
            choices: $fieldChoices.deal.carbon_sequestration,
            multipleChoices: true,
            required: !!(val.date || val.area),
          }}
          fieldname="{fieldname}_{i}_choices"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 grow"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Projected carbon sequestration during project lifetime")}
        <LowLevelDecimalField
          bind:value={val.projected_lifetime_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Projected annual carbon sequestration")}
        <LowLevelDecimalField
          bind:value={val.projected_annual_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Certification standard/mechanism")}
        <LowLevelNullBooleanField
          bind:value={val.certification_standard}
          nullable
          fieldname="certification_standard"
          wrapperClass="flex justify-end gap-3"
          on:change={() => (val.certification_standard_name = null)}
        />
      </label>
      {#if val.certification_standard === true}
        <div transition:slide class="flex flex-col gap-4 pl-4">
          <label class={labelClass} for={undefined}>
            {$_("Name of certification standard/mechanism")}
            <ChoicesEditField
              bind:value={val.certification_standard_name}
              extras={{
                choices: $fieldChoices.deal.carbon_sequestration_certs,
                placeholder: $_("Name of certification standard/mechanism"),
                closeListOnChange: true,
                otherHint: $_("Please specify in comment field"),
                required: true,
              }}
              fieldname="{fieldname}_{i}_certification_standard_name"
            />
          </label>
          <label class={labelClass} for={undefined}>
            {$_("ID of certification standard / mechanism")}
            <input
              bind:value={val.certification_standard_id}
              type="text"
              class="inpt"
              placeholder={$_("ID of certification standard / mechanism")}
            />
          </label>
        </div>
      {/if}

      <label class={labelClass} for={undefined}>
        {$_("Comment on certtification standard/mechanism")}
        <input
          bind:value={val.certification_standard_comment}
          type="text"
          class="inpt"
          placeholder={$_("Comment on certification standard")}
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
