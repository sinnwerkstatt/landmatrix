<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"

  interface JSONLeaseField {
    date?: string
    area?: number
    farmers?: number
    households?: number
    current?: boolean
  }

  export let formfield: FormField
  export let value: Array<JSONLeaseField> | null

  let valueCopy = createValueCopy(value)
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1
  $: value = syncValue(val => !!(val.area || val.farmers || val.households), valueCopy)

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
        <th class="font-normal">{$_("Area (ha)")}</th>
        <th class="font-normal">{$_("Farmers")}</th>
        <th class="font-normal">{$_("Households")}</th>
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="text-center" on:click={() => updateCurrent(i)}>
            <input
              type="radio"
              bind:group={current}
              name="{formfield.name}_current"
              required={valueCopy.length > 0}
              disabled={!val.area && !val.farmers && !val.households}
              value={i}
            />
          </td>

          <td class="w-1/3 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              name="{formfield.name}_{i}_date"
            />
          </td>

          <td class="w-1/3 p-1">
            <LowLevelDecimalField
              bind:value={val.area}
              required={val.date && !(val.farmers || val.households)}
              unit="ha"
              name="{formfield.name}_{i}_area"
            />
          </td>
          <td class="w-1/3 p-1">
            <LowLevelDecimalField
              bind:value={val.farmers}
              required={val.date && !(val.households || val.area)}
              decimals={0}
              min={0}
              name="{formfield.name}_{i}_farmers"
            />
          </td>
          <td class="w-1/3 p-1">
            <LowLevelDecimalField
              bind:value={val.households}
              required={val.date && !(val.area || val.farmers)}
              decimals={0}
              min={0}
              name="{formfield.name}_{i}_households"
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
