<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONLeaseFieldType } from "$lib/types/data"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"
  import HomeIcon from "$components/icons/HomeIcon.svelte"
  import UsersIcon from "$components/icons/UsersIcon.svelte"

  import { cardClass, labelClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: JSONLeaseFieldType[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  const emptyEntry: JSONLeaseFieldType = {
    current: false,
    date: null,
    area: null,
    farmers: null,
    households: null,
  }
  let valueCopy: JSONLeaseFieldType[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )
  let current = $state(value.length ? value.map(val => val.current).indexOf(true) : -1)

  const updateVal = () => {
    value = valueCopy.filter(val => !!(val.area || val.farmers || val.households))
  }

  const addEntry = () => {
    valueCopy = [...valueCopy, structuredClone(emptyEntry)]
    updateVal()
  }

  const removeEntry = (index: number) => {
    if (valueCopy[index].current) current = -1
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    updateVal()
  }

  const updateCurrent = (index: number) => {
    valueCopy = valueCopy.map((val, i) => ({ ...val, current: i === index }))
    updateVal()
  }
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Area")}
        <LowLevelDecimalField
          bind:value={val.area}
          unit={$_("ha")}
          name="{fieldname}_{i}_area"
          class="w-36"
          required={!!(val.date && !(val.farmers || val.households))}
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Farmers")}
        <LowLevelDecimalField
          bind:value={val.farmers}
          unit={UsersIcon}
          name="{fieldname}_{i}_farmers"
          class="w-36"
          decimals={0}
          required={!!(val.date && !(val.households || val.area))}
          onchange={updateVal}
        />
      </label>
      <label class={labelClass} for={undefined}>
        {$_("Households")}
        <LowLevelDecimalField
          bind:value={val.households}
          unit={HomeIcon}
          name="{fieldname}_{i}_households"
          class="w-36"
          decimals={0}
          required={!!(val.date && !(val.area || val.farmers))}
          onchange={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Date")}
        <LowLevelDateYearField
          bind:value={val.date}
          name="{fieldname}_{i}_date"
          onchange={updateVal}
        />
      </label>

      <label class={labelClass}>
        {$_("Current")}
        <input
          type="radio"
          bind:group={current}
          name="{fieldname}_current"
          required={valueCopy.length > 0}
          class="h-5 w-5 accent-violet-400 ring-red-600"
          disabled={!val.area && !val.farmers && !val.households}
          onchange={() => updateCurrent(i)}
          class:ring-2={value.length > 0 && current < 0}
          value={i}
        />
      </label>
      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}
  <AddButton onclick={addEntry} />
</div>
