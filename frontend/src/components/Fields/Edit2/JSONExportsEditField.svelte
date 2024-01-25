<script lang="ts">
  // TODO WIP
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONExportsFieldType } from "$lib/types/newtypes"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import ChoicesField from "$components/Fields/Edit2/ChoicesField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  export let fieldname: string
  export let value: JSONExportsFieldType[] = []

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  let valueCopy: JSONExportsFieldType[] = structuredClone(
    value.length
      ? value
      : [
          {
            current: false,
            date: null,
            choices: [],
            area: null,
            yield: null,
            export: null,
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
        choices: [],
        area: null,
        yield: null,
        export: null,
      },
    ]
  }

  function removeEntry(index: number) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }

  const anySelectedAsCurrent = values => values.some(val => val.current)
  const isCurrentRequired = (values): boolean =>
    values.length > 0 && !anySelectedAsCurrent(values)
</script>

<table class="w-full">
  <thead>
    <tr>
      <th class="pr-2 text-center font-normal">{$_("Current")}</th>
      <th class="font-normal">{$_("Date")}</th>
      <th class="font-normal">{$_("Area")}</th>
      <th class="font-normal">{$_("Choices")}</th>
      <th class="font-normal">{$_("Yield")}</th>
      <th class="font-normal">{$_("Export")}</th>
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
            name="{fieldname}_{i}_current"
            required={isCurrentRequired(valueCopy)}
            disabled={!val.choices || !val.choices.length}
          />
        </td>

        <td class="w-1/6 p-1">
          <LowLevelDateYearField bind:value={val.date} name="{fieldname}_{i}_date" />
        </td>
        <td class="w-1/6 p-1">
          <LowLevelDecimalField
            bind:value={val.area}
            name="{fieldname}_{i}_area"
            unit="ha"
          />
        </td>
        <td class="w-2/6 p-1">
          <ChoicesField {extras} bind:value={val.choices} />
        </td>
        <td class="w-1/6 p-1">
          <LowLevelDecimalField
            bind:value={val.yield}
            unit="tons"
            name="{fieldname}_{i}_yield"
          />
        </td>
        <td class="w-1/6 p-1">
          <LowLevelDecimalField
            bind:value={val.export}
            name="{fieldname}_{i}_export"
            unit="%"
            max={100}
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
