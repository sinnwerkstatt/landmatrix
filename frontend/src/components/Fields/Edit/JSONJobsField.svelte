<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"

  interface JSONJobsField {
    date?: string
    jobs?: string
    employees?: string
    workers?: string
    current?: boolean
  }

  export let formfield: FormField
  export let value: Array<JSONJobsField> | null

  let valueCopy = createValueCopy(value)
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1
  $: value = syncValue(val => !!(val.jobs || val.employees || val.workers), valueCopy)

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

<div class="json_date_area_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th class="pr-2 text-center font-normal">{$_("Current")}</th>
        <th class="font-normal">{$_("Date")}</th>
        <th class="font-normal">{$_("Jobs")}</th>
        <th class="font-normal">{$_("Employees")}</th>
        <th class="font-normal">{$_("Workers")}</th>
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
              disabled={!val.jobs && !val.employees && !val.workers}
              value={i}
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
              bind:value={val.jobs}
              required={val.date && !(val.employees || val.workers)}
              name="{formfield.name}_{i}_jobs"
              decimals={0}
              unit=""
            />
          </td>
          <td class="w-1/4 p-1">
            <LowLevelDecimalField
              bind:value={val.employees}
              required={val.date && !(val.workers || val.jobs)}
              name="{formfield.name}_{i}_employees"
              decimals={0}
              unit=""
            />
          </td>
          <td class="w-1/4 p-1">
            <LowLevelDecimalField
              bind:value={val.workers}
              required={val.date && !(val.jobs || val.employees)}
              name="{formfield.name}_{i}_workers"
              decimals={0}
              unit=""
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
</div>
