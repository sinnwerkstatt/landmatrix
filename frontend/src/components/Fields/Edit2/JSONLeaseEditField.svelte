<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import HomeIcon from "$components/icons/HomeIcon.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import UsersIcon from "$components/icons/UsersIcon.svelte"

  interface JSONLeaseField {
    current: boolean | null
    date: string | null
    area: number | null
    farmers: number | null
    households: number | null
  }

  export let value: JSONLeaseField[] = []

  export let fieldname: string

  let valueCopy: JSONLeaseField[] = structuredClone(
    value.length
      ? value
      : [{ current: false, date: null, area: null, farmers: null, households: null }],
  )
  let current = valueCopy.map(val => val.current).indexOf(true) ?? -1
  $: value = valueCopy.filter(val => !!(val.area || val.farmers || val.households))

  function updateCurrent(index: number) {
    valueCopy = valueCopy.map(val => ({ ...val, current: null }))
    valueCopy[index].current = true
    valueCopy = valueCopy
  }

  function addEntry() {
    valueCopy = [
      ...valueCopy,
      { current: false, date: null, area: null, farmers: null, households: null },
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
      <th class="font-normal">{$_("Area (ha)")}</th>
      <th class="font-normal">{$_("Farmers")}</th>
      <th class="font-normal">{$_("Households")}</th>
    </tr>
  </thead>
  <tbody>
    {#each valueCopy as val, i}
      <tr class:is-current={val.current}>
        <td class="text-center">
          <input
            type="radio"
            bind:group={current}
            name="{fieldname}_current"
            required={valueCopy.length > 0}
            on:change={() => updateCurrent(i)}
            disabled={!val.area && !val.farmers && !val.households}
            value={i}
          />
        </td>

        <td class="w-1/3 p-1">
          <LowLevelDateYearField bind:value={val.date} name="{fieldname}_{i}_date" />
        </td>

        <td class="w-1/3 p-1">
          <LowLevelDecimalField
            bind:value={val.area}
            required={!!(val.date && !(val.farmers || val.households))}
            unit="ha"
            name="{fieldname}_{i}_area"
          />
        </td>
        <td class="w-1/3 p-1">
          <LowLevelDecimalField
            bind:value={val.farmers}
            required={!!(val.date && !(val.households || val.area))}
            decimals={0}
            min={0}
            name="{fieldname}_{i}_farmers"
            unit={UsersIcon}
          />
        </td>
        <td class="w-1/3 p-1">
          <LowLevelDecimalField
            bind:value={val.households}
            required={!!(val.date && !(val.area || val.farmers))}
            decimals={0}
            min={0}
            name="{fieldname}_{i}_households"
            unit={HomeIcon}
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
