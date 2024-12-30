<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import type { components } from "$lib/openAPI"
  import { fieldChoices } from "$lib/stores"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: components["schemas"]["CarbonSequestrationItem"][]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const emptyEntry: components["schemas"]["CarbonSequestrationItem"] = {
    current: false,
    start_date: null,
    end_date: null,
    area: null,
    choices: [],
    projected_lifetime_sequestration: null,
    projected_annual_sequestration: null,
    project_proponents: "",
    certification_standard: null,
    certification_standard_name: [],
    certification_standard_id: "",
    certification_standard_comment: "",
  }

  const isEmpty = (val: components["schemas"]["CarbonSequestrationItem"]) =>
    JSON.stringify(val) === JSON.stringify(emptyEntry)

  let valueCopy: components["schemas"]["CarbonSequestrationItem"][] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )

  const updateVal = () => {
    value = valueCopy.filter(val => val.choices && val.choices.length > 0)
  }

  const addEntry = () => {
    valueCopy = [...valueCopy, structuredClone(emptyEntry)]
    updateVal()
  }

  const removeEntry = (index: number) => {
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    updateVal()
  }

  let isCurrentRequired = $derived(
    value.length ? !value.some(val => val.current) : false,
  )
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
            required: !isEmpty(val),
          }}
          fieldname="{fieldname}_{i}_choices"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit="ha"
          name="{fieldname}_{i}_area"
          class="w-24 grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Estimated emission reduction/removal during project lifetime")}
        <LowLevelDecimalField
          bind:value={val.projected_lifetime_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Estimated annual emission reduction/removal")}
        <LowLevelDecimalField
          bind:value={val.projected_annual_sequestration}
          unit={$_("tCO2e")}
          name="{fieldname}_{i}_area"
          class="w-24 max-w-[8rem] grow"
          onchange={updateVal}
        />
      </label>
      <label class={labelClass}>
        {$_("Project proponents")}
        <input
          bind:value={val.project_proponents}
          type="text"
          class="inpt"
          placeholder={$_("Project proponents")}
          oninput={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Certification standard/mechanism")}
        <LowLevelNullBooleanField
          bind:value={val.certification_standard}
          nullable
          fieldname="certification_standard"
          wrapperClass="flex justify-end gap-3"
          onchange={() => {
            val.certification_standard_name = []
            val.certification_standard_id = ""
            updateVal()
          }}
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
                multipleChoices: true,
              }}
              fieldname="{fieldname}_{i}_certification_standard_name"
            />
          </label>
          <label class={labelClass}>
            {$_("ID of certification standard/mechanism")}
            <input
              bind:value={val.certification_standard_id}
              type="text"
              class="inpt"
              placeholder={$_("ID of certification standard/mechanism")}
            />
          </label>
        </div>
      {/if}

      <label class={labelClass}>
        {$_("Comment on certification standard / mechanism")}
        <input
          bind:value={val.certification_standard_comment}
          type="text"
          class="inpt"
          placeholder={$_("Comment on certification standard / mechanism")}
          oninput={updateVal}
        />
      </label>

      <Date
        bind:value={val.start_date}
        name="{fieldname}_{i}_date"
        label={$_("Start date")}
        onchange={updateVal}
      />
      <Date
        bind:value={val.end_date}
        name="{fieldname}_{i}_date"
        label={$_("End date")}
        onchange={updateVal}
      />

      <CurrentCheckbox
        bind:checked={val.current}
        name="{fieldname}_{i}_current"
        required={isCurrentRequired}
        onchange={updateVal}
      />

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
