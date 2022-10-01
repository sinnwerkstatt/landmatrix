<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import TypedChoiceField from "./TypedChoiceField.svelte"

  interface JSONDateChoiceField {
    date?: string
    choice?: string
    current?: boolean
  }

  export let formfield: FormField
  export let value: Array<JSONDateChoiceField> | null

  let valueCopy = createValueCopy(value)
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1
  $: value = syncValue(val => !!(val.date || val.choice), valueCopy)

  function updateCurrent(index) {
    valueCopy = valueCopy.map(val => ({ ...val, current: undefined }))
    valueCopy[index].current = true
    valueCopy = valueCopy
  }
  function addEntry() {
    valueCopy = [...valueCopy, {}]
  }
  function removeEntry(index) {
    if (current === index) {
      current = -1
    } else if (current > index) {
      current--
    }
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }
</script>

<div class="json_date_choice_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th class="font-normal">{$_("Current")}</th>
        <th class="font-normal">{$_("Date")}</th>
        <th class="font-normal">{$_("Choice")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="p-1 text-center" on:click={() => updateCurrent(i)}>
            <input
              type="radio"
              bind:group={current}
              name="{formfield.name}_current"
              required={valueCopy.length > 0}
              disabled={!val.date && !val.choices}
              value={i}
            />
          </td>
          <td class="w-36 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={val.choice}
              name={formfield.name}
            />
          </td>
          <td class="w-2/3 p-1">
            <TypedChoiceField bind:value={val.choice} {formfield} required={val.date} />
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
</div>
