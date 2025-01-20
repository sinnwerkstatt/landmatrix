<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/fieldChoices"
  import type { JSONCurrentDateAreaChoicesFieldType } from "$lib/types/data"

  import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import CurrentCheckbox from "$components/Fields/Edit2/JSONFieldComponents/CurrentCheckbox.svelte"
  import Date from "$components/Fields/Edit2/JSONFieldComponents/Date.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: JSONCurrentDateAreaChoicesFieldType[]
    fieldname: string
    extras?: { choices: ValueLabelEntry[] }
  }

  let { value = $bindable(), fieldname, extras = { choices: [] } }: Props = $props()

  const emptyEntry: JSONCurrentDateAreaChoicesFieldType = {
    choices: [],
    date: null,
    area: null,
    current: false,
  }

  let valueCopy: JSONCurrentDateAreaChoicesFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )

  let updateVal = () => {
    value = valueCopy.filter(val => val.choices.length || !!val.area)
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
            choices: extras.choices,
            multipleChoices: true,
            required: !!(val.date || val.area),
          }}
          fieldname="{fieldname}_{i}_choices"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit={$_("ha")}
          name="{fieldname}_{i}_area"
          class="w-36"
          onchange={updateVal}
        />
      </label>

      <Date bind:value={val.date} name="{fieldname}_{i}_date" onchange={updateVal} />

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
