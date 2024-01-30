<script lang="ts">
  // TODO WIP -> Is current radio or checkbox ?
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import ChoicesField from "$components/Fields/Edit2/ChoicesField.svelte"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  export let value: JSONCurrentDateChoiceFieldType
  export let fieldname: string

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  const createEmptyEntry = (): JSONCurrentDateChoiceFieldType[number] => ({
    choice: null,
    date: null,
    current: false,
  })

  let valueCopy = structuredClone<JSONCurrentDateChoiceFieldType>(
    value.length ? value : [createEmptyEntry()],
  )

  $: value = valueCopy.filter(val => !!val.choice)

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  const removeEntry = (index: number) =>
    (valueCopy = valueCopy.filter((val, i) => i !== index))

  const isCurrentRequired = (v: JSONCurrentDateChoiceFieldType) =>
    v.length ? !v.some(val => val.current) : false
</script>

<div class="grid gap-2 xl:grid-cols-2">
  {#each valueCopy as val, i}
    <div class:border-violet-400={val.current} class="flex flex-col gap-4 border p-3">
      <label class="flex flex-wrap items-center justify-between gap-4" for={undefined}>
        {$_("Choices")}
        <ChoicesField
          bind:value={val.choice}
          extras={{
            choices: extras.choices,
            required: !!val.date,
          }}
        />
      </label>

      <label class="flex flex-wrap items-center justify-between gap-4" for={undefined}>
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
            class="h-5 w-5 {valueCopy.length > 1 ? 'text-red-600' : 'text-gray-200'}"
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
