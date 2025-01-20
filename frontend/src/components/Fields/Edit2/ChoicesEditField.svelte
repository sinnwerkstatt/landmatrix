<script lang="ts">
  import { tick } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import { slide } from "svelte/transition"

  import type { ValueLabelEntry } from "$lib/fieldChoices"

  interface Extras {
    multipleChoices?: boolean
    choices: ValueLabelEntry[]
    required?: boolean
    clearable?: boolean
    otherHint?: string
    placeholder?: string
    closeListOnChange?: boolean
  }

  interface Props {
    value: string | string[] | null
    fieldname: string
    extras?: Extras
    onchange?: () => void
  }

  let {
    value = $bindable(),
    fieldname,
    extras = { choices: [] },
    onchange,
  }: Props = $props()

  let multiple = $derived(!!extras.multipleChoices)
  let required = $derived(!!extras.required)
  let clearable = $derived(!!extras.clearable)

  let focused: boolean = $state(false)

  const setMultiValue = (items: ValueLabelEntry[]) => {
    value = !items || items.length === 0 ? [] : items.map(i => i.value)
  }
  const setValue = (item: ValueLabelEntry) => {
    value = !item ? null : item.value
  }
</script>

<div
  class="w-full ring-red-600"
  class:ring-2={required && (value?.length === 0 || !value)}
>
  <Select
    bind:focused
    {clearable}
    hasError={required && !value && !focused}
    items={extras.choices}
    groupBy={item => item.group}
    {multiple}
    on:input={e => (multiple ? setMultiValue : setValue)(e.detail)}
    on:change={() => onchange?.()}
    on:clear={() => tick().then(() => onchange?.())}
    placeholder={extras.placeholder ?? $_("Please select")}
    {required}
    showChevron
    value={multiple
      ? extras.choices.filter(c => (value || []).includes(c.value))
      : extras.choices.find(c => c.value === value)}
    name={fieldname}
    closeListOnChange={extras.closeListOnChange ?? !multiple}
  />

  {#if extras.otherHint && (value === "OTHER" || value?.includes("OTHER_LAND"))}
    <div class="m-1 italic text-orange-600" transition:slide>
      {extras.otherHint}
    </div>
  {/if}
</div>
