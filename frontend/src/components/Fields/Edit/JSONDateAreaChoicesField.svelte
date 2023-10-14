<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"
  import TypedChoicesField from "./TypedChoicesField.svelte"

  interface JSONDateAreaChoicesField {
    date?: string
    area?: number
    choices?: string[]
    current?: boolean
  }

  export let formfield: FormField
  export let value: Array<JSONDateAreaChoicesField> | null

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

<table class="w-full">
  <thead>
    <tr>
      <th class="pr-2 text-center font-normal">{$_("Current")}</th>
      <th class="font-normal">{$_("Date")}</th>
      <th class="font-normal">{$_("Area (ha)")}</th>
      <th class="font-normal">{$_("Choices")}</th>
      <th />
    </tr>
  </thead>
  <tbody>
    {#each valueCopy as val, i}
      <tr class:is-current={val.current}>
        <td class="p-1 text-center">
          <input
            type="checkbox"
            bind:checked={val.current}
            name="{formfield.name}_{i}_current"
            required={isCurrentRequired(valueCopy)}
            disabled={!val.choices}
          />
        </td>

        <td class="w-1/4 p-1">
          <LowLevelDateYearField
            bind:value={val.date}
            name="{formfield.name}_{i}_date"
          />
        </td>

        <td class="w-1/4 p-1">
          <LowLevelDecimalField
            bind:value={val.area}
            unit="ha"
            name="{formfield.name}_{i}_area"
          />
        </td>
        <td class="w-2/4">
          <TypedChoicesField
            bind:value={val.choices}
            formfield={{ ...formfield, name: `${formfield.name}_${i}_choices` }}
            required={!!(val.date || val.area)}
          />
        </td>
        <td class="p-1">
          <button type="button" on:click={addEntry}>
            <PlusIcon class="h-5 w-5 text-black" />
          </button>
          <button
            type="button"
            disabled={valueCopy.length <= 1}
            on:click={() => removeEntry(i)}
          >
            <MinusIcon class="h-5 w-5 text-red-600" />
          </button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
