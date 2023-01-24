<script lang="ts">
  import { _ } from "svelte-i18n"

  export let value: number | null | undefined
  export let name: string
  export let unit = ""
  export let required = false
  export let max: number
  export let min = 0
  export let decimals = 2
  export let emitUndefinedOnEmpty = false

  // fixme: JSON_Field
  // binding to input field of type number sets value to null on empty
  $: if (value === null && emitUndefinedOnEmpty) {
    value = undefined
  }
  $: step = 1 / 10 ** decimals
  $: placeholder = min && max ? `${min} – ${max}` : step === 1 ? "0" : "123.45"
</script>

<div class="flex whitespace-nowrap">
  <input
    bind:value
    type="number"
    class="inpt"
    {placeholder}
    {required}
    {min}
    {max}
    {step}
    {name}
  />
  {#if unit}
    <div
      class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 py-1.5 px-3 text-gray-600"
    >
      {$_(unit)}
    </div>
  {/if}
</div>
