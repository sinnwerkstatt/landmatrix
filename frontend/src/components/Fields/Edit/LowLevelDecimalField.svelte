<script lang="ts">
  import { _ } from "svelte-i18n"

  export let name: string
  export let value: number | undefined
  export let required = false
  export let unit = ""
  export let max: number | undefined
  export let min: number | undefined
  export let decimals = 2

  $: step = 1 / 10 ** decimals
  $: placeholder = min && max ? `${min} – ${max}` : step === 1 ? "0" : "123.45"

  const onInput = (event: InputEvent) => {
    const targetValue = (event.target as HTMLInputElement).value
    value = targetValue === "" ? undefined : parseFloat(targetValue)
  }
</script>

<div class="flex whitespace-nowrap">
  <input
    value={value ?? ""}
    type="number"
    class="inpt"
    {placeholder}
    {required}
    {min}
    {max}
    {step}
    {name}
    on:input|preventDefault={onInput}
  />
  {#if unit}
    <div
      class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 py-1.5 px-3 text-gray-600"
    >
      {$_(unit)}
    </div>
  {/if}
</div>
