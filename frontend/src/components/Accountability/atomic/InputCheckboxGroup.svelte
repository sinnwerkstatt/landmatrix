<script lang="ts">
  import { arrayIncludesAllOf, arrayIncludesAnyOf } from "$lib/accountability/helpers"

  import Checkbox from "./Checkbox.svelte"

  interface Props {
    group?: string[]
    choices?: { value: string; label: string }[]
    categories?: { values: string[]; label: string }[]
    orphansLabel?: string
    filter?: string
    readonlyCategories?: boolean
    disabled?: boolean
  }

  let {
    group = $bindable([]),
    choices = [],
    categories = [],
    orphansLabel = "Orphans",
    filter = "",
    readonlyCategories = false,
    disabled = false,
  }: Props = $props()

  function getOrphans(choices, categories) {
    if (categories.length > 0) {
      const allValues = categories.map(e => e.values).flat()
      let orphans: string[] = []
      choices.forEach(c => {
        if (!allValues.includes(c.value)) orphans = [...orphans, c]
      })
      return orphans
    } else {
      return choices
    }
  }

  function joinArrays(choices, categories) {
    const orphans = getOrphans(choices, categories)
    let result = []

    categories.forEach(category => {
      let categoryChoices = []
      category.values.forEach(val => {
        const choice = choices.find(e => e.value == val)
        if (choice) {
          categoryChoices = [...categoryChoices, choice]
        }
      })
      let obj = {
        label: category.label,
        choices: categoryChoices,
        values: categoryChoices.map(e => e.value),
      }
      obj.checked = arrayIncludesAllOf(group, obj.values)
      obj.partiallyChecked = arrayIncludesAnyOf(group, obj.values)
      result = [...result, obj]
    })

    if (orphans.length > 0) {
      let obj = {
        label: orphansLabel,
        choices: orphans,
        values: orphans.map(e => e.value),
      }
      obj.checked = arrayIncludesAllOf(group, obj.values)
      obj.partiallyChecked = arrayIncludesAnyOf(group, obj.values)
      result = [...result, obj]
    }

    return result
  }

  let cleanCategories: string[] | [] = $state([])
  $effect(() => {
    cleanCategories = categories ? joinArrays(choices, categories) : []
  })

  function checkChoice(value: string, checked: boolean) {
    // Add choice to groups
    if (checked) {
      group = [...group, value]
    } else {
      group = group.filter(v => v !== value)
    }

    // Update category status
    const category = cleanCategories.find(e => e.values.includes(value))
    category.checked = arrayIncludesAllOf(group, category.values)
    category.partiallyChecked = arrayIncludesAnyOf(group, category.values)

    // Force update with assignment
    cleanCategories = cleanCategories // TODO: force cleanCategories update somehow
  }

  function checkCategory(value: string, checked: boolean) {
    // Check or uncheck subgroup
    const category = cleanCategories.find(e => e.label == value)
    if (checked) {
      group = [...group, category.values].flat()
    } else {
      group = group.filter(e => !category.values.includes(e))
    }

    // Update category status
    category.checked = arrayIncludesAllOf(group, category.values)
    category.partiallyChecked = arrayIncludesAnyOf(group, category.values)

    // Force update with assignment
    cleanCategories = cleanCategories
  }

  function searchMatch(string: string, filter: string) {
    return string.toLowerCase().indexOf(filter.toLowerCase()) >= 0
  }

  function searchMatchInArray(array: string[], filter: string) {
    let result = false
    array.forEach(e => {
      if (e.toLowerCase().indexOf(filter.toLowerCase()) >= 0) result = true
    })
    return result
  }
</script>

<div class="">
  {#if categories.length > 0}
    {#each cleanCategories as { label, choices, checked, partiallyChecked }}
      {@const hidden = !searchMatchInArray(
        choices.map(e => e.label),
        filter,
      )}

      {#if readonlyCategories}
        <p class="m-0 my-2 px-4 uppercase text-a-gray-400">{label}</p>
      {:else}
        <Checkbox
          {label}
          value={label}
          bold={true}
          {checked}
          {partiallyChecked}
          {hidden}
          onchanged={checkCategory}
          {disabled}
        />
      {/if}

      <div class="pl-4">
        {#each choices as { label, value }}
          {@const checked = group.includes(value)}
          {@const hidden = !searchMatch(label, filter)}
          <Checkbox
            {label}
            {value}
            {checked}
            {hidden}
            onchanged={checkChoice}
            {disabled}
          />
        {/each}
      </div>
    {/each}
  {:else}
    {#each choices as { label, value }}
      {@const checked = group.includes(value)}
      {@const hidden = !searchMatch(label, filter)}
      <Checkbox {label} {value} {checked} {hidden} onchanged={checkChoice} {disabled} />
    {/each}
  {/if}
</div>
