<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  interface JSONJobsField {
    current: boolean | null
    date: string | null
    jobs: number | null
    employees: number | null
    workers: number | null
  }

  export let fieldname: string
  export let value: JSONJobsField[] = []

  let valueCopy: JSONJobsField[] = structuredClone(
    value.length
      ? value
      : [{ current: false, date: null, jobs: null, employees: null, workers: null }],
  )
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1
  $: value = valueCopy.filter(val => !!(val.jobs || val.employees || val.workers))

  function updateCurrent(index: number) {
    valueCopy = valueCopy.map(val => ({ ...val, current: null }))
    valueCopy[index].current = true
    valueCopy = valueCopy
  }
  function addEntry() {
    valueCopy = [
      ...valueCopy,
      { current: false, date: null, jobs: null, employees: null, workers: null },
    ]
  }
  function removeEntry(index: number) {
    if (current === index) {
      current = -1
    } else if (current > index) {
      current--
    }
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }
</script>

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
        <td class="p-1 text-center">
          <input
            type="radio"
            bind:group={current}
            name="{fieldname}_current"
            required={valueCopy.length > 0}
            on:change={() => updateCurrent(i)}
            disabled={!val.jobs && !val.employees && !val.workers}
            value={i}
          />
        </td>

        <td class="w-1/4 p-1">
          <LowLevelDateYearField bind:value={val.date} name="{fieldname}_{i}_date" />
        </td>

        <td class="w-1/4 p-1">
          <LowLevelDecimalField
            bind:value={val.jobs}
            required={!!val.date && !(val.employees || val.workers)}
            name="{fieldname}_{i}_jobs"
            decimals={0}
            unit=""
          />
        </td>
        <td class="w-1/4 p-1">
          <LowLevelDecimalField
            bind:value={val.employees}
            required={!!val.date && !(val.workers || val.jobs)}
            name="{fieldname}_{i}_employees"
            decimals={0}
            unit=""
          />
        </td>
        <td class="w-1/4 p-1">
          <LowLevelDecimalField
            bind:value={val.workers}
            required={!!val.date && !(val.jobs || val.employees)}
            name="{fieldname}_{i}_workers"
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
