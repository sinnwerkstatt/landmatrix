<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/newtypes"

  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  type EntryType = {
    current: boolean
    date: string | null
    area?: number
  }

  export let value: JSONCurrentDateAreaFieldType
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5 items-start"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"

  let valueCopy: EntryType[] = structuredClone(
    value.length ? value : [{ current: false, date: null }],
  )

  $: value = valueCopy.filter(val => !!val.area) as JSONCurrentDateAreaFieldType

  const addEntry = () => (valueCopy = [...valueCopy, { current: false, date: null }])
  const removeEntry = (index: number) =>
    (valueCopy = valueCopy.filter((val, i) => i !== index))

  const isCurrentRequired = (v: JSONCurrentDateAreaFieldType) =>
    v.length ? !v.some(val => val.current) : false
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <div class="grid gap-2 xl:grid-cols-2">
      {#each valueCopy as val, i}
        <div
          class:border-violet-400={val.current}
          class="flex flex-col gap-4 border p-3"
        >
          <label
            class="flex flex-wrap items-center justify-between gap-4"
            for={undefined}
          >
            {$_("Area")}
            <LowLevelDecimalField
              bind:value={val.area}
              unit={$_("ha")}
              name="{fieldname}_{i}_area"
              class="w-24 grow"
              required={val.current || val.date}
            />
          </label>

          <label
            class="flex flex-wrap items-center justify-between gap-4"
            for={undefined}
          >
            {$_("Date")}
            <LowLevelDateYearField
              bind:value={val.date}
              name="{fieldname}_{i}_date"
              class="w-36"
            />
          </label>
          <label class="flex items-center justify-between gap-4">
            {$_("Current")}
            <input
              type="checkbox"
              bind:checked={val.current}
              name="{fieldname}_{i}_current"
              required={isCurrentRequired(value)}
              class="accent-violet-400"
            />
          </label>

          <div class="text-right">
            <button
              type="button"
              disabled={valueCopy.length <= 1}
              on:click={() => removeEntry(i)}
              title={$_("Remove entry")}
            >
              <MinusIcon
                class="h-5 w-5 {valueCopy.length > 1
                  ? 'text-red-600'
                  : 'text-gray-200'}"
              />
            </button>
          </div>
        </div>
      {/each}

      <button
        type="button"
        on:click={addEntry}
        class="flex w-full items-center justify-center border p-2"
      >
        <PlusIcon class="h-7 w-7 text-black" />
      </button>
    </div>
  </div>
</div>
