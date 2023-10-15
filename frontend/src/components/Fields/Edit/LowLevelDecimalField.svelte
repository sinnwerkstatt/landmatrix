<script lang="ts">
  import { _ } from "svelte-i18n"

  export let name: string
  export let value: number | undefined
  export let required = false
  export let unit = ""
  export let max: number | undefined = undefined
  export let min: number | undefined = undefined
  export let decimals = 2

  let step: number
  $: step = 1 / 10 ** decimals
  let placeholder: string
  $: placeholder = min && max ? `${min} – ${max}` : step === 1 ? "0" : "123.45"

  const onInput = (event: InputEvent) => {
    const targetValue = (event.target as HTMLInputElement).value
    value = targetValue === "" ? undefined : parseFloat(targetValue)
  }
</script>

<div class="flex grow justify-end">
  <input
    value={value ?? ""}
    type="number"
    class="inpt {$$props.class ?? ''}"
    {placeholder}
    {required}
    {min}
    {max}
    {step}
    {name}
    on:input|preventDefault={onInput}
  />
  {#if unit}
    <div class="flex items-center bg-lm-dark px-3 font-bold text-white">
      {$_(unit)}
    </div>
  {/if}
</div>

<style>
  /* Chrome, Safari, Edge, Opera */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  /* Firefox */
  input[type="number"] {
    -moz-appearance: textfield;
  }
</style>
