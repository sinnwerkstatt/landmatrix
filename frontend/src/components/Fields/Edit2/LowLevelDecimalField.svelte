<script lang="ts">
  import type { Component } from "svelte"
  import { _ } from "svelte-i18n"
  import type { FormEventHandler } from "svelte/elements"

  interface Props {
    name: string
    value: number | null
    required?: boolean
    unit?: string | Component
    max?: number | undefined
    min?: number | undefined
    decimals?: number
    placeholder?: string
    class?: string
    onchange?: () => void
  }

  let {
    name,
    value = $bindable(),
    required = false,
    unit = "",
    max = undefined,
    min = 0,
    decimals = 2,
    placeholder = "",
    class: className = "",
    onchange,
  }: Props = $props()

  let step: number = $derived(1 / 10 ** decimals)
  // $: placeholder = min && max ? `${min} – ${max}` : step === 1 ? "0" : "123.45"

  const oninput: FormEventHandler<HTMLInputElement> = event => {
    event.preventDefault()
    const targetValue = (event.target as HTMLInputElement).value
    value = targetValue === "" ? null : parseFloat(targetValue)
    onchange?.()
  }
</script>

<div class="flex grow justify-end">
  <input
    class="inpt {className}"
    {max}
    {min}
    {name}
    {oninput}
    {placeholder}
    {required}
    {step}
    type="number"
    value={value ?? ""}
  />
  {#if unit}
    <div class="flex items-center bg-gray-700 px-3 font-bold text-white">
      {#if typeof unit === "string"}
        {$_(unit)}
      {:else}
        {@const SvelteComponent = unit}
        <SvelteComponent class="h-4 w-4" />
      {/if}
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
    appearance: textfield;
  }
</style>
